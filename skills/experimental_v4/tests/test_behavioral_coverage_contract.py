"""Static inventory and routing contracts, not agent behavioral tests."""
import importlib.util
import json
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("coverage", HERE / "check_behavioral_coverage.py")
coverage = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = coverage
spec.loader.exec_module(coverage)


class BehavioralCoverageContract(unittest.TestCase):
    def setUp(self):
        self.data = coverage.load_catalog()

    def test_inventory_covers_every_skill_and_is_valid(self):
        self.assertEqual([], coverage.validate_catalog(self.data))
        self.assertEqual(19, coverage.report(self.data)["skills_inventoried"])

    def test_defined_scenarios_do_not_mean_success(self):
        summary = coverage.report(self.data)
        self.assertEqual("unmeasured", summary["all_agent_outcomes"])
        self.assertGreater(len(summary["critical_gaps"]), 0)

    def test_unknown_scenario_rejected(self):
        self.data["rules"][0]["scenarios"].append("H999")
        self.assertTrue(any("H999" in e for e in coverage.validate_catalog(self.data)))

    def test_uncovered_rule_requires_explicit_gap(self):
        row = next(r for r in self.data["rules"] if not r["scenarios"])
        row["gap"] = ""
        self.assertTrue(any(row["id"] in e for e in coverage.validate_catalog(self.data)))

    def test_duplicate_rule_rejected(self):
        self.data["rules"][1]["id"] = self.data["rules"][0]["id"]
        self.assertTrue(any("duplicate" in e for e in coverage.validate_catalog(self.data)))

    def test_routing_cases_reference_real_distinct_skills(self):
        routes = json.loads((HERE / "routing-cases.json").read_text(encoding="utf-8"))
        self.assertEqual(1, routes["schema"])
        ids = set()
        for case in routes["cases"]:
            self.assertNotIn(case["id"], ids)
            ids.add(case["id"])
            self.assertTrue(case["request"].strip())
            self.assertIn(case["expected"], coverage.known_skills())
            self.assertNotIn(case["expected"], case["not"])
            for name in case["not"]:
                self.assertIn(name, coverage.known_skills())
        self.assertGreaterEqual(len(ids), 10)


if __name__ == "__main__":
    unittest.main()
