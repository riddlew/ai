#!/usr/bin/env python3
"""Dependency-free, deterministic Brain operations. No operation grants approval."""
from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import os
from pathlib import Path
import re
import subprocess
import sys

VERSION = "1"
KINDS = {
    "brief": ("01", "01-brief", "BRF", "brief"),
    "specification": ("02", "02-specifications", "SPEC", "specification"),
    "component": ("03", "03-components", "CMP", "component"),
    "plan": ("04", "04-implementation-plans", "PLAN", "implementation-plan"),
    "task": ("05", "05-tasks", "TASK", "task"),
}
REFS = Path(__file__).resolve().parent.parent / "references"
SKILLS = Path(__file__).resolve().parents[2]


class Problem(Exception):
    pass


def opt(argv: list[str]) -> tuple[list[str], dict[str, object]]:
    pos: list[str] = []
    options: dict[str, object] = {"parent": []}
    boolean = {"apply", "check-coverage", "save-location"}
    i = 0
    while i < len(argv):
        token = argv[i]
        if token.startswith("--"):
            key = token[2:]
            if key in boolean:
                options[key] = True
            elif key == "parent":
                if i + 1 >= len(argv):
                    raise Problem(f"missing value for --{key}")
                options["parent"].append(argv[i + 1])
                i += 1
            else:
                if i + 1 >= len(argv) or argv[i + 1].startswith("--"):
                    raise Problem(f"missing value for --{key}")
                options[key] = argv[i + 1]
                i += 1
        else:
            pos.append(token)
        i += 1
    return pos, options


def required(options: dict, key: str) -> str:
    value = options.get(key)
    if not value or not isinstance(value, str):
        raise Problem(f"--{key} is required")
    return value


def slug(value: str) -> str:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value):
        raise Problem(f"invalid slug: {value!r}")
    return value


def path(value: str) -> Path:
    return Path(value).expanduser().resolve()


def in_scope(destination: Path, options: dict) -> None:
    root = options.get("authorized-root")
    if not root:
        raise Problem("--authorized-root is required for --apply")
    dest = destination.resolve()
    try:
        dest.relative_to(path(str(root)))
    except ValueError as exc:
        raise Problem(f"outside authorized write root: {destination}") from exc


def changes(items: list[tuple[Path, str]], options: dict) -> None:
    """Preflight the whole change set; never replace differing files."""
    for target, text in items:
        if options.get("apply"):
            in_scope(target, options)
        if target.exists() and (not target.is_file() or target.read_text() != text):
            raise Problem(f"existing content differs: {target}")
    for target, text in items:
        if target.exists():
            print(f"UNCHANGED {target}")
        elif not options.get("apply"):
            print(f"CREATE {target} (dry-run)")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            try:
                with target.open("x", encoding="utf-8", newline="\n") as f:
                    f.write(text)
            except FileExistsError as exc:
                raise Problem(f"concurrent creation: {target}") from exc
            print(f"CREATED {target}")


def git(repo: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(["git", "-C", str(repo), *args],
                            capture_output=True, text=True, check=False)
    if check and result.returncode:
        raise Problem(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def brain_path(options: dict) -> Path:
    value = required(options, "brain")
    result = path(value)
    if result.name != ".brain" and not (result / "00_index.md").is_file():
        # Explicit path is authoritative; no implicit second brain is created.
        return result
    return result


def init(options: dict) -> None:
    brain = brain_path(options)
    repo = path(str(options.get("repo", ".")))
    mode = str(options.get("tracking", "ignored"))
    if mode not in ("ignored", "tracked"):
        raise Problem("--tracking must be ignored or tracked")
    existing = brain / "00_index.md"
    if existing.is_file():
        index = existing.read_text()
    else:
        date = str(options.get("at") or dt.datetime.now(dt.timezone.utc).date())
        sha = str(options.get("revision") or git(repo, "rev-parse", "HEAD"))
        main = str(options.get("main-branch") or "main")
        index = (
            "# Project Brain Index\n\n"
            f"Last synced: {sha} ({date})\nGit: {mode}\nMain branch: {main}\n\n"
            "## Root files\n\n| File | Purpose | Status |\n|---|---|---|\n\n"
            "## Documents\n\n| Path | Purpose | Status |\n|---|---|---|\n"
        )
    guide_rows = [
        ("USAGE.md", "Brain Skills workflow examples and selection guide"),
        ("README.md", "Brain Skills catalog and installation reference"),
    ]
    for filename, purpose in guide_rows:
        if not re.search(r"(?m)^\|\s*\`?" + re.escape(filename) + r"\`?\s*\|", index):
            index += f"| `{filename}` | {purpose} | reference |\n"
    items = [(brain / file, (REFS / file).read_text())
             for file, _ in guide_rows]
    if not existing.is_file() or index != existing.read_text():
        if existing.is_file():
            # Existing index edits require a separate command or human review.
            if options.get("apply"):
                raise Problem("index needs new guide rows; review update before applying")
            print("REVIEW index guide registration (existing index differs)")
        else:
            items.insert(0, (existing, index))
    policy = repo / "CLAUDE.local.md"
    if policy.exists():
        if policy.read_text() != (REFS / "CLAUDE.local.md").read_text():
            print("REVIEW existing CLAUDE.local.md; preserve custom policy")
    else:
        items.append((policy, (REFS / "CLAUDE.local.md").read_text()))
    changes(items, options)
    if mode == "ignored" and options.get("apply"):
        common = path(git(repo, "rev-parse", "--path-format=absolute", "--git-common-dir"))
        exclusion = common / "info" / "exclude"
        in_scope(exclusion, options)
        content = exclusion.read_text() if exclusion.exists() else ""
        if ".brain/" not in content.splitlines():
            exclusion.parent.mkdir(parents=True, exist_ok=True)
            with exclusion.open("a", encoding="utf-8") as f:
                f.write(("" if not content or content.endswith("\n") else "\n") + ".brain/\n")
            print(f"UPDATED {exclusion}")


def template(kind: str, doc_id: str, parents: list[str], feature: str) -> str:
    level, _, _, _ = KINDS[kind]
    raw = (REFS / "feature-document-templates.md").read_text()
    match = re.search(rf"(?ms)^## {level} .+?\n.*?^" + r"\`\`\`markdown\n(.*?)^\`\`\`", raw)
    if not match:
        raise Problem(f"missing canonical template for {kind}")
    body = match.group(1)
    replacements = {
        "id": doc_id,
        "status": "draft",
        "parents": "[" + ", ".join(parents) + "]",
        "requirements": "[]",
        "depends_on": "[]",
        "parent_hashes": "[]",
    }
    for key, value in replacements.items():
        body = re.sub(rf"(?m)^{key}:.*$", lambda _: f"{key}: {value}", body, count=1)
    # Illustrative IDs/examples in the reference are not real requirements.
    if kind == "specification":
        body = re.sub(r"(?m)^- (?:REQ-\d{3}|E\d+):.*\n", "", body)
    body = re.sub(r"<Feature(?: area)?>", feature.replace("-", " ").title(), body)
    return body.rstrip() + "\n"


def doc(options: dict) -> None:
    brain = brain_path(options)
    feature = slug(required(options, "feature"))
    kind = required(options, "kind")
    if kind not in KINDS:
        raise Problem(f"unknown document kind: {kind}")
    name = slug(str(options.get("slug") or feature))
    area = brain / "features" / feature
    ids: set[str] = set()
    by_id: dict[str, int] = {}
    for level, folder, prefix, _ in KINDS.values():
        for candidate in (area / folder).glob("*.md"):
            match = re.search(r"(?m)^id:\s*((?:BRF|SPEC|CMP|PLAN|TASK)-\d{3})\s*$",
                              candidate.read_text())
            if match:
                if match.group(1) in ids:
                    raise Problem(f"duplicate existing ID: {match.group(1)}")
                ids.add(match.group(1))
                by_id[match.group(1)] = int(level)
    level, folder, prefix, _ = KINDS[kind]
    parents: list[str] = list(options.get("parent") or [])
    if len(parents) != len(set(parents)):
        raise Problem("duplicate parent ID")
    if kind == "brief" and parents:
        raise Problem("brief cannot have parents")
    if kind not in ("brief", "specification") and not parents:
        raise Problem("this document needs at least one governing --parent")
    for parent in parents:
        if parent not in by_id or by_id[parent] >= int(level):
            raise Problem(f"unknown or invalid earlier-level parent: {parent}")
    numbers = [int(i.split("-")[1]) for i in ids if i.startswith(prefix + "-")]
    next_id = max(numbers, default=0) + 1
    if next_id > 999:
        raise Problem(f"exhausted {prefix} IDs")
    doc_id = f"{prefix}-{next_id:03d}"
    filename = "brief.md" if kind == "brief" else f"{doc_id}-{name}.md" if kind == "task" else f"{name}.md"
    target = area / folder / filename
    if target.exists():
        raise Problem(f"existing document; preserve its ID: {target}")
    changes([(target, template(kind, doc_id, parents, feature))], options)


def load_validator():
    source = Path(__file__).resolve().parent / "validate_feature_docs.py"
    spec = importlib.util.spec_from_file_location("brain_feature_validator", source)
    if spec is None or spec.loader is None:
        raise Problem("existing feature validator not found")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate(options: dict) -> None:
    validator = load_validator()
    if "show-parent-hashes" in options:
        file = path(str(options["show-parent-hashes"]))
        values = validator.describe_parent_hashes(file)
        print("parent_hashes: [" + ", ".join(values) + "]")
        return
    feature_root = brain_path(options) / "features"
    if "affected" in options:
        ident = str(options["affected"])
        docs = {}
        for feature in feature_root.iterdir() if feature_root.is_dir() else ():
            for folder in validator.LEVELS:
                for file in (feature / folder).glob("*.md"):
                    meta, _ = validator.parse_document(file)
                    docs[(feature.name, meta["id"])] = (file, meta)
        seeds = [x for x in docs if x[1] == ident]
        if len(seeds) != 1:
            raise Problem(f"ID not unique or unknown: {ident}")
        affected = set(seeds)
        while True:
            next_set = affected | {
                key for key, (_, meta) in docs.items()
                if key not in affected
                and any((key[0], parent) in affected
                        for parent in meta["parents"] + meta["depends_on"])
            }
            if next_set == affected:
                break
            affected = next_set
        for key in sorted(affected - set(seeds)):
            print(f"AFFECTED {key[1]} {docs[key][0]}")
        return
    errors = validator.validate_features(feature_root, bool(options.get("check-coverage")))
    if errors:
        for error in errors:
            print(f"INVALID {error}")
        raise Problem(f"{len(errors)} feature-document error(s)")
    print("VALID feature documents")


def git_state(options: dict) -> None:
    repo = path(str(options.get("repo", ".")))
    print("BRANCH " + git(repo, "branch", "--show-current"))
    print("HEAD " + git(repo, "rev-parse", "HEAD"))
    for label, args in (
        ("STATUS", ("status", "--porcelain", "--untracked-files=all")),
        ("STAGED", ("diff", "--cached", "--name-status")),
        ("UNSTAGED", ("diff", "--name-status")),
    ):
        for line in git(repo, *args).splitlines():
            print(f"{label} {line}")
    if options.get("since"):
        since = str(options["since"])
        git(repo, "cat-file", "-e", since + "^{commit}")
        for line in git(repo, "diff", "--name-status", since, "HEAD").splitlines():
            print(f"COMMITTED {line}")


def record(options: dict) -> None:
    brain = brain_path(options)
    feature = slug(required(options, "feature"))
    target = brain / "features" / feature / "execution.md"
    if not target.is_file():
        raise Problem(f"execution.md does not exist; initialize through brain-implement first: {target}")
    event = required(options, "event")
    detail = required(options, "detail")
    if not re.fullmatch(r"[a-z0-9-]+", event) or "\n" in detail:
        raise Problem("event must be a slug and detail must be one line")
    entry = f"- {event}: {detail}\n"
    text = target.read_text()
    if entry in text.split("## Checkpoints")[-1]:
        print(f"UNCHANGED {target}")
        return
    if "## Checkpoints" not in text:
        raise Problem("execution record has no ## Checkpoints heading")
    in_scope(target, options)
    if not options.get("apply"):
        print(f"APPEND {target} (dry-run)")
        return
    with target.open("a", encoding="utf-8") as f:
        f.write(("\n" if not text.endswith("\n") else "") + entry)
    print(f"APPENDED {target}")


def context(options: dict) -> None:
    brain = brain_path(options)
    if not (brain / "00_index.md").is_file():
        raise Problem(f"not a Brain: {brain}")
    files = [f for f in brain.glob("*.md") if f.name not in ("README.md", "USAGE.md")]
    if options.get("branch"):
        branch = str(options["branch"]).replace("/", "--")
        if not re.fullmatch(r"[A-Za-z0-9._-]+", branch) or ".." in branch:
            raise Problem("invalid branch name")
        item = brain / "pending" / f"{branch}.md"
        if item.is_file():
            files.append(item)
    if options.get("feature"):
        feature = slug(str(options["feature"]))
        files += list((brain / "features" / feature).rglob("*.md"))
    for file in sorted(set(files)):
        content = file.read_text()
        status = re.search(r"(?m)^status:\s*(\S+)", content)
        print(f"DOC {file.relative_to(brain)}\t{len(content.encode('utf-8'))}\t"
              f"{status.group(1) if status else '-'}")


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in ("--help", "-h"):
        print("brain-tool <init|doc|validate|git|record|context> [options]; "
              "writes require --apply --authorized-root PATH")
        return 0
    family = args.pop(0)
    if args and args[0] in ("new", "summary", "list"):
        args.pop(0)
    try:
        _, opts = opt(args)
        commands = {
            "init": init, "doc": doc, "validate": validate,
            "git": git_state, "record": record, "context": context,
        }
        if family not in commands:
            raise Problem(f"unknown command: {family}")
        commands[family](opts)
        return 0
    except (Problem, OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
