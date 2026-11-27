#!/usr/bin/env python3
"""V5 feature document validator: references and amendments, never approval gates."""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path
import re
import sys

LEVELS = {
    "01-brief": ("brief", "BRF", 1),
    "02-specifications": ("specification", "SPEC", 2),
    "03-components": ("component", "CMP", 3),
    "04-implementation-plans": ("implementation-plan", "PLAN", 4),
    "05-tasks": ("task", "TASK", 5),
}
SEQUENCES = {"parents", "requirements", "depends_on", "amends", "supersedes", "parent_hashes"}
REQUIRED = {"id", "kind", "parents", "requirements", "depends_on"}
DECLARED_REQUIREMENT = re.compile(r"^\s*[-*]\s*(REQ-\d{3}):", re.M)
REQUIREMENT = re.compile(r"^(SPEC-\d{3})#(REQ-\d{3})$")
DOCUMENT_ID = re.compile(r"^(?:BRF|SPEC|CMP|PLAN|TASK)-\d{3}$")
DECISION_REF = re.compile(r"^((?:BRF|SPEC|CMP|PLAN|TASK)-\d{3})#([A-Za-z][A-Za-z0-9_-]*)$")

def parse_document(path: Path) -> tuple[dict, str]:
    source = path.read_text(encoding="utf-8")
    if not source.startswith("---\n"):
        raise ValueError("missing opening frontmatter")
    boundary = source.find("\n---", 4)
    if boundary < 0:
        raise ValueError("unterminated frontmatter")
    meta: dict = {}
    current = None
    for line in source[4:boundary].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - ") and current:
            meta[current].append(line[4:].strip().strip("'\""))
            continue
        match = re.fullmatch(r"([a-z_]+):\s*(.*)", line)
        if not match:
            raise ValueError(f"unsupported metadata line: {line}")
        key, value = match.groups()
        if key in meta:
            raise ValueError(f"duplicate metadata key: {key}")
        if key in SEQUENCES:
            if value == "" or value == "[]":
                meta[key] = []
                current = key if value == "" else None
            elif value.startswith("[") and value.endswith("]"):
                meta[key] = [x.strip().strip("'\"") for x in value[1:-1].split(",") if x.strip()]
                current = None
            else:
                raise ValueError(f"unsupported list syntax: {key}")
        else:
            meta[key] = value.strip().strip("'\"")
            current = None
    return meta, source[boundary+4:]

def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def describe_parent_hashes(path: Path) -> list[str]:
    """Legacy compatibility diagnostic only; never required for v5 documents."""
    meta, _ = parse_document(path)
    feature = path.parent.parent
    known = {}
    for folder in LEVELS:
        for f in (feature / folder).glob("*.md"):
            m, _ = parse_document(f)
            known[m["id"]] = f
    return [f"{pid}@{git_blob_sha(known[pid])}" for pid in meta.get("parents", []) if pid in known]

def validate_feature(feature: Path, check_coverage: bool = False) -> list[str]:
    errors: list[str] = []
    docs: dict[str, dict] = {}
    by_level = {n: [] for n in range(1, 6)}
    for folder, (kind, prefix, level) in LEVELS.items():
        for path in sorted((feature / folder).glob("*.md")):
            try:
                meta, body = parse_document(path)
                missing = REQUIRED - meta.keys()
                if missing:
                    raise ValueError("missing metadata: " + ", ".join(sorted(missing)))
                if meta["kind"] != kind or not re.fullmatch(rf"{prefix}-\d{{3}}", meta["id"]):
                    errors.append(f"{path}: invalid kind or ID")
                for key in SEQUENCES:
                    if key not in meta:
                        meta[key] = []
                    if not isinstance(meta[key], list):
                        errors.append(f"{path}: {key} must be list")
                    elif len(meta[key]) != len(set(meta[key])):
                        errors.append(f"{path}: duplicate {key}")
                if meta["id"] in docs:
                    errors.append(f"{path}: duplicate ID {meta['id']}")
                    continue
                doc = {"path": path, "meta": meta, "body": body, "level": level}
                docs[meta["id"]] = doc
                by_level[level].append(doc)
            except (OSError, ValueError) as exc:
                errors.append(f"{path}: {exc}")
    specs = {}
    for d in by_level[2]:
        ids = DECLARED_REQUIREMENT.findall(d["body"])
        if len(ids) != len(set(ids)):
            errors.append(f"{d['path']}: duplicate requirement ID")
        specs[d["meta"]["id"]] = set(ids)
    for doc_id, doc in docs.items():
        m, level, path = doc["meta"], doc["level"], doc["path"]
        if level == 1 and m["parents"]:
            errors.append(f"{path}: brief cannot have parents")
        for pid in m["parents"]:
            parent = docs.get(pid)
            if parent is None:
                errors.append(f"{path}: unknown parent {pid}")
            elif parent["level"] >= level:
                errors.append(f"{path}: parent {pid} must be earlier level")
        for did in m["depends_on"]:
            dep = docs.get(did)
            if dep is None or dep["level"] != level or did == doc_id:
                errors.append(f"{path}: invalid dependency {did}")
        for req in m["requirements"]:
            match = REQUIREMENT.fullmatch(req)
            if not match or match.group(2) not in specs.get(match.group(1), set()):
                errors.append(f"{path}: unknown requirement {req}")
        if bool(m["amends"]) != bool(m["supersedes"]):
            errors.append(f"{path}: amendments require both amends and supersedes")
        for aid in m["amends"]:
            target = docs.get(aid)
            if not target or target["level"] != level or aid == doc_id:
                errors.append(f"{path}: invalid amendment target {aid}")
        for ref in m["supersedes"]:
            match = DECISION_REF.fullmatch(ref)
            if not match or match.group(1) not in m["amends"]:
                errors.append(f"{path}: invalid supersession {ref}")
            elif match.group(1) in docs:
                original = docs[match.group(1)]["body"]
                anchor = match.group(2)
                if (not re.search(r"(?m)^\s*[-*]?\s*" + re.escape(anchor) + r"\b", original)
                        and not re.search(r"(?m)^#{1,6}\s+.*\b" + re.escape(anchor.replace("-", " ")) + r"\b", original, re.I)):
                    errors.append(f"{path}: superseded anchor not found {ref}")
    for field in ("depends_on", "amends"):
        seen, active = set(), set()
        def visit(did: str) -> None:
            if did in active:
                errors.append(f"{feature}: {field} cycle at {did}")
                return
            if did in seen:
                return
            active.add(did)
            for nxt in docs[did]["meta"][field]:
                if nxt in docs:
                    visit(nxt)
            active.remove(did)
            seen.add(did)
        for did in docs:
            visit(did)
    claims: dict[str, str] = {}
    for did, doc in docs.items():
        for ref in doc["meta"]["supersedes"]:
            if ref in claims:
                errors.append(f"{doc['path']}: conflicting supersession {ref} claimed by {claims[ref]} and {did}")
            else:
                claims[ref] = did
    if check_coverage:
        for level in (3, 4, 5):
            for spec_id, reqs in specs.items():
                participants = [d for d in by_level[level]
                                if spec_id in d["meta"]["parents"]
                                or any(r.startswith(spec_id + "#") for r in d["meta"]["requirements"])]
                if participants:
                    covered = {r for d in participants for r in d["meta"]["requirements"]}
                    for req in sorted(reqs):
                        if f"{spec_id}#{req}" not in covered:
                            errors.append(f"{feature}: no document covers {spec_id}#{req} at level {level}")
    return errors

def validate_features(features_root: Path, check_coverage: bool = False) -> list[str]:
    if not features_root.exists():
        return []
    if not features_root.is_dir():
        return [f"{features_root}: expected directory"]
    errors = []
    for feature in sorted(f for f in features_root.iterdir() if f.is_dir()):
        errors.extend(validate_feature(feature, check_coverage))
    return errors

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("features_root", type=Path, nargs="?")
    parser.add_argument("--check-coverage", action="store_true")
    parser.add_argument("--show-parent-hashes", type=Path)
    args = parser.parse_args()
    if args.show_parent_hashes:
        print("parent_hashes: [" + ", ".join(describe_parent_hashes(args.show_parent_hashes)) + "]")
        return 0
    if not args.features_root:
        parser.error("features_root required")
    errors = validate_features(args.features_root, args.check_coverage)
    for e in errors:
        print("INVALID " + e)
    if errors:
        return 1
    print("VALID feature documents")
    return 0
if __name__ == "__main__":
    sys.exit(main())
