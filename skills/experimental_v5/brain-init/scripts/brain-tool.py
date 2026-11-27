#!/usr/bin/env python3
"""Dependency-free, deterministic Brain operations. No operation grants approval."""
from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import hashlib
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
    boolean = {"apply", "check-coverage", "pending", "estimate", "hashes", "save-location"}
    values = {"brain", "repo", "tracking", "revision", "at", "main-branch",
              "feature", "kind", "slug", "authorized-root", "affected",
              "show-parent-hashes", "since", "event", "detail", "branch",
              "report-type", "select"}
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
            elif key in values:
                if i + 1 >= len(argv) or argv[i + 1].startswith("--"):
                    raise Problem(f"missing value for --{key}")
                options[key] = argv[i + 1]
                i += 1
            else:
                raise Problem(f"unknown option: --{key}")
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
    items = []
    for filename, _ in guide_rows:
        target = brain / filename
        bundled = (REFS / filename).read_text()
        if target.exists() and target.read_text() != bundled:
            print(f"REVIEW existing {target}: differs from bundled guide; preserved")
        else:
            items.append((target, bundled))
    if not existing.is_file() or index != existing.read_text():
        if existing.is_file():
            # Existing index edits require a separate command or human review.
            if options.get("apply"):
                raise Problem("index needs new guide rows; review update before applying")
            print("REVIEW index guide registration (existing index differs)")
        else:
            items.insert(0, (existing, index))
    policy = repo / "CLAUDE.local.md"
    policy_append = None
    bundled_policy = (REFS / "CLAUDE.local.md").read_text()
    saved_location = f"Project brain: {brain}"
    if policy.exists():
        existing_policy = policy.read_text()
        if existing_policy != bundled_policy:
            print("REVIEW existing CLAUDE.local.md; preserve custom policy")
        if options.get("save-location"):
            present = re.findall(r"(?m)^Project brain:.*$", existing_policy)
            if len(present) > 1 or (present and present[0] != saved_location):
                raise Problem("conflicting saved Project brain location; review before applying")
            if not present:
                policy_append = ("\n" if existing_policy and not existing_policy.endswith("\n") else "") + saved_location + "\n"
                if options.get("apply"):
                    in_scope(policy, options)
                else:
                    print(f"APPEND {policy}: Project brain location (dry-run)")
    else:
        content = bundled_policy
        if options.get("save-location"):
            content += ("" if content.endswith("\n") else "\n") + saved_location + "\n"
        items.append((policy, content))
    exclude_entries = []
    def git_succeeds(*args: str) -> bool:
        return subprocess.run(["git", "-C", str(repo), *args],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                              check=False).returncode == 0
    if mode == "ignored" and brain == repo / ".brain" and not git_succeeds(
            "check-ignore", "-q", "--", ".brain/"):
        exclude_entries.append(".brain/")
    if not git_succeeds("ls-files", "--error-unmatch", "--", "CLAUDE.local.md") and not git_succeeds(
            "check-ignore", "-q", "--", "CLAUDE.local.md"):
        exclude_entries.append("CLAUDE.local.md")
    exclusion = None
    if exclude_entries and options.get("apply"):
        common = path(git(repo, "rev-parse", "--path-format=absolute", "--git-common-dir"))
        exclusion = common / "info" / "exclude"
        in_scope(exclusion, options)
    changes(items, options)
    if policy_append is not None and options.get("apply"):
        with policy.open("a", encoding="utf-8") as stream:
            stream.write(policy_append)
        print(f"UPDATED {policy}: Project brain location")
    if exclusion is not None:
        content = exclusion.read_text() if exclusion.exists() else ""
        missing = [entry for entry in exclude_entries if entry not in content.splitlines()]
        if missing:
            exclusion.parent.mkdir(parents=True, exist_ok=True)
            with exclusion.open("a", encoding="utf-8") as stream:
                stream.write(("" if not content or content.endswith("\n") else "\n") +
                             "".join(f"{entry}\n" for entry in missing))
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
        "parents": "[" + ", ".join(parents) + "]",
        "requirements": "[]",
        "depends_on": "[]",
    }
    for key, value in replacements.items():
        body = re.sub(rf"(?m)^{key}:.*$", lambda _: f"{key}: {value}", body, count=1)
    # Illustrative IDs/examples in the reference are not real requirements.
    if kind == "specification":
        body = re.sub(r"(?m)^- (?:REQ-\d{3}|E\d+):.*\n", "", body)
    body = re.sub(r"<Feature(?: area)?>", feature.replace("-", " ").title(), body)
    return body.rstrip() + "\n"


def scaffold(options: dict, kind: str, brain: Path, feature: str, name: str) -> None:
    root = Path(__file__).resolve().parent / "scaffolds"
    title = name.replace("-", " ").title()
    if kind == "execution":
        target = brain / "features" / feature / "execution.md"
    elif kind == "planning-index":
        target = brain / "planning" / feature / "INDEX.md"
    elif kind == "planning-ticket":
        folder = brain / "planning" / feature
        numbers = [int(m.group(1)) for p in folder.glob("*.md")
                   if (m := re.match(r"^(\d+)-.+\.md$", p.name))]
        target = folder / f"{max(numbers, default=0)+1:03d}-{name}.md"
    elif kind == "diagnosis":
        folder = brain / "diagnoses"
        numbers = [int(m.group(1)) for p in folder.glob("*.md")
                   if (m := re.match(r"^(\d+)-.+\.md$", p.name))]
        target = folder / f"{max(numbers, default=0)+1:02d}-{name}.md"
    elif kind == "review":
        review_type = str(options.get("report-type", ""))
        if review_type not in ("architecture", "code", "merge-request", "security"):
            raise Problem("--report-type is required: architecture, code, merge-request, or security")
        folder = brain / "reviews" / review_type
        numbers = [int(m.group(1)) for p in folder.iterdir()
                   if (m := re.match(r"^(\d+)-.+(?:\.md)?$", p.name))] if folder.is_dir() else []
        target = folder / f"{max(numbers, default=0)+1:02d}-{name}" / "review.md"
    else:
        raise Problem(f"unsupported scaffold kind: {kind}")
    if target.exists():
        raise Problem(f"existing document; refusing overwrite: {target}")
    filename = ("review" if kind == "review" else kind) + ".md"
    content = (root / filename).read_text(encoding="utf-8").replace("{{TITLE}}", title)
    changes([(target, content)], options)


def doc(options: dict) -> None:
    brain = brain_path(options)
    feature = slug(required(options, "feature"))
    kind = required(options, "kind")
    name = slug(str(options.get("slug") or feature))
    if kind not in KINDS:
        scaffold(options, kind, brain, feature, name)
        return
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
    if options.get("pending"):
        brain = brain_path(options)
        branch = str(options.get("branch") or git(repo, "branch", "--show-current"))
        if not branch or not re.fullmatch(r"[A-Za-z0-9._/-]+", branch) or ".." in branch:
            raise Problem("invalid branch for pending")
        mapped = branch.replace("/", "--")
        target = brain / "pending" / (mapped + ".md")
        if target.exists():
            current = target.read_text()
            if not re.search(r"(?m)^Branch: " + re.escape(branch) + r"$", current):
                raise Problem(f"pending filename collision: {target}")
            print(f"UNCHANGED {target}")
            return
        date = str(options.get("at") or dt.datetime.now(dt.timezone.utc).date())
        content = (Path(__file__).resolve().parent / "scaffolds/pending.md").read_text()
        changes([(target, content.replace("{{BRANCH}}", branch).replace("{{DATE}}", date))], options)
        return
    print("BRANCH " + git(repo, "branch", "--show-current"))
    print("HEAD " + git(repo, "rev-parse", "HEAD"))
    # Exclude private notes from all Git inventories, including tracked changes.
    excluded = ("--", ".", ":(exclude).brain/.notes/**")
    for label, args in (
        ("STATUS", ("status", "--porcelain", "--untracked-files=all")),
        ("STAGED", ("diff", "--cached", "--name-status")),
        ("UNSTAGED", ("diff", "--name-status")),
    ):
        for line in git(repo, *args, *excluded).splitlines():
            print(f"{label} {line}")
    if options.get("since"):
        since = str(options["since"])
        git(repo, "cat-file", "-e", since + "^{commit}")
        for line in git(repo, "diff", "--name-status", since, "HEAD", *excluded).splitlines():
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
    if not options.get("apply"):
        print(f"APPEND {target} (dry-run)")
        return
    in_scope(target, options)
    with target.open("a", encoding="utf-8") as f:
        f.write(("\n" if not text.endswith("\n") else "") + entry)
    print(f"APPENDED {target}")


def context(options: dict) -> None:
    brain = brain_path(options)
    if not (brain / "00_index.md").is_file():
        raise Problem(f"not a Brain: {brain}")
    if options.get("select"):
        name = str(options["select"])
        rel = Path(name)
        if rel.is_absolute() or ".." in rel.parts or (rel.parts and rel.parts[0] == ".notes"):
            raise Problem("invalid context selection")
        target = (brain / rel).resolve()
        try:
            target.relative_to(brain.resolve())
        except ValueError as exc:
            raise Problem("context selection escapes Brain") from exc
        if not target.is_file():
            raise Problem(f"context document missing: {name}")
        print(target.read_text(encoding="utf-8"), end="")
        return
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
    total = 0
    for file in sorted(set(files)):
        content = file.read_bytes()
        total += len(content)
        status = re.search(rb"(?m)^status:\s*(\S+)", content)
        extra = ""
        if options.get("hashes"):
            prefix = f"blob {len(content)}\0".encode()
            extra = "\t" + hashlib.sha1(prefix + content).hexdigest()
        print(f"DOC {file.relative_to(brain)}\t{len(content)}\t"
              f"{status.group(1).decode() if status else '-'}{extra}")
    if options.get("estimate"):
        print(f"ESTIMATE bytes={total} tokens~={(total+3)//4} (approximate)")


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
