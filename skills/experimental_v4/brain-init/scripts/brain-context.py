#!/usr/bin/env python3
"""Conservative, dependency-free Brain context planner.

A reviewed scope map permits omission; missing/stale evidence forces a full read.
The plan is a file list, never a substitute for source/decision verification.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import sys

VERSION = "# brain-context-map v1"
EXCLUDED_ROOT = {"README.md", "USAGE.md"}
CATALOGS = {"00_index.md", "state.md"}
MANDATORY = {"00_index.md", "01_about.md", "02_features.md",
             "03_architecture.md", "09_user_decisions.md",
             "open_questions.md", "state.md", "glossary.md"}
FEATURE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
PATH = re.compile(r"[A-Za-z0-9_./ -]+\Z")


def die(message: str) -> None:
    raise ValueError(message)


def safe_relative(text: str, *, directory: bool = False) -> str:
    value = text.replace("\\", "/")
    if not value or value.startswith("/") or "\t" in value or "\n" in value:
        die("invalid relative path")
    parts = value.rstrip("/").split("/")
    if any(part in ("", ".", "..") for part in parts):
        die("invalid relative path")
    if not PATH.fullmatch(value):
        die("unsupported relative path")
    return value.rstrip("/") + ("/" if directory and value.endswith("/") else "")


def blob(content: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()


def inventory(brain: Path) -> dict[str, bytes]:
    if not (brain / "00_index.md").is_file():
        die("brain index missing")
    docs: dict[str, bytes] = {}
    for node in brain.rglob("*"):
        if node.is_symlink():
            die("unsafe symlink in Brain: " + node.relative_to(brain).as_posix())
    for file in sorted(brain.rglob("*.md")):
        rel = file.relative_to(brain).as_posix()
        if file.is_symlink() or not file.is_file() or not file.resolve().is_relative_to(brain):
            die("unsafe Brain document: " + rel)
        if rel not in EXCLUDED_ROOT:
            docs[rel] = file.read_bytes()
    return docs


def governed(rel: str) -> bool:
    return not rel.startswith(("features/", "pending/"))


def scope_match(selectors: str, features: list[str], paths: list[str]) -> bool:
    for selector in selectors.split(";"):
        if selector.startswith("feature:"):
            if selector[8:] in features:
                return True
        elif selector.startswith("path:"):
            prefix = selector[5:]
            for candidate in paths:
                if candidate == prefix.rstrip("/") or (
                    prefix.endswith("/") and candidate.startswith(prefix)
                ):
                    return True
    return False


def parse_map(brain: Path, docs: dict[str, bytes]) -> tuple[dict[str, tuple[str, str]], str]:
    location = brain / "context-map.tsv"
    if not location.is_file():
        return {}, "missing-map"
    lines = location.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != VERSION:
        return {}, "invalid-map-header"
    mapping: dict[str, tuple[str, str]] = {}
    for line in lines[1:]:
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) != 4:
            return {}, "invalid-map-row"
        rel, mode, selectors, fingerprint = fields
        try:
            if safe_relative(rel) != rel:
                raise ValueError()
        except ValueError:
            return {}, "invalid-map-path"
        if rel in mapping:
            return {}, "duplicate-map-path"
        if mode == "global":
            if selectors != "-":
                return {}, "invalid-global-selector"
        elif mode == "scoped":
            if not selectors or selectors == "-":
                return {}, "invalid-scope"
            for selector in selectors.split(";"):
                if selector.startswith("feature:") and FEATURE.fullmatch(selector[8:]):
                    continue
                if selector.startswith("path:"):
                    try:
                        if safe_relative(selector[5:], directory=True) == selector[5:]:
                            continue
                    except ValueError:
                        pass
                return {}, "invalid-scope"
        else:
            return {}, "invalid-map-mode"
        if not re.fullmatch(r"[0-9a-f]{40}", fingerprint):
            return {}, "invalid-map-hash"
        if rel not in docs or blob(docs[rel]) != fingerprint:
            return {}, "stale-map"
        mapping[rel] = (mode, selectors)
    if set(mapping) != {name for name in docs if governed(name)}:
        return {}, "incomplete-map"
    return mapping, ""


def plan(brain: Path, docs: dict[str, bytes], features: list[str],
         paths: list[str], branch: str | None) -> tuple[str, str, list[str]]:
    mapping, reason = parse_map(brain, docs)
    active_pending = "pending/" + branch.replace("/", "--") + ".md" if branch else None
    full_docs = sorted(name for name in docs
                       if not name.startswith("pending/") or name == active_pending)
    scoped = bool(features or paths)
    if not scoped:
        reason = reason or "unknown-scope"
    if not branch:
        reason = reason or "unknown-branch"
    if reason:
        return "full", reason, full_docs

    selected = {name for name in docs if name in MANDATORY}
    if branch:
        pending = "pending/" + branch.replace("/", "--") + ".md"
        if pending in docs:
            selected.add(pending)
    for feature in features:
        selected.update(name for name in docs if name.startswith("features/" + feature + "/"))

    matched = False
    for name, (mode, selectors) in mapping.items():
        if mode == "global":
            selected.add(name)
        elif scope_match(selectors, features, paths):
            selected.add(name)
            matched = True

    # No proven ownership for a code path or a feature outside the active feature tree.
    # A matching feature selector cannot compensate for an uncovered code path.
    for candidate in paths:
        if not any(mode == "scoped" and scope_match(selectors, [], [candidate])
                   for mode, selectors in mapping.values()):
            return "full", "unmapped-code-path", full_docs
    for feature in features:
        if not any(name.startswith("features/" + feature + "/") for name in docs) and not any(
            mode == "scoped" and scope_match(selectors, [feature], [])
            for mode, selectors in mapping.values()
        ):
            return "full", "unmapped-feature", full_docs

    # Extra safety net: inspect text of *all* documents without feeding it to the AI.
    # Include a document that mentions an affected source or feature path, even
    # when its declared scope is narrower. This can only add, never remove, context.
    probes = list(paths) + ["features/" + feature + "/" for feature in features]
    for name, content in docs.items():
        if name.startswith("pending/") and name not in selected:
            continue
        if any(probe in content.decode("utf-8", errors="replace") for probe in probes):
            selected.add(name)

    # Follow both forward and reverse explicit file references transitively.
    # Existing source maps and knowledge documents commonly link to one another.
    changed = True
    while changed:
        changed = False
        for name, content in docs.items():
            if name.startswith("pending/") and name not in selected:
                continue
            text = content.decode("utf-8", errors="replace")
            for other in docs:
                if other == name or (other.startswith("pending/") and other not in selected):
                    continue
                if name not in CATALOGS and other not in CATALOGS and (
                    (other in text or other.rsplit("/", 1)[-1] in text)
                    and (name in selected or other in selected)
                ):
                    if name not in selected or other not in selected:
                        selected.update((name, other))
                        changed = True
    return "selective", "mapped-and-linked", sorted(selected)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("plan", "map"))
    parser.add_argument("--brain", required=True)
    parser.add_argument("--branch")
    parser.add_argument("--feature", action="append", default=[])
    parser.add_argument("--path", action="append", default=[])
    args = parser.parse_args()

    brain = Path(args.brain).expanduser().resolve()
    features = args.feature
    for feature in features:
        if not FEATURE.fullmatch(feature):
            die("invalid feature slug")
    paths = [safe_relative(item, directory=True) for item in args.path]
    if args.branch and (args.branch.startswith("/") or ".." in args.branch or not
                        re.fullmatch(r"[A-Za-z0-9._/-]+", args.branch)):
        die("invalid branch")
    docs = inventory(brain)

    if args.action == "map":
        print(VERSION)
        print("# Review scope declarations before using selective loading.")
        for name, content in docs.items():
            if governed(name):
                print(f"{name}\tglobal\t-\t{blob(content)}")
        return

    mode, reason, selected = plan(brain, docs, features, paths, args.branch)
    print("MODE\t" + mode)
    print("REASON\t" + reason)
    for name in selected:
        print("READ\t" + name)
    total = sum(len(value) for value in docs.values())
    amount = sum(len(docs[name]) for name in selected)
    print(f"BYTES\t{amount}\t{total}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as exc:
        print("ERROR " + str(exc), file=sys.stderr)
        sys.exit(1)
