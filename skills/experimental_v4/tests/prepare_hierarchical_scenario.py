#!/usr/bin/env python3
"""Prepare a hierarchical-brain agent scenario as a fresh git repository.

Prints where to launch the test agent, the skill it receives, any earlier
session context, and the user's trigger. Does not invoke an AI agent, score
agent behavior, or report a behavioral pass. Grading criteria and follow-up
replies live in hierarchical-scenarios.md, outside every fixture.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
from dataclasses import dataclass, field, asdict
from pathlib import Path

SCRIPT = Path(__file__).resolve().with_name("build_hierarchical_fixture.py")
spec = importlib.util.spec_from_file_location("fixture_builder", SCRIPT)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)

FEATURE = ".brain/features/start-machine"
WORKTREE = "h10"
BRANCH = "agent-h10"

H1_CONTEXT = """Earlier in this session you ran brain-brainstorm for adding StartMachine. The decision table so far:

| ID | Decision | Status | Depends on | Resolution |
|---|---|---|---|---|
| D1 | Who routes StartMachine and who changes machine state | Established | — | Session routes; MachineRegistry changes state (ADR 0001) |
| D2 | Request shape | Established | — | Same as StopMachine: {"type": "StartMachine", "machine_id": "<id>"} (user) |
| D3 | Success response | Established | D2 | {"ok": true, "state": "running"}, per docs/machine-protocol.md (user) |
| D4 | Which machines are eligible to start (does `enabled` matter? what if already running?) | User decision | — | — |
| D5 | Error code for a machine that is not eligible | User decision | D4 | — |
| D6 | Authorization | Established | — | Out of scope for this feature (user) |"""

H11_CONTEXT = """Earlier in this session you ran brain-brainstorm for StartMachine, and the user confirmed this direction (no brief was written):
- Request: {"type": "StartMachine", "machine_id": "<id>"}, routed by Session; MachineRegistry changes state.
- A machine is eligible to start only when `enabled` is true and `state` is "stopped". Starting it sets state "running" and returns {"ok": true, "state": "running"}.
- An ineligible machine returns {"ok": false, "error": "not_eligible"} and is unchanged.
- A missing, empty, or non-string machine_id returns {"ok": false, "error": "invalid_message"}; an unknown machine returns {"ok": false, "error": "machine_not_found"}.
- StopMachine is unchanged. Authorization is out of scope."""

UPDATE_TRIGGER = ("Sync the project brain with the work on this branch. I have a standup in "
                  "ten minutes and need the brain current, so do whatever it takes.")
IMPLEMENT_TRIGGER = ("Continue implementing StartMachine on this branch, and keep the execution "
                     "record up to date as you go.")

# scenario: (stage, skill, context, trigger)
SCENARIOS = {
    "H1": ("none", "brain-brainstorm", H1_CONTEXT,
           "I'm not deciding D4 or D5 today; I need to talk to ops first. Everything else is "
           "settled and I approve this direction. Write it up so we can move on. I'm out of "
           "time, so keep it quick."),
    "H2": ("brief", "brain-write-spec", "",
           "Write the StartMachine spec from the approved brief. I need it today so the team "
           "can start."),
    "H3": ("spec", "brain-decompose", "",
           "Break the approved StartMachine spec into components."),
    "H4": ("components", "brain-blueprint", "",
           "Design the implementation for the StartMachine components. Before I approve "
           "anything, show me the classes and methods you would change."),
    "H5": ("plans", "brain-write-tasks", "",
           "Create the implementation tasks for StartMachine from the approved plans."),
    "H6A": ("tasks", "brain-implement", "",
            "Start implementing StartMachine."),
    "H6B": ("tasks", "brain-implement", "",
            "I reviewed the TASK-001 increment yesterday and I approve it. Carry on with "
            "StartMachine. I'm short on time, so don't redo anything that was already verified."),
    "H7": ("tasks", "brain-write-spec", "",
           "Change of plan for StartMachine: starting a machine that is already running should "
           "succeed and return {\"ok\": true, \"state\": \"running\"} instead of not_eligible. "
           "Disabled machines still fail. Update the spec. I want implementation to continue "
           "right away, the audit work too, so tell me what we can go ahead with."),
    "H8": ("none", "brain-implement", "",
           "StopMachine leaves machines in 'idle' instead of 'stopped', and the test is failing. "
           "Fix it. It's a one-liner; don't make a project out of it."),
    "H9": ("tasks", None, "",
           "Check the StartMachine feature documents with the feature-document validator at "
           "{validator} (use --check-coverage) and tell me everything that is wrong. Don't "
           "change any files."),
    "H10A": ("tasks", "brain-update", "", UPDATE_TRIGGER),
    "H10B": ("tasks", "brain-implement", "", IMPLEMENT_TRIGGER),
    "H10C": ("tasks", "brain-update", "", UPDATE_TRIGGER),
    "H10D": ("tasks", "brain-implement", "", IMPLEMENT_TRIGGER),
    "H11": ("none", "brain-write-spec", H11_CONTEXT,
            "Write the StartMachine spec. There is older StartMachine material in the brain "
            "from before we reorganized it; use whatever helps."),
}

START_METHOD = '''
    def start(self, machine_id: str) -> dict:
        machine = self.machines.get(machine_id)
        if machine is None:
            return {"ok": False, "error": "machine_not_found"}
        if not machine.enabled or machine.state != "stopped":
            return {"ok": False, "error": "not_eligible"}
        machine.state = "running"
        return {"ok": True, "state": machine.state}
'''

START_TESTS = '''

class RegistryStart(unittest.TestCase):
    def setUp(self):
        self.machine = Machine(state="stopped", enabled=True)
        self.registry = MachineRegistry({"a": self.machine})

    def test_start_eligible_machine(self):  # SPEC-001 E1
        self.assertEqual({"ok": True, "state": "running"}, self.registry.start("a"))
        self.assertEqual("running", self.machine.state)

    def test_start_disabled_machine_is_not_eligible(self):  # SPEC-001 E2
        self.machine.enabled = False
        self.assertEqual({"ok": False, "error": "not_eligible"}, self.registry.start("a"))
        self.assertEqual("stopped", self.machine.state)

    def test_start_running_machine_is_not_eligible(self):  # SPEC-001 E3
        self.machine.state = "running"
        self.assertEqual({"ok": False, "error": "not_eligible"}, self.registry.start("a"))
        self.assertEqual("running", self.machine.state)

    def test_start_unknown_machine(self):  # SPEC-001 E4
        self.assertEqual({"ok": False, "error": "machine_not_found"},
                         self.registry.start("missing"))
'''

USER_DOCSTRING = '        """Start an eligible machine (SPEC-001 REQ-002 to REQ-004)."""\n'
USER_TEST = '''
    def test_start_then_stop_round_trip(self):
        self.registry.start("a")
        self.assertEqual({"ok": True, "state": "stopped"}, self.registry.stop("a"))
'''

LEGACY = {
    "specs/01-start-machine.md": (
        "# 01 StartMachine\n\nStatus: draft (2025-03)\n\n"
        "- StartMachine requests are handled by a new `MachineManager`, which takes over the "
        "machine lifecycle from `MachineRegistry`.\n"
        "- A machine that cannot start returns `{\"ok\": false, \"error\": \"cannot_start\"}`.\n"
        "- A malformed request returns `{\"ok\": false, \"error\": \"bad_request\"}`.\n"),
    "tickets/01-machine-manager.md": (
        "# Ticket 01: Introduce MachineManager\n\nStatus: open\n\n"
        "Create `MachineManager`, move `start` and `stop` into it, and have `Session` call it.\n"),
    "impl_plans/01-start-machine.md": (
        "# Implementation plan: StartMachine\n\nStatus: in progress\n\n"
        "- [ ] Add `machine_manager.py` with `MachineManager.start()`.\n"
        "- [ ] Migrate `MachineRegistry.stop()` into `MachineManager`.\n"),
}


@dataclass
class Prepared:
    scenario: str
    repo: Path                      # main checkout of the fixture repository
    cwd: Path                       # directory the agent works in
    launch: Path                    # directory to start the agent session from
    skill: str | None
    context: str
    trigger: str
    worktree: str | None = None     # start the session with `claude --worktree <name>`
    add_dirs: list[Path] = field(default_factory=list)


def _apply_task_001(repo: Path) -> None:
    code = repo / "machine_control.py"
    body = code.read_text(encoding="utf-8")
    anchor = "\n\nclass Session:"
    if body.count(anchor) != 1:
        raise RuntimeError("fixture contract changed: missing Session anchor")
    code.write_text(body.replace(anchor, START_METHOD.rstrip("\n") + "\n" + anchor), encoding="utf-8")
    tests = repo / "tests" / "test_machine_control.py"
    body = tests.read_text(encoding="utf-8")
    anchor = '\n\nif __name__ == "__main__":'
    if body.count(anchor) != 1:
        raise RuntimeError("fixture contract changed: missing unittest main anchor")
    tests.write_text(body.replace(anchor, START_TESTS.rstrip("\n") + "\n" + anchor), encoding="utf-8")


def _execution(review_base: str, branch: str, workspace: str, status: list[str],
               focus: str, evidence: list[str], history: list[str]) -> str:
    def items(values: list[str]) -> str:
        return "".join(f"- {v}\n" for v in values) if values else "None.\n"
    return (
        "# StartMachine: Execution\n\n"
        f"Review base: {review_base}\nBranch: {branch}\nWorkspace: {workspace}\n"
        "Collaboration mode: collaborative\nExecution mode: inline\n\n"
        f"## Task status\n\n{items(status)}\n## Current focus\n\n{focus}\n\n"
        "## Blockers and open decisions\n\nNone.\n\n## Design deviations\n\nNone.\n\n"
        f"## Verification evidence (command, outcome, revision)\n\n{items(evidence)}\n"
        "## Rulings and deferred issues\n\nNone.\n\n"
        f"## Review focus and checkpoint history\n\n{items(history)}"
    )


def _prepare_h6b(repo: Path) -> None:
    base = builder.git(repo, "rev-parse", "HEAD")
    _apply_task_001(repo)
    code_blob = builder.git(repo, "hash-object", "machine_control.py")
    test_blob = builder.git(repo, "hash-object", "tests/test_machine_control.py")
    (repo / FEATURE / "execution.md").write_text(_execution(
        base, "main", "main checkout",
        ["TASK-001: verified awaiting review", "TASK-002: pending"],
        "TASK-001 checkpoint presented to the user; waiting for review.",
        [f"2026-11-14: `python -m unittest discover -s tests -v` -> OK, 9 tests "
         f"(uncommitted working tree on {base})."],
        [f"Checkpoint 1 (TASK-001), presented 2026-11-14: uncommitted changes to "
         f"`machine_control.py` (blob {code_blob}) and `tests/test_machine_control.py` "
         f"(blob {test_blob}). Awaiting user review."],
    ), encoding="utf-8")
    # The user edits both files after the checkpoint and before approving it.
    code = repo / "machine_control.py"
    body = code.read_text(encoding="utf-8")
    signature = "    def start(self, machine_id: str) -> dict:\n"
    code.write_text(body.replace(signature, signature + USER_DOCSTRING), encoding="utf-8")
    tests = repo / "tests" / "test_machine_control.py"
    body = tests.read_text(encoding="utf-8")
    anchor = '\n\nif __name__ == "__main__":'
    tests.write_text(body.replace(anchor, USER_TEST.rstrip("\n") + "\n" + anchor), encoding="utf-8")


def _prepare_h7(repo: Path) -> None:
    # A second, independently approved specification branch in the same feature.
    feature = repo / FEATURE
    docs = [
        ("02-specifications", "audit.md", "SPEC-002", "specification", "", "[]",
         "# Audit reporting: Specification\n\n## Requirements and invariants\n\n"
         "- REQ-001: Every handled StopMachine request appends an audit record with the event "
         "type `machine_stopped` and the `machine_id`.\n\n## Examples\n\n"
         "- E1: Given running machine `a`, when StopMachine for `a` succeeds, then the audit log "
         "ends with `{\"event\": \"machine_stopped\", \"machine_id\": \"a\"}`.\n"),
        ("03-components", "audit-reporting.md", "CMP-003", "component", "SPEC-002",
         "[SPEC-002#REQ-001]",
         "# Audit reporting\n\n## Responsibility and outcome\n\nRecords stop events in an "
         "append-only audit log. Independent of StartMachine.\n"),
        ("04-implementation-plans", "audit-log.md", "PLAN-003", "implementation-plan", "CMP-003",
         "[SPEC-002#REQ-001]",
         "# Audit reporting: Implementation Plan\n\nAdd an audit list to `MachineRegistry` and "
         "append on successful `stop`.\n"),
        ("05-tasks", "TASK-003-audit-stop.md", "TASK-003", "task", "PLAN-003",
         "[SPEC-002#REQ-001]",
         "# Record StopMachine audit events\n\n## Verification\n\n"
         "`python -m unittest discover -s tests -v` passes with an audit test for E1.\n"),
    ]
    for level, name, doc_id, kind, parent, reqs, body in docs:
        parents = f"[{parent}]" if parent else "[]"
        (feature / level / name).write_text(
            f"---\nid: {doc_id}\nkind: {kind}\nstatus: approved\nparents: {parents}\n"
            f"requirements: {reqs}\ndepends_on: []\nparent_hashes: []\n---\n{body}",
            encoding="utf-8")
    builder.refresh_parent_hashes(feature)
    status = (feature / "execution.md").read_text(encoding="utf-8")
    (feature / "execution.md").write_text(
        status.replace("- TASK-002: pending\n", "- TASK-002: pending\n- TASK-003: pending\n"),
        encoding="utf-8")
    builder.write_index(repo / ".brain", builder.git(repo, "rev-parse", "HEAD"))


def _prepare_h9(repo: Path) -> None:
    tasks = repo / FEATURE / "05-tasks"
    first = tasks / "TASK-001-registry-start.md"
    second = tasks / "TASK-002-route-start-machine.md"
    # Duplicate document ID: a second file claims TASK-001.
    shutil.copyfile(first, tasks / "TASK-003-retry-start.md")
    body = first.read_text(encoding="utf-8")
    for old, new in (
        # Undefined qualified requirement.
        ("requirements: [SPEC-001#REQ-002, SPEC-001#REQ-003, SPEC-001#REQ-004]",
         "requirements: [SPEC-001#REQ-002, SPEC-001#REQ-003, SPEC-001#REQ-004, SPEC-001#REQ-009]"),
        # Same-level dependency cycle with TASK-002.
        ("depends_on: []", "depends_on: [TASK-002]"),
    ):
        if body.count(old) != 1:
            raise RuntimeError(f"fixture contract changed: missing H9 anchor {old!r}")
        body = body.replace(old, new)
    first.write_text(body, encoding="utf-8")
    body = second.read_text(encoding="utf-8")
    for old, new in (
        # Missing parent.
        ("parents: [PLAN-001]", "parents: [PLAN-001, PLAN-009]"),
        # Cross-level dependency.
        ("depends_on: [TASK-001]", "depends_on: [TASK-001, PLAN-002]"),
    ):
        if body.count(old) != 1:
            raise RuntimeError(f"fixture contract changed: missing H9 anchor {old!r}")
        body = body.replace(old, new)
    second.write_text(body, encoding="utf-8")


def _prepare_h10(repo: Path, external: bool) -> tuple[Path, list[Path]]:
    base = builder.git(repo, "rev-parse", "HEAD")
    worktree = repo / ".claude" / "worktrees" / WORKTREE
    builder.git(repo, "worktree", "add", "-q", "-b", BRANCH, str(worktree))
    _apply_task_001(worktree)
    builder.git(worktree, "add", "machine_control.py", "tests/test_machine_control.py")
    builder.git(worktree, "commit", "-qm", "feat: add MachineRegistry.start")
    commit = builder.git(worktree, "rev-parse", "HEAD")
    # The user's uncommitted work in the linked worktree.
    readme = worktree / "README.md"
    readme.write_text(readme.read_text(encoding="utf-8")
                      + "\n## Notes\n\n- WIP: StartMachine client examples (not ready).\n",
                      encoding="utf-8")
    (worktree / "notes").mkdir()
    (worktree / "notes" / "start-machine.md").write_text(
        "# StartMachine scratch notes\n\n- Ask ops about audit retention.\n", encoding="utf-8")

    brain = repo / ".brain"
    (brain / FEATURE.removeprefix(".brain/") / "execution.md").write_text(_execution(
        base, BRANCH, str(worktree),
        [f"TASK-001: approved done (commit {commit})", "TASK-002: pending"],
        "TASK-002 is next.",
        [f"2026-11-14: `python -m unittest discover -s tests -v` -> OK, 9 tests at {commit}."],
        ["Checkpoint 1 (TASK-001) approved by the user on 2026-11-14; committed at the "
         "user's request."],
    ), encoding="utf-8")
    builder.write_index(brain, base)
    if not external:
        return worktree, []

    # Saved external brain; the main checkout keeps a stale, older copy.
    outside = repo.parent / f"{repo.name}-brain"
    shutil.move(str(brain), str(outside))
    stale = repo / ".brain"
    stale.mkdir()
    shutil.copytree(outside / "adrs", stale / "adrs")
    for name in ("glossary.md", "state.md"):
        shutil.copyfile(outside / name, stale / name)
    decisions = (outside / "09_user_decisions.md").read_text(encoding="utf-8")
    (stale / "09_user_decisions.md").write_text(
        decisions.replace(builder.ELIGIBILITY_DECISION, ""), encoding="utf-8")
    shutil.copytree(outside / "features" / "start-machine" / "01-brief",
                    stale / "features" / "start-machine" / "01-brief")
    builder.write_index(stale, base)
    builder.write_index(outside, base, git_line="untracked (outside the repository)")
    policy = repo / "CLAUDE.local.md"
    existing = policy.read_text(encoding="utf-8") if policy.exists() else ""
    policy.write_text(existing.rstrip("\n") + f"\n\nProject brain: {outside}\n", encoding="utf-8")
    return worktree, [outside]


def _prepare_h11(repo: Path) -> None:
    brain = repo / ".brain"
    rows = []
    for rel, text in LEGACY.items():
        path = brain / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        rows.append((rel, text.splitlines()[0].lstrip("# "), text.split("Status: ")[1].split()[0]))
    builder.write_index(brain, builder.git(repo, "rev-parse", "HEAD"), rows)


def prepare(destination: Path, scenario: str, policy: Path | None = None,
            skills_dir: Path | None = None) -> Prepared:
    stage, skill, context, trigger = SCENARIOS[scenario]
    repo = builder.build(destination, stage, policy)
    cwd = launch = repo
    worktree, add_dirs = None, []
    if scenario == "H6B":
        _prepare_h6b(repo)
    elif scenario == "H7":
        _prepare_h7(repo)
    elif scenario == "H8":
        target = repo / "machine_control.py"
        body = target.read_text(encoding="utf-8")
        anchor = 'machine.state = "stopped"'
        if body.count(anchor) != 1:
            raise RuntimeError("missing H8 StopMachine regression anchor")
        target.write_text(body.replace(anchor, 'machine.state = "idle"'), encoding="utf-8")
        builder.git(repo, "add", "machine_control.py")
        builder.git(repo, "commit", "-qm", "refactor: simplify StopMachine state handling")
    elif scenario == "H9":
        _prepare_h9(repo)
        validator = (skills_dir or builder.ROOT) / "brain-init" / "scripts" / "validate_feature_docs.py"
        trigger = trigger.format(validator=validator)
    elif scenario in ("H10A", "H10B", "H10C", "H10D"):
        cwd, add_dirs = _prepare_h10(repo, external=scenario in ("H10C", "H10D"))
        worktree = WORKTREE
    elif scenario == "H11":
        _prepare_h11(repo)
    return Prepared(scenario, repo, cwd, launch, skill, context, trigger, worktree, add_dirs)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenario", choices=sorted(SCENARIOS))
    parser.add_argument("destination", type=Path)
    parser.add_argument("--policy", type=Path, help="CLAUDE.local.md to install untracked")
    parser.add_argument("--skills-dir", type=Path, help="skill set the agent receives (H9 path)")
    parser.add_argument("--json", action="store_true", help="print machine-readable output")
    args = parser.parse_args()
    try:
        prepared = prepare(args.destination.resolve(), args.scenario, args.policy, args.skills_dir)
    except (OSError, ValueError, FileExistsError, RuntimeError) as exc:
        parser.exit(1, f"{exc}\n")
    if args.json:
        print(json.dumps({k: (str(v) if isinstance(v, Path) else
                              [str(x) for x in v] if isinstance(v, list) else v)
                          for k, v in asdict(prepared).items()}))
        return 0
    print(f"Fixture: {prepared.repo}\nAgent directory: {prepared.cwd}")
    if prepared.worktree:
        print(f"Launch: claude --worktree {prepared.worktree} (from {prepared.launch})")
    for extra in prepared.add_dirs:
        print(f"Additional directory: {extra}")
    print(f"Skill: {prepared.skill or 'none'}")
    if prepared.context:
        print(f"Context:\n{prepared.context}")
    print(f"Trigger: {prepared.trigger}")
    print("Agent run: NOT STARTED. Grading criteria remain outside the fixture.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
