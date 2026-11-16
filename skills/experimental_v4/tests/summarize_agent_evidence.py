#!/usr/bin/env python3
"""Summarize agent-run metadata without claiming any behavioral pass or failure."""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path


def inspect(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return {"path": str(path), "valid": False, "reason": str(exc)}
    turns = data.get("turns", [])
    if not isinstance(turns, list) or not turns:
        reason = "missing agent turns"
    elif any(t.get("is_error") or t.get("exit") not in (None, 0) for t in turns):
        reason = "agent execution error"
    elif any(t.get("skipped") for t in turns):
        reason = "incomplete scripted follow-up"
    elif data.get("arm_digest_before") != data.get("arm_digest_after"):
        reason = "skill arm modified during run"
    elif any(t.get("reply") is None for t in turns):
        reason = "missing reply"
    else:
        reason = ""
    return {
        "path": str(path), "scenario": data.get("scenario", "?"),
        "arm": data.get("arm", "?"), "model": data.get("model", "?"),
        "sample": data.get("sample"),
        "valid": not reason, "reason": reason,
        "cost_usd": sum(t.get("cost_usd") or 0 for t in turns if isinstance(t, dict)),
        "seconds": sum(t.get("seconds") or 0 for t in turns if isinstance(t, dict)),
        "behavior": "ungraded",
    }


def summarize(paths: list[Path]) -> dict:
    samples = [inspect(path) for path in paths]
    by_group = defaultdict(list)
    for item in samples:
        by_group[(item.get("scenario", "?"), item.get("arm", "?"),
                  item.get("model", "?"))].append(item)
    groups = []
    for (scenario, arm, model), rows in sorted(by_group.items()):
        count = sum(bool(r["valid"]) for r in rows)
        groups.append({
            "scenario": scenario, "arm": arm, "model": model,
            "recorded": len(rows), "potentially_gradable": count,
            "void_or_incomplete": len(rows) - count,
            "enough_samples_for_general_claim": count >= 3,
            "behavior": "not assessed",
            "recorded_cost_usd": round(sum(r.get("cost_usd", 0) for r in rows), 5),
            "recorded_seconds": sum(r.get("seconds", 0) for r in rows),
        })
    return {"report_type": "execution_metadata_not_behavioral_grading",
            "cohorts": groups, "runs": samples}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not args.evidence.is_dir():
        parser.error("evidence must be an existing directory")
    result = summarize(sorted(args.evidence.glob("*/meta.json")))
    if args.json:
        print(json.dumps(result, indent=2))
    elif not result["runs"]:
        print("No agent runs found; no behavior measured.")
    else:
        for group in result["cohorts"]:
            print(group["scenario"], group["arm"],
                  str(group["potentially_gradable"]) + "/" + str(group["recorded"]),
                  "potentially gradable; behavior NOT graded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
