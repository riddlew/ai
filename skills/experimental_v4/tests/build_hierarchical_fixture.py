#!/usr/bin/env python3
"""Build an isolated, reproducible repository for H1–H8 agent scenarios.

Creates a fresh repository with committed baseline code, ignored .brain/
documents, and approved feature stages. Does not run or grade any AI agent.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "tests" / "fixture" / "start-machine-app"
DOCS = ROOT / "tests" / "fixture" / "hierarchical-brain" / ".brain" / "features" / "start-machine"
LAYERS = (
    "01-brief", "02-specifications", "03-components",
    "04-implementation-plans", "05-tasks",
)
STAGES = ("none", "brief", "spec", "components", "plans", "tasks")


def git(path: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(path), *args],
                            check=True, capture_output=True, text=True)
    return result.stdout.strip()


def build(destination: Path, stage: str = "none") -> Path:
    if stage not in STAGES:
        raise ValueError(f"invalid stage {stage!r}; choose from {STAGES}")
    if destination.exists():
        raise FileExistsError(f"refusing to overwrite existing fixture {destination}")
    shutil.copytree(APP, destination)
    (destination / "CLAUDE.local.md").write_text(
        (ROOT / "brain-init" / "references" / "CLAUDE.local.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    git(destination, "init", "-q", "-b", "main")
    git(destination, "config", "user.name", "Brain Fixture")
    git(destination, "config", "user.email", "fixture@example.invalid")
    git(destination, "add", "machine_control.py", "tests", "README.md", "CLAUDE.local.md")
    git(destination, "commit", "-qm", "test: baseline machine-control behavior")
    revision = git(destination, "rev-parse", "HEAD")
    exclude = destination / ".git" / "info" / "exclude"
    with exclude.open("a", encoding="utf-8") as f:
        f.write("\n.brain/\n")
    brain = destination / ".brain"
    brain.mkdir()
    (brain / "00_index.md").write_text(
        f"# Brain index\nGit: ignored\nMain branch: main\nLast synced: {revision}\n"
        "\n## Documents\n| Path | Purpose | Status |\n|---|---|---|\n",
        encoding="utf-8",
    )
    (brain / "glossary.md").write_text(
        "# Glossary\n\n- Session: existing message dispatcher\n"
        "- MachineRegistry: existing owner of machine state changes\n",
        encoding="utf-8",
    )
    (brain / "09_user_decisions.md").write_text(
        "# User decisions\n\n- Existing Session retains routing and connection ownership.\n",
        encoding="utf-8",
    )
    count = STAGES.index(stage)
    if count:
        feature = brain / "features" / "start-machine"
        for layer in LAYERS[:count]:
            shutil.copytree(DOCS / layer, feature / layer)
        if stage == "tasks":
            shutil.copyfile(DOCS / "execution.md", feature / "execution.md")
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path, help="new empty destination (must not exist)")
    parser.add_argument("--stage", choices=STAGES, default="none",
                        help="highest preapproved document layer to copy")
    args = parser.parse_args()
    try:
        built = build(args.destination.resolve(), args.stage)
    except (FileExistsError, ValueError, OSError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"{exc}\n")
    print(f"Fixture ready: {built}; stage={args.stage}; no agent run")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
