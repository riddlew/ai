#!/usr/bin/env python3
"""Check references and metadata in the new .brain/features/ hierarchy.

Uses only Python's standard library and the intentionally small YAML
frontmatter subset defined in feature-document-contract.md.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

LEVELS = {
    "01-brief": ("brief", "BRF", 1),
    "02-specifications": ("specification", "SPEC", 2),
    "03-components": ("component", "CMP", 3),
    "04-implementation-plans": ("implementation-plan", "PLAN", 4),
    "05-tasks": ("task", "TASK", 5),
}
SEQUENCES = {"parents", "requirements", "depends_on"}
REQUIRED = {"id", "kind", "status", *SEQUENCES}
STATUSES = {"draft", "approved", "needs-revision"}
REQUIREMENT = re.compile(r"^(SPEC-\d{3})#(REQ-\d{3})$")
DECLARED_REQUIREMENT = re.compile(r"^\s*(?:[-*]\s*)?(REQ-\d{3}):", re.MULTILINE)


def _items(value: str) -> list[str]:
    value = value.strip()
    if value == "[]":
        return []
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1]
    return [item.strip().strip("'\"") for item in value.split(",") if item.strip()]


def parse_document(path: Path) -> tuple[dict, str]:
    """Parse a limited metadata map, including simple YAML sequences."""
    source = path.read_text(encoding="utf-8")
    lines = source.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("missing opening YAML frontmatter delimiter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError("missing closing YAML frontmatter delimiter") from exc

    values: dict = {}
    active: str | None = None
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - ") and active in SEQUENCES:
            values[active].append(line[4:].strip().strip("'\""))
            continue
        match = re.fullmatch(r"([a-z_]+):\s*(.*)", line)
        if match is None:
            raise ValueError(f"unsupported YAML frontmatter syntax: {line!r}")
        key, value = match.groups()
        if key in values:
            raise ValueError(f"duplicate metadata key: {key}")
        if key in SEQUENCES:
            values[key] = _items(value)
            active = key if not value else None
        else:
            values[key] = value.strip().strip("'\"")
            active = None
    return values, "\n".join(lines[end + 1:])


def validate_feature(feature: Path, check_coverage: bool = False) -> list[str]:
    errors: list[str] = []
    documents: dict[str, dict] = {}
    by_level: dict[int, list[dict]] = {i: [] for i in range(1, 6)}

    for folder, (kind, prefix, level) in LEVELS.items():
        location = feature / folder
        if not location.exists():
            continue
        for file in sorted(location.glob("*.md")):
            try:
                metadata, body = parse_document(file)
            except (OSError, ValueError) as exc:
                errors.append(f"{file}: {exc}")
                continue

            missing = REQUIRED - metadata.keys()
            if missing:
                errors.append(f"{file}: missing metadata: {', '.join(sorted(missing))}")
                continue
            if metadata["kind"] != kind:
                errors.append(f"{file}: kind must be {kind}")
            if not re.fullmatch(rf"{prefix}-\d{{3}}", metadata["id"]):
                errors.append(f"{file}: invalid {kind} id {metadata['id']!r}")
            if metadata["status"] not in STATUSES:
                errors.append(f"{file}: invalid status {metadata['status']!r}")
            for key in SEQUENCES:
                if not isinstance(metadata[key], list):
                    errors.append(f"{file}: {key} must be a sequence")
                if len(metadata[key]) != len(set(metadata[key])):
                    errors.append(f"{file}: duplicate entries in {key}")

            doc_id = metadata["id"]
            if doc_id in documents:
                errors.append(f"{file}: duplicate id {doc_id} (also {documents[doc_id]['path']})")
                continue
            doc = {"path": file, "id": doc_id, "kind": kind,
                   "level": level, "meta": metadata, "body": body}
            documents[doc_id] = doc
            by_level[level].append(doc)

    # Specification requirements must be unique so stable qualified IDs are reliable.
    for spec in by_level[2]:
        ids = DECLARED_REQUIREMENT.findall(spec["body"])
        if len(ids) != len(set(ids)):
            errors.append(f"{spec['path']}: duplicate declared requirement ID")

    for doc in documents.values():
        meta, path = doc["meta"], doc["path"]
        if doc["level"] == 1 and meta["parents"]:
            errors.append(f"{path}: brief must not have parents")
        if doc["level"] > 1 and not meta["parents"]:
            if any(by_level[i] for i in range(1, doc["level"])):
                errors.append(f"{path}: parent reference required when earlier documents exist")
        for parent_id in meta["parents"]:
            parent = documents.get(parent_id)
            if parent is None:
                errors.append(f"{path}: unknown parent {parent_id}")
            elif parent["level"] >= doc["level"]:
                errors.append(f"{path}: parent {parent_id} must be from an earlier level")
            elif meta["status"] == "approved" and parent["meta"]["status"] != "approved":
                errors.append(f"{path}: approved document has unapproved parent {parent_id}")
        for dep_id in meta["depends_on"]:
            dep = documents.get(dep_id)
            if dep is None:
                errors.append(f"{path}: unknown dependency {dep_id}")
            elif dep["level"] != doc["level"]:
                errors.append(f"{path}: dependency {dep_id} must be at the same level")
            elif dep_id == doc["id"]:
                errors.append(f"{path}: self-dependency {dep_id}")
            elif meta["status"] == "approved" and dep["meta"]["status"] != "approved":
                errors.append(f"{path}: approved document has unapproved dependency {dep_id}")
        parent_requirements: set[str] = set()
        for parent_id in meta["parents"]:
            parent = documents.get(parent_id)
            if parent is None:
                continue
            if parent["kind"] == "specification":
                parent_requirements.update(
                    f"{parent_id}#{req}" for req in DECLARED_REQUIREMENT.findall(parent["body"])
                )
            else:
                parent_requirements.update(parent["meta"]["requirements"])
        for req in meta["requirements"]:
            if doc["level"] >= 3 and meta["parents"] and req not in parent_requirements:
                errors.append(f"{path}: requirement {req} is not supported by a parent")
            match = REQUIREMENT.fullmatch(req)
            if match is None:
                errors.append(f"{path}: invalid qualified requirement {req!r}")
                continue
            spec_id, requirement_id = match.groups()
            spec = documents.get(spec_id)
            if spec is None or spec["kind"] != "specification":
                errors.append(f"{path}: unknown specification {spec_id} in {req}")
            elif requirement_id not in set(DECLARED_REQUIREMENT.findall(spec["body"])):
                errors.append(f"{path}: unknown requirement {req}")

    # Cycles on explicit same-level dependencies, even when dependencies are valid IDs.
    visiting: set[str] = set()
    visited: set[str] = set()

    def walk(doc_id: str, path: tuple[str, ...]) -> None:
        if doc_id in visiting:
            errors.append(f"{documents[doc_id]['path']}: dependency cycle: {' -> '.join((*path, doc_id))}")
            return
        if doc_id in visited:
            return
        visiting.add(doc_id)
        for dep in documents[doc_id]["meta"]["depends_on"]:
            if dep in documents and dep != doc_id:
                walk(dep, (*path, doc_id))
        visiting.remove(doc_id)
        visited.add(doc_id)

    for doc_id in documents:
        walk(doc_id, ())

    if check_coverage:
        required = {
            f"{doc['id']}#{req}"
            for doc in by_level[2] if doc["meta"]["status"] == "approved"
            for req in DECLARED_REQUIREMENT.findall(doc["body"])
        }
        for level in range(3, 6):
            if not by_level[level]:
                continue  # A deliberate skipped level is not a coverage failure.
            if any(doc["meta"]["status"] != "approved" for doc in by_level[level]):
                continue  # Partial drafts are not claiming complete stage coverage.
            covered = {
                req for doc in by_level[level] if doc["meta"]["status"] == "approved"
                for req in doc["meta"]["requirements"]
            }
            for req in sorted(required - covered):
                errors.append(f"{feature / next(k for k, v in LEVELS.items() if v[2] == level)}: "
                              f"no approved document covers {req}")
    return errors


def validate_features(features_root: Path, check_coverage: bool = False) -> list[str]:
    if not features_root.exists():
        return []  # A new brain need not have a features directory yet.
    if not features_root.is_dir():
        return [f"{features_root}: expected directory, found non-directory"]
    errors: list[str] = []
    for feature in sorted(p for p in features_root.iterdir() if p.is_dir()):
        errors.extend(validate_feature(feature, check_coverage))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("features_root", type=Path, help="path to .brain/features")
    parser.add_argument("--check-coverage", action="store_true",
                        help="require each populated downstream stage to cover approved requirements")
    args = parser.parse_args()
    errors = validate_features(args.features_root, args.check_coverage)
    if errors:
        for error in errors:
            print(error)
        print(f"{len(errors)} feature-document error(s)")
        return 1
    print(f"Feature documents valid: {args.features_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
