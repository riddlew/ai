#!/usr/bin/env python3
"""Validate and summarize declared behavioral coverage; never imply agent success.

A scenario reference establishes that a scenario has been specified, not run.
Fresh-agent evidence is collected separately outside the repository.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CATALOG = HERE / "behavioral-coverage.json"
SCENARIO_FILES = (
    HERE / "scenarios.md",
    HERE / "skill-test-scenarios.md",
    HERE / "hierarchical-scenarios.md",
)
SCENARIO_HEADING = re.compile(r"^#{2,4}\s+([SH]\d+[A-Z]?)(?=\s|:|—|$)", re.M)
PRIORITIES = {"critical", "high", "medium"}


def known_scenarios() -> set[str]:
    return set().union(*(set(SCENARIO_HEADING.findall(p.read_text(encoding="utf-8")))
                         for p in SCENARIO_FILES))


def known_skills() -> set[str]:
    return {p.parent.name for p in ROOT.glob("brain-*/SKILL.md")} | {"write-human"}


def load_catalog(path: Path = CATALOG) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_catalog(data: dict) -> list[str]:
    errors = []
    if data.get("schema") != 1:
        errors.append("unknown catalog schema")
    if data.get("minimum_samples_for_general_claim", 0) < 3:
        errors.append("general reliability claims require at least three valid runs")
    skills, scenarios, ids = known_skills(), known_scenarios(), set()
    represented = set()
    for row in data.get("rules", []):
        ident = row.get("id", "")
        if not ident or ident in ids:
            errors.append(f"missing/duplicate rule id: {ident!r}")
        ids.add(ident)
        skill = row.get("skill")
        if skill not in skills:
            errors.append(f"{ident}: unknown skill {skill!r}")
        represented.add(skill)
        if row.get("priority") not in PRIORITIES:
            errors.append(f"{ident}: unknown priority")
        matches = row.get("scenarios")
        if not isinstance(matches, list) or len(matches) != len(set(matches)):
            errors.append(f"{ident}: scenarios must be a unique list")
            continue
        for scenario in matches:
            if scenario not in scenarios:
                errors.append(f"{ident}: scenario {scenario!r} not defined")
        if not matches and not row.get("gap", "").strip():
            errors.append(f"{ident}: untested rule requires an actionable gap")
        if matches and row.get("gap"):
            errors.append(f"{ident}: use gap only when no scenario is defined")
    for skill in sorted(skills - represented):
        errors.append(f"no rules inventoried for skill: {skill}")
    return errors


def report(data: dict) -> dict:
    rows = data["rules"]
    defined = [r for r in rows if r["scenarios"]]
    gaps = [r for r in rows if not r["scenarios"]]
    return {
        "skills_inventoried": len({r["skill"] for r in rows}),
        "rules": len(rows),
        "with_defined_scenarios": len(defined),
        "without_defined_scenarios": len(gaps),
        "critical_gaps": [r["id"] for r in gaps if r["priority"] == "critical"],
        "all_agent_outcomes": "unmeasured",
        "minimum_samples_for_general_claim": data["minimum_samples_for_general_claim"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="print machine-readable coverage report")
    parser.add_argument("--strict", action="store_true", help="also fail when a critical scenario is missing")
    args = parser.parse_args()
    data = load_catalog()
    errors = validate_catalog(data)
    summary = report(data)
    if args.json:
        print(json.dumps({"coverage": summary, "errors": errors}, indent=2))
    else:
        print(f"{summary['skills_inventoried']} skills; {summary['rules']} rules; "
              f"{summary['with_defined_scenarios']} have scenario definitions, "
              f"{summary['without_defined_scenarios']} need scenarios.")
        print("No agent run is inferred from a scenario definition.")
        for name in summary["critical_gaps"]:
            print(f"  CRITICAL GAP: {name}")
        for error in errors:
            print(f"  ERROR: {error}")
    return 1 if errors or (args.strict and summary["critical_gaps"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
