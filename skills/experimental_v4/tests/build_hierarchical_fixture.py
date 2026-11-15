#!/usr/bin/env python3
"""Build an isolated, reproducible repository for hierarchical agent scenarios.

Creates a fresh repository with committed baseline code, an ignored project
brain, and approved feature stages. Commits use a fixed identity and date, so
the same stage always yields the same baseline revision. The collaboration
policy (CLAUDE.local.md) is not committed: it belongs to the skill set under
test and is written, untracked, only when ``policy`` is given. Does not run or
grade any AI agent.
"""
from __future__ import annotations

import argparse
import importlib.util
import os
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "tests" / "fixture" / "start-machine-app"
DOCS = ROOT / "tests" / "fixture" / "hierarchical-brain" / ".brain" / "features" / "start-machine"
VALIDATOR = ROOT / "brain-init" / "scripts" / "validate_feature_docs.py"
LAYERS = (
    "01-brief", "02-specifications", "03-components",
    "04-implementation-plans", "05-tasks",
)
STAGES = ("none", "brief", "spec", "components", "plans", "tasks")
FIXED_DATE = "2026-11-01T09:00:00+0000"
ADR_PATH = "adrs/0001-session-routing-registry-state.md"

_spec = importlib.util.spec_from_file_location("feature_validator", VALIDATOR)
validator = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(validator)

ADR = """# ADR 0001: Session routes requests; MachineRegistry owns machine state

Status: accepted (2026-10-20)

## Context

Requests arrive through `Session`; machine state lives in `MachineRegistry`. A separate machine manager was proposed and rejected.

## Decision

`Session.handle` remains the single request dispatcher and the owner of the client session. `MachineRegistry` remains the single owner of machine state transitions. New machine operations extend these two owners; no separate manager or service is introduced.

## Consequences

A new operation adds a registry method and a dispatch branch. Changing either ownership requires a superseding ADR.
"""

ELIGIBILITY_DECISION = (
    "- 2026-11-03: StartMachine eligibility. A machine is eligible to start only "
    "when `enabled` is true and `state` is `\"stopped\"`; an ineligible request "
    "fails with `not_eligible` and changes nothing. Resolves the open decisions in "
    "`features/start-machine/01-brief/brief.md`.\n"
)


def git(path: Path, *args: str) -> str:
    env = {**os.environ, "GIT_AUTHOR_DATE": FIXED_DATE, "GIT_COMMITTER_DATE": FIXED_DATE}
    result = subprocess.run(["git", "-C", str(path), *args],
                            check=True, capture_output=True, text=True, env=env)
    return result.stdout.strip()


def exclude(repo: Path, *patterns: str) -> None:
    common = Path(git(repo, "rev-parse", "--path-format=absolute", "--git-common-dir"))
    target = common / "info" / "exclude"
    existing = target.read_text(encoding="utf-8").splitlines() if target.exists() else []
    with target.open("a", encoding="utf-8") as f:
        for pattern in patterns:
            if pattern not in existing:
                f.write(f"{pattern}\n")


def refresh_parent_hashes(feature: Path) -> None:
    """Record current direct-parent fingerprints, highest level first.

    Fixture construction only: it represents approvals recorded against the
    documents as built. Unknown parents are left without a fingerprint so a
    deliberately broken reference stays visible to the validator.
    """
    for layer in LAYERS[1:]:
        for path in sorted((feature / layer).glob("*.md")):
            known = {}
            for folder in LAYERS:
                for candidate in (feature / folder).glob("*.md"):
                    meta, _ = validator.parse_document(candidate)
                    known.setdefault(meta["id"], candidate)
            meta, _ = validator.parse_document(path)
            values = [f"{p}@{validator.git_blob_sha(known[p])}"
                      for p in meta["parents"] if p in known]
            source = path.read_text(encoding="utf-8")
            updated = re.sub(r"(?m)^parent_hashes:.*$",
                             "parent_hashes: [" + ", ".join(values) + "]", source, count=1)
            path.write_text(updated, encoding="utf-8")


def write_index(brain: Path, revision: str, extra_rows: list[tuple[str, str, str]] = (),
                git_line: str = "ignored") -> None:
    rows = [(ADR_PATH, "Session routes requests; MachineRegistry owns state", "accepted")]
    features = brain / "features"
    if features.exists():
        for path in sorted(features.rglob("*.md")):
            rel = path.relative_to(brain).as_posix()
            if path.name == "execution.md":
                rows.append((rel, "Observed progress and verification", "in progress"))
                continue
            meta, body = validator.parse_document(path)
            title = next((line[2:].strip() for line in body.splitlines()
                          if line.startswith("# ")), meta["id"])
            rows.append((rel, f"{meta['id']}: {title}", meta["status"]))
    rows.extend(extra_rows)
    table = "".join(f"| `{p}` | {purpose} | {status} |\n" for p, purpose, status in rows)
    (brain / "00_index.md").write_text(
        f"# Project Brain Index\n\nLast synced: {revision} (2026-11-01)\nGit: {git_line}\n"
        "Main branch: main\n\n## Root files\n\n| File | Purpose | Status |\n|---|---|---|\n"
        "| `glossary.md` | Canonical terms | current |\n"
        "| `09_user_decisions.md` | Approved user decisions | current |\n"
        "| `state.md` | Feature state | current |\n"
        f"\n## Documents\n\n| Path | Purpose | Status |\n|---|---|---|\n{table}",
        encoding="utf-8",
    )


def build(destination: Path, stage: str = "none", policy: Path | None = None) -> Path:
    if stage not in STAGES:
        raise ValueError(f"invalid stage {stage!r}; choose from {STAGES}")
    if destination.exists():
        raise FileExistsError(f"refusing to overwrite existing fixture {destination}")
    shutil.copytree(APP, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    git(destination, "init", "-q", "-b", "main")
    git(destination, "config", "user.name", "Brain Fixture")
    git(destination, "config", "user.email", "fixture@example.invalid")
    git(destination, "add", "machine_control.py", "tests", "README.md", "docs")
    git(destination, "commit", "-qm", "feat: machine control with StopMachine")
    revision = git(destination, "rev-parse", "HEAD")
    exclude(destination, ".brain/", "__pycache__/", "*.pyc", "CLAUDE.local.md", ".claude/worktrees/")
    if policy is not None:
        shutil.copyfile(policy, destination / "CLAUDE.local.md")

    brain = destination / ".brain"
    brain.mkdir()
    (brain / "adrs").mkdir()
    (brain / ADR_PATH).write_text(ADR, encoding="utf-8")
    (brain / "glossary.md").write_text(
        "# Glossary\n\n"
        "- **Session**: the request dispatcher; validates requests and routes them. Owns the client session.\n"
        "- **MachineRegistry**: the owner of machine state transitions.\n"
        "- **Machine**: a controlled machine with `state` (`stopped` or `running`) and `enabled`.\n",
        encoding="utf-8",
    )
    decisions = ("# User decisions\n\n- Session keeps message routing and connection ownership; "
                 f"MachineRegistry keeps machine state transitions. See `{ADR_PATH}`.\n")
    count = STAGES.index(stage)
    if count >= STAGES.index("spec"):
        decisions += ELIGIBILITY_DECISION
    (brain / "09_user_decisions.md").write_text(decisions, encoding="utf-8")
    (brain / "state.md").write_text(
        "# State\n\n## Done\n\n- StopMachine request handling.\n\n## Planned\n\n- StartMachine"
        + (" (see `features/start-machine/`)." if count else ".") + "\n",
        encoding="utf-8",
    )
    if count:
        feature = brain / "features" / "start-machine"
        for layer in LAYERS[:count]:
            shutil.copytree(DOCS / layer, feature / layer)
        plans = feature / "04-implementation-plans"
        for plan in plans.glob("*.md") if plans.exists() else ():
            plan.write_text(plan.read_text(encoding="utf-8").replace("{{BASELINE_SHA}}", revision),
                            encoding="utf-8")
        refresh_parent_hashes(feature)
        if stage == "tasks":
            shutil.copyfile(DOCS / "execution.md", feature / "execution.md")
    write_index(brain, revision)
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path, help="new empty destination (must not exist)")
    parser.add_argument("--stage", choices=STAGES, default="none",
                        help="highest preapproved document layer to copy")
    parser.add_argument("--policy", type=Path, help="CLAUDE.local.md to install untracked")
    args = parser.parse_args()
    try:
        built = build(args.destination.resolve(), args.stage, args.policy)
    except (FileExistsError, ValueError, OSError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"{exc}\n")
    print(f"Fixture ready: {built}; stage={args.stage}; no agent run")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
