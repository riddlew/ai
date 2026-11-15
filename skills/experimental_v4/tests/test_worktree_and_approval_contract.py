"""Static checks for worktree-safety and approval-invalidation rules and runner limits.

These pin the wording agents rely on and the runner's usage guards. They do
not show that an agent follows the rules; fresh-agent scenarios H7 and H10 do.
"""
import contextlib
import importlib.util
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
POLICY = (ROOT / "brain-init/references/CLAUDE.local.md").read_text()
IMPLEMENT = (ROOT / "brain-implement/SKILL.md").read_text()
UPDATE = (ROOT / "brain-update/SKILL.md").read_text()
WRITE_SPEC = (ROOT / "brain-write-spec/SKILL.md").read_text()

spec = importlib.util.spec_from_file_location("brain_runner", ROOT / "tests/run_hierarchical_scenario.py")
runner = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = runner
spec.loader.exec_module(runner)


def section(text: str, start: str, end: str) -> str:
    return text.split(start, 1)[1].split(end, 1)[0]


class WorktreeSafetyContract(unittest.TestCase):
    def test_policy_states_general_worktree_rules(self):
        rule = section(POLICY, "**Worktrees and brain writes.**", "\n\n")
        for phrase in ("uses the brain located above", "worktrees share one brain",
                       "when access is permitted", "never route around a denied write",
                       "copy of the brain", "ask the user how to proceed", "pending/<branch>.md"):
            self.assertIn(phrase, rule)

    def test_skills_follow_the_policy_without_environment_specific_rules(self):
        self.assertIn("If that write is denied, follow `CLAUDE.local.md` §Worktrees and brain writes",
                      section(IMPLEMENT, "## 2.", "## 3."))
        self.assertIn("do not copy brain documents into it", section(IMPLEMENT, "## 1.", "## 2."))
        rule = section(UPDATE, "**Write access.**", "\n\n")
        self.assertIn("§Worktrees and brain writes", rule)
        self.assertIn("never route around the denial", rule)
        for text in (POLICY, IMPLEMENT, UPDATE):
            for term in ("claude --worktree", "EnterWorktree", "isolated session"):
                self.assertNotIn(term, text)


class ApprovalInvalidationContract(unittest.TestCase):
    def test_material_spec_revision_needs_explicit_reapproval(self):
        rule = section(WRITE_SPEC, "**Revising an approved spec.**", "### Technical Decisions")
        for phrase in ("`status: needs-revision` in the same edit", "never renumber",
                       "not approval of the written revision", "Editorial changes",
                       "`brain-decompose`, `brain-blueprint`, `brain-write-tasks`",
                       "do not change their status or `parent_hashes` yourself", "**Unaffected:**"):
            self.assertIn(phrase, rule)


class RunnerLimits(unittest.TestCase):
    def batch(self, *extra):
        argv = ["run", "batch", tempfile.mkdtemp(), "--arm", "green=/nonexistent",
                "--jobs", "H10B:green:1", *extra]
        out = io.StringIO()
        with mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(out), \
                mock.patch.object(runner, "run", side_effect=AssertionError("agent launched")):
            code = runner.main()
        return code, out.getvalue()

    def test_defaults_are_bounded_and_dry_run(self):
        self.assertEqual(30, runner.DEFAULT_MAX_TURNS)
        self.assertEqual(1.00, runner.DEFAULT_BUDGET_USD)
        self.assertIn("sonnet", runner.STANDARD)
        code, out = self.batch()
        self.assertEqual(0, code)
        self.assertIn("DRY RUN", out)

    def test_more_than_one_session_is_rejected(self):
        with self.assertRaises(SystemExit):
            self.batch("--parallel", "2", "--execute")

    def test_session_command_disallows_nested_agents_and_caps_usage(self):
        captured = {}

        def fake(command, **kwargs):
            captured["command"] = command
            return subprocess.CompletedProcess(command, 0, "", "")

        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(runner.subprocess, "run", fake):
            runner.claude("prompt", Path(tmp), runner.STANDARD, [], Path(tmp) / "log.jsonl", [])
        command = captured["command"]
        self.assertEqual("Agent", command[command.index("--disallowedTools") + 1])
        self.assertEqual("30", command[command.index("--max-turns") + 1])
        self.assertEqual("1.0", command[command.index("--max-budget-usd") + 1])
        self.assertEqual(runner.STANDARD, command[command.index("--model") + 1])


if __name__ == "__main__":
    unittest.main()
