#!/usr/bin/env python3
"""Run hierarchical-brain scenarios in fresh Claude Code sessions (not used by CI).

Each sample gets its own fixture in a new temporary directory, a fresh
non-interactive `claude -p` session with an explicit model and clean
configuration, and scripted follow-up turns that resume the same session.
Transcripts, replies, and before/after state are written to an evidence folder
outside the repository. This script records what happened; it does not grade.

    python run_hierarchical_scenario.py export-arm main /tmp/arms/red
    python run_hierarchical_scenario.py batch EVIDENCE --arm red=/tmp/arms/red \\
        --arm green=/tmp/arms/green --jobs H3:red:1 H3:green:1 --parallel 4
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import io
import json
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("brain_scenarios", HERE / "prepare_hierarchical_scenario.py")
scenarios = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = scenarios
spec.loader.exec_module(scenarios)

STANDARD = "sonnet"
MODELS = {name: STANDARD for name in scenarios.SCENARIOS}
RED_SKILLS = {"brain-write-tasks": "brain-write-tickets", "brain-decompose": None}
ALWAYS, IF_NO_CODE_CHANGE = "always", "if-no-code-change"
FOLLOWUPS = {
    "H1": [(ALWAYS, "Confirmed. D4 and D5 stay open; write it up.")],
    "H2": [(ALWAYS, "I haven't decided which machines are eligible or what error an ineligible "
                    "machine gets; leave those open. Keep the spec a draft for now; I'll review it "
                    "tomorrow.")],
    "H3": [(ALWAYS, "Approved as proposed.")],
    "H4": [(ALWAYS, "Show me the exact method signatures and which class each check lives in, "
                    "then I'll decide."),
           (ALWAYS, "Approved.")],
    "H5": [(ALWAYS, "Approved.")],
    "H6A": [(IF_NO_CODE_CHANGE, "Go ahead.")],
    "H6B": [(IF_NO_CODE_CHANGE, "Yes, those edits are mine. Go ahead.")],
    "H7": [(ALWAYS, "Approved.")],
    "H8": [(ALWAYS, "Looks good.")],
    "H9": [(ALWAYS, "If we fix exactly those problems so the validator passes, will the "
                    "feature's requirement coverage be complete?")],
    "H10D": [(IF_NO_CODE_CHANGE, "Go ahead.")],
    "H11": [(ALWAYS, "Keep the spec as a draft for now; I'll review it later.")],
}
WRAPPER = """You are an AI coding assistant working in the project at {cwd}. Run every command from that directory.
Your `CLAUDE.local.md` is {policy}. Read it first and treat it as loaded instructions.
Use only the skills named here and the skills they mention; don't invoke other installed skills or plugins.
{skill_line}{context}The user says: "{trigger}"
Behave exactly as you would in a real session. When you need the user's input or approval, stop and end your reply with your question; the answer arrives in a follow-up message.
End every reply with a section "Files read and commands run:" that lists each one, including every file written and every subagent dispatched, with its model."""
TURN_TIMEOUT = 5 * 60
DEFAULT_MAX_TURNS = 5
DEFAULT_BUDGET_USD = 1.00


def export_arm(ref: str, destination: Path) -> None:
    """Export the skill set at `ref` without tests or the implementation plan."""
    repo = HERE.parents[2]
    prefix = "skills/experimental_v4/"
    archive = subprocess.run(["git", "-C", str(repo), "archive", "--format=tar", ref, prefix],
                             check=True, capture_output=True).stdout
    destination.mkdir(parents=True)
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        for member in tar.getmembers():
            rel = member.name[len(prefix):]
            if not rel or rel.split("/")[0] in ("tests", "IMPLEMENTATION_PLAN.md"):
                continue
            member.name = rel
            tar.extract(member, destination, filter="data")
    commit = subprocess.run(["git", "-C", str(repo), "rev-parse", ref],
                            check=True, capture_output=True, text=True).stdout.strip()
    (destination.parent / f"{destination.name}.ref").write_text(f"{ref} {commit}\n")


def tree_digest(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    return {p.relative_to(path).as_posix(): hashlib.sha1(p.read_bytes()).hexdigest()
            for p in sorted(path.rglob("*")) if p.is_file() and ".git" not in p.relative_to(path).parts}


def git_state(path: Path) -> str:
    out = []
    for args in (("status", "--porcelain", "--untracked-files=all"), ("log", "--oneline", "-5"),
                 ("diff", "HEAD"), ("branch", "--show-current")):
        result = subprocess.run(["git", "-C", str(path), *args], capture_output=True, text=True)
        out.append(f"$ git {' '.join(args)}\n{result.stdout}{result.stderr}")
    return "\n".join(out)


def code_digest(cwd: Path) -> str:
    files = [cwd / "machine_control.py", *sorted((cwd / "tests").glob("*.py"))]
    return hashlib.sha1(b"".join(f.read_bytes() for f in files if f.exists())).hexdigest()


def read_only(*paths: Path) -> list[str]:
    """Permission rules that let the agent read, but not edit, these trees."""
    rules = set()
    for path in paths:
        for variant in (path, path.resolve()):
            rules.add(f"Read(/{variant}/**)")
    return sorted(rules)


def claude(prompt: str, run_dir: Path, model: str, extra: list[str], log: Path,
           readable: list[str], budget: float = DEFAULT_BUDGET_USD,
           turns: int = DEFAULT_MAX_TURNS, timeout: int = TURN_TIMEOUT,
           subagents: bool = False) -> dict:
    command = ["claude", "-p", prompt, "--model", model, "--setting-sources", "project,local",
               "--disable-slash-commands", "--strict-mcp-config",
               "--permission-mode", "acceptEdits", "--allowedTools", "Bash", *readable,
               "--max-budget-usd", str(budget), "--max-turns", str(turns),
               "--output-format", "stream-json", "--verbose", *extra]
    if not subagents:
        command += ["--disallowedTools", "Agent"]
    started = time.time()
    with log.open("w") as out:
        process = subprocess.run(command, cwd=run_dir, stdout=out, stderr=subprocess.PIPE,
                                 text=True, timeout=timeout)
    result = {}
    for line in log.read_text().splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "result":
            result = event
    return {"exit": process.returncode, "stderr": process.stderr[-2000:],
            "seconds": round(time.time() - started), "session_id": result.get("session_id"),
            "cost_usd": result.get("total_cost_usd"), "reply": result.get("result", ""),
            "is_error": result.get("is_error"), "num_turns": result.get("num_turns")}


def run(scenario: str, arm: str, arm_dir: Path, sample: int, evidence: Path,
        model: str = STANDARD, budget: float = DEFAULT_BUDGET_USD,
        turns: int = DEFAULT_MAX_TURNS, timeout: int = TURN_TIMEOUT,
        subagents: bool = False, sample_budget: float = 2.00) -> Path:
    out = evidence / f"{scenario}-{arm}-{sample}"
    out.mkdir(parents=True)
    root = Path(tempfile.mkdtemp(prefix="brain-run-"))
    skill = scenarios.SCENARIOS[scenario][1]
    if arm == "red" and skill in RED_SKILLS:
        skill = RED_SKILLS[skill]
    if skill and not (arm_dir / skill / "SKILL.md").is_file():
        skill = None
    prepared = scenarios.prepare(root / "repo", scenario,
                                 policy=arm_dir / "brain-init" / "references" / "CLAUDE.local.md",
                                 skills_dir=arm_dir)
    brains = {"main-brain": prepared.repo / ".brain",
              **{f"extra-{i}": d for i, d in enumerate(prepared.add_dirs)}}
    for name, path in brains.items():
        shutil.copytree(path, out / "before" / name)
    (out / "before" / "git.txt").write_text(git_state(prepared.repo) + "\n\n# agent directory\n"
                                            + git_state(prepared.cwd))
    skill_line = ""
    if skill:
        skill_line = (f"You have the skill {skill}. Read {arm_dir / skill}/SKILL.md and follow it. "
                      f"${{CLAUDE_SKILL_DIR}} means {arm_dir / skill}. Skills it mentions live in "
                      f"{arm_dir}/.\n")
    context = f"Context: {prepared.context}\n" if prepared.context else ""
    prompt = WRAPPER.format(cwd=prepared.cwd, policy=prepared.repo / "CLAUDE.local.md",
                            skill_line=skill_line, context=context, trigger=prepared.trigger)
    extra = [arg for d in prepared.add_dirs for arg in ("--add-dir", str(d))]
    first = extra + (["--worktree", prepared.worktree] if prepared.worktree else [])
    meta = {"scenario": scenario, "arm": arm, "arm_dir": str(arm_dir),
            "arm_ref": (arm_dir.parent / f"{arm_dir.name}.ref").read_text().strip()
            if (arm_dir.parent / f"{arm_dir.name}.ref").exists() else None,
            "sample": sample, "model": model, "skill": skill, "repo": str(prepared.repo),
            "cwd": str(prepared.cwd), "add_dirs": [str(d) for d in prepared.add_dirs],
            "worktree": prepared.worktree, "prompt": prompt, "turns": []}
    (out / "prompt.txt").write_text(prompt)
    before_code = code_digest(prepared.cwd)
    readable = read_only(arm_dir, prepared.repo)
    meta["arm_digest_before"] = hashlib.sha1(json.dumps(tree_digest(arm_dir)).encode()).hexdigest()
    turn = claude(prompt, prepared.launch, model, first, out / "turn1.jsonl", readable,
                  budget, turns, timeout, subagents)
    meta["turns"].append({"user": prompt, **turn})
    (out / "reply1.md").write_text(turn["reply"] or "")
    for index, (condition, text) in enumerate(FOLLOWUPS.get(scenario, []), start=2):
        last = meta["turns"][-1]
        if not last.get("session_id") or last.get("is_error") or last.get("exit") != 0:
            break
        remaining = sample_budget - sum(t.get("cost_usd") or 0 for t in meta["turns"])
        if remaining <= 0:
            meta["turns"].append({"user": None, "skipped": "estimated sample budget exhausted"})
            break
        after_code = code_digest(prepared.cwd)
        if condition == IF_NO_CODE_CHANGE and after_code != before_code:
            meta["turns"].append({"user": None, "skipped": f"code changed: {text}"})
            break
        before_code = after_code
        message = f"The user replies: {text}"
        turn = claude(message, prepared.cwd, model,
                      extra + ["--resume", meta["turns"][-1]["session_id"]],
                      out / f"turn{index}.jsonl", readable,
                      min(budget, remaining), turns, timeout, subagents)
        meta["turns"].append({"user": message, **turn})
        (out / f"reply{index}.md").write_text(turn["reply"] or "")
    for name, path in brains.items():
        if path.exists():
            shutil.copytree(path, out / "after" / name)
    (out / "after").mkdir(exist_ok=True)
    (out / "after" / "git.txt").write_text(git_state(prepared.repo) + "\n\n# agent directory\n"
                                           + git_state(prepared.cwd))
    meta["digest_before"] = {n: tree_digest(out / "before" / n) for n in brains}
    meta["digest_after"] = {n: tree_digest(out / "after" / n) for n in brains}
    meta["arm_digest_after"] = hashlib.sha1(json.dumps(tree_digest(arm_dir)).encode()).hexdigest()
    meta["cost_usd"] = sum(t.get("cost_usd") or 0 for t in meta["turns"])
    (out / "meta.json").write_text(json.dumps(meta, indent=2))
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    exp = sub.add_parser("export-arm")
    exp.add_argument("ref")
    exp.add_argument("destination", type=Path)
    batch = sub.add_parser("batch")
    batch.add_argument("evidence", type=Path)
    batch.add_argument("--arm", action="append", required=True, help="name=exported skill dir")
    batch.add_argument("--jobs", nargs="+", required=True, help="SCENARIO:ARM:SAMPLE")
    batch.add_argument("--parallel", type=int, default=1)
    batch.add_argument("--model", default=STANDARD)
    batch.add_argument("--max-budget-usd", type=float, default=DEFAULT_BUDGET_USD)
    batch.add_argument("--sample-budget-usd", type=float, default=2.00)
    batch.add_argument("--max-turns", type=int, default=DEFAULT_MAX_TURNS)
    batch.add_argument("--timeout", type=int, default=TURN_TIMEOUT)
    batch.add_argument("--subagents", action="store_true")
    batch.add_argument("--execute", action="store_true", help="explicitly allow paid agent runs")
    args = parser.parse_args()
    if args.command == "export-arm":
        export_arm(args.ref, args.destination)
        return 0
    if not 1 <= args.parallel <= 4 or args.max_budget_usd <= 0 or args.sample_budget_usd <= 0 or args.max_turns < 1 or args.timeout < 10:
        parser.error("invalid execution limits")
    if not args.execute:
        print("DRY RUN: no agents launched. Add --execute for paid agent sessions.")
        for job in args.jobs:
            print(f"  {job}: model={args.model}, maximum per turn=${args.max_budget_usd:.2f}, per sample=${args.sample_budget_usd:.2f}")
        return 0
    arms = dict(item.split("=", 1) for item in args.arm)
    limited = []

    def job(spec: str) -> str:
        scenario, arm, sample = spec.split(":")
        if limited:
            return f"{spec} SKIPPED: usage limit reached earlier in this batch"
        try:
            out = run(scenario, arm, Path(arms[arm]), int(sample), args.evidence,
                      args.model, args.max_budget_usd, args.max_turns,
                      args.timeout, args.subagents, args.sample_budget_usd)
            meta = json.loads((out / "meta.json").read_text())
            if any(t.get("is_error") or t.get("exit") not in (None, 0) for t in meta["turns"]):
                if any(any(word in ((t.get("reply") or "") + (t.get("stderr") or "")).lower()
                           for word in ("limit", "budget", "quota")) for t in meta["turns"]):
                    limited.append(spec)
                return f"{spec} ERROR in a turn: void, rerun ({out.name})"
            return f"{spec} done ${meta['cost_usd']:.2f} turns={len(meta['turns'])}"
        except Exception as exc:  # keep the batch going; report the failure
            return f"{spec} ERROR {type(exc).__name__}: {exc}"

    with ThreadPoolExecutor(args.parallel) as pool:
        for line in pool.map(job, args.jobs):
            print(line, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
