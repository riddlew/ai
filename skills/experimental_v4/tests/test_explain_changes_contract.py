"""Static guardrails for the explain-changes skill, not an agent behavior evaluation."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "brain-explain-changes" / "SKILL.md"


class ExplainChangesContract(unittest.TestCase):
    def test_manual_skill_with_argument_support(self):
        content = SKILL.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\nname: brain-explain-changes\n"))
        self.assertIn("disable-model-invocation: true", content)
        self.assertIn("argument-hint:", content)
        self.assertIn("$ARGUMENTS", content)

    def test_scopes_actual_changes_and_application_execution(self):
        content = SKILL.read_text(encoding="utf-8")
        for phrase in (
            "staged, unstaged, and untracked",
            "latest commit",
            "real execution path",
            "actually wired into production code",
            "what changed from what already existed",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_teaches_in_plain_language_and_pauses(self):
        content = SKILL.read_text(encoding="utf-8")
        for phrase in (
            "plain English",
            "short, direct sentences",
            "Explain unfamiliar terms",
            "one coherent part per response",
            "then pause",
            "Do not quiz the user unless requested",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_is_read_only_and_not_a_review(self):
        content = SKILL.read_text(encoding="utf-8")
        self.assertIn("**Read-only:**", content)
        self.assertIn("**Not a review:**", content)
        self.assertIn("don't run them unless the user asks", content)
        self.assertIn("Do not claim an execution path", content)

    def test_skill_appears_in_installed_guides(self):
        readme = (ROOT / "brain-init" / "references" / "README.md").read_text(encoding="utf-8")
        usage = (ROOT / "brain-init" / "references" / "USAGE.md").read_text(encoding="utf-8")
        self.assertIn("**17 Claude Code skills**", readme)
        self.assertIn("/brain-explain-changes", readme)
        self.assertIn("/brain-explain-changes", usage)


if __name__ == "__main__":
    unittest.main()
