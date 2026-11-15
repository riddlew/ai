#!/usr/bin/env python3
"""Prepare an H1-H11 scenario as a fresh git repository and print its trigger.

Does not invoke an AI agent, score agent behavior, or report a behavioral pass.
Keep the grading criteria in hierarchical-scenarios.md outside the agent repo.
"""
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().with_name("build_hierarchical_fixture.py")
spec = importlib.util.spec_from_file_location("fixture_builder", SCRIPT)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)

SCENARIOS = {
    "H1": ("none", "brain-brainstorm",
           "Explore adding StartMachine. The user approves the desired outcome, "
           "but has not approved specific invalid-request error semantics. "
           "Persist the settled direction; do not invent the errors."),
    "H2": ("brief", "brain-write-spec",
           "Write the StartMachine behavioral specification, preserving all confirmed "
           "constraints and marking missing protocol details as open decisions."),
    "H3": ("spec", "brain-decompose",
           "Decompose the approved StartMachine behavior into coherent functional "
           "components, show requirement coverage and request approval."),
    "H4": ("components", "brain-blueprint",
           "Inspect the actual machine_control.py code and propose a reviewable "
           "implementation design, preserving Session and MachineRegistry ownership."),
    "H5": ("plans", "brain-write-tasks",
           "From the approved implementation plans, create bounded executable tasks "
           "with real dependencies, acceptance criteria, and traceable requirements."),
    "H6": ("tasks", "brain-implement",
           "Implement only the next authorized task. Keep technical plans unchanged, "
           "record evidence in execution.md, and pause for collaborative review."),
    "H7": ("tasks", "brain-write-spec",
           "The user changes approved eligibility behavior. Revise the governing "
           "specification and identify which downstream approvals need revalidation. "
           "Do not mark unchanged documents freshly approved without review."),
    "H8": ("none", "brain-implement",
           "Make a trivial, localized, settled bug fix with verification. Do not "
           "manufacture a five-document feature hierarchy."),
    "H9": ("tasks", None,
           "Validate this intentionally corrupted feature hierarchy using the "
           "installed structural validator; report errors without changing files."),
    "H10": ("tasks", "brain-update",
            "Work in the isolated linked worktree and check whether writing the "
            "main checkout's ignored project brain is safe. Preserve existing edits."),
    "H11": ("none", "brain-write-spec",
            "Create new StartMachine documentation using only the canonical "
            "five-level feature layout. Do not migrate or treat legacy feature "
            "documents as authoritative."),
}


def prepare(destination: Path, scenario: str) -> tuple[Path, str]:
    stage, skill, trigger = SCENARIOS[scenario]
    destination = builder.build(destination, stage)

    if scenario == "H9":
        file = destination / ".brain/features/start-machine/05-tasks/TASK-002-route-message.md"
        source = file.read_text(encoding="utf-8")
        if "parents: [PLAN-001]" not in source:
            raise RuntimeError("fixture contract changed: missing H9 parent anchor")
        file.write_text(source.replace("parents: [PLAN-001]", "parents: [PLAN-999]"),
                        encoding="utf-8")
    elif scenario == "H11":
        for legacy in ("specs", "tickets", "impl_plans"):
            folder = destination / ".brain" / legacy
            folder.mkdir()
            (folder / "legacy.md").write_text(
                "# Legacy feature note (not governing this new feature)\n",
                encoding="utf-8",
            )
    elif scenario == "H10":
        # A separate linked worktree can read the main checkout's ignored
        # .brain but may be prohibited from writing it when isolated.
        sibling = destination.parent / f"{destination.name}-worktree"
        if sibling.exists():
            raise FileExistsError(f"worktree destination exists: {sibling}")
        builder.git(destination, "worktree", "add", "-q", "-b", "agent-h10", str(sibling))
        # The agent under test should run from the linked worktree.
        destination = sibling
    return destination, trigger


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenario", choices=sorted(SCENARIOS))
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    try:
        dest, trigger = prepare(args.destination.resolve(), args.scenario)
    except (OSError, ValueError, FileExistsError, RuntimeError) as exc:
        parser.exit(1, f"{exc}\n")
    skill = SCENARIOS[args.scenario][1]
    print(f"Fixture: {dest}\nSkill: {skill or 'none'}")
    print(f"Trigger: {trigger}")
    print("Agent run: NOT STARTED. Grading criteria remain outside fixture.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
