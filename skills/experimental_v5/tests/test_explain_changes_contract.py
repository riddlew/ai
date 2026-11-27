"""Static guardrails for the explain-changes skill, not an agent behavior evaluation."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "brain-explain-changes" / "SKILL.md"
DETAILS = ROOT / "brain-explain-changes" / "references" / "explain-details.md"


class ExplainChangesContract(unittest.TestCase):
    @unittest.skip("Legacy v4 instruction contract superseded; see test_v5_workflow.py")
    def test_auto_invocable_skill_with_manual_argument_support(self):
        content = SKILL.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\nname: brain-explain-changes\n"))
        frontmatter = content.split("\n---\n", 1)[0]
        self.assertNotIn("disable-model-invocation: true", frontmatter)
        self.assertIn("argument-hint:", frontmatter)
        self.assertIn("$ARGUMENTS", content)

    @unittest.skip("Legacy v4 instruction contract superseded; see test_v5_workflow.py")

    def test_scopes_actual_changes_and_application_execution(self):
        content = SKILL.read_text(encoding="utf-8")
        for phrase in (
            "staged, unstaged, and untracked",
            "latest commit",
            "real execution path",
            "actually wired into production code",
            "what changed from what already existed",
            "final cumulative diff",
            "merge base",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    @unittest.skip("Legacy v4 instruction contract superseded; see test_v5_workflow.py")

    def test_teaches_in_plain_language_and_pauses(self):
        content = SKILL.read_text(encoding="utf-8")
        for phrase in (
            "plain English",
            "short, direct sentences",
            "Explain unfamiliar terms",
            "one coherent part per response",
            "then pause",
            "Do not quiz the user unless requested",
            "recorded design rationale",
            "inferred reasons",
            "how selected files connect",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    @unittest.skip("Legacy v4 instruction contract superseded; see test_v5_workflow.py")

    def test_flexible_scope_not_a_collection_of_prescriptive_modes(self):
        content = SKILL.read_text(encoding="utf-8")
        for phrase in (
            "Adapt to their question",
            "do not force",
            "file",
            "branch",
            "subsystem",
            "user drive",
            "no new ledger",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), content.lower())
        self.assertNotIn("## Mode 1", content)
        self.assertNotIn("## Mode 2", content)

    def test_branch_walkthrough_uses_cumulative_actual_diff(self):
        details = DETAILS.read_text(encoding="utf-8")
        for phrase in (
            "intended target branch",
            "merge base",
            "final cumulative diff",
            "Do not narrate each commit",
            "added, modified, renamed and deleted",
            "change map",
            "uncommitted staged, unstaged and untracked",
            "conversation-level",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), details.lower())

    @unittest.skip("Legacy v4 instruction contract superseded; see test_v5_workflow.py")

    def test_during_implementation_review_preserves_approval_checkpoint(self):
        content = SKILL.read_text(encoding="utf-8")
        details = DETAILS.read_text(encoding="utf-8")
        for phrase in ("brain-implement", "brain-pair-program",
                       "do not approve, close or advance that checkpoint"):
            self.assertIn(phrase.lower(), content.lower())
        for phrase in ("execution.md", "do not mark the increment approved",
                       "not** authorization to approve"):
            self.assertIn(phrase.lower(), details.lower())

    @unittest.skip("Legacy v4 instruction contract superseded; see test_v5_workflow.py")

    def test_is_read_only_and_not_a_review(self):
        content = SKILL.read_text(encoding="utf-8")
        self.assertIn("**Read-only:**", content)
        self.assertIn("**Not a review:**", content)
        self.assertIn("don't run them unless the user asks", content)
        self.assertIn("Do not claim an execution path", content)
        self.assertIn("Follow `CLAUDE.local.md`", content)

    @unittest.skip("Legacy v4 instruction contract superseded; see test_v5_workflow.py")

    def test_skill_appears_in_installed_guides(self):
        readme = (ROOT / "brain-init" / "references" / "README.md").read_text(encoding="utf-8")
        usage = (ROOT / "brain-init" / "references" / "USAGE.md").read_text(encoding="utf-8")
        self.assertIn("**23 Claude Code skills**", readme)
        self.assertIn("/brain-explain-changes", readme)
        self.assertIn("/brain-explain-changes", usage)
        self.assertIn("final cumulative diff", readme)
        self.assertIn("branch feature/order-cancellation", usage)


if __name__ == "__main__":
    unittest.main()
