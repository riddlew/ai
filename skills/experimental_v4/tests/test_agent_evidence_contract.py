"""Execution metadata cannot certify skill behavior."""
import importlib.util
import json
import sys
import tempfile
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("ev", HERE / "summarize_agent_evidence.py")
ev = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = ev
spec.loader.exec_module(ev)


class AgentEvidenceContract(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "one" / "meta.json"
        self.path.parent.mkdir()

    def inspect(self, **kwargs):
        data = {"scenario": "H6B", "arm": "candidate", "model": "sonnet",
                "sample": 1, "arm_digest_before": "a", "arm_digest_after": "a",
                "turns": [{"reply": "Finished", "exit": 0, "is_error": False, "cost_usd": 0.3}]}
        data.update(kwargs)
        self.path.write_text(json.dumps(data))
        return ev.inspect(self.path)

    def test_success_is_ungraded(self):
        outcome = self.inspect()
        self.assertTrue(outcome["valid"])
        self.assertEqual("ungraded", outcome["behavior"])
        cohort = ev.summarize([self.path])["cohorts"][0]
        self.assertFalse(cohort["enough_samples_for_general_claim"])
        self.assertEqual("not assessed", cohort["behavior"])

    def test_error_invalidates(self):
        self.assertFalse(self.inspect(turns=[{"is_error": True, "exit": 1}])["valid"])

    def test_mutated_skill_invalidates(self):
        self.assertFalse(self.inspect(arm_digest_after="different")["valid"])

    def test_skipped_followup_invalidates(self):
        self.assertFalse(self.inspect(turns=[{"skipped": "budget"}])["valid"])


if __name__ == "__main__":
    unittest.main()
