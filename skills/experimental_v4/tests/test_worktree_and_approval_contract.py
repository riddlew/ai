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
    def test_policy_distinguishes_ordinary_worktrees_from_isolated_sessions(self):
        rule = section(POLICY, "**Worktrees and brain writes.**", "\n\n")
        for phrase in ("ordinary linked Git worktree is not isolation", "claude --worktree",
                       "EnterWorktree", "external brain", "/brain-init <path>",
                       "non-isolated session", "Bash, Python", "pending/<branch>.md"):
            self.assertIn(phrase, rule)

    def test_implement_checks_brain_access_before_code_and_review_base(self):
        boundary = section(IMPLEMENT, "## 1. Establish the boundary", "**Execution mode switch.**")
        self.assertLess(boundary.index("**Brain write access.**"), boundary.index("Record the review base"))
        step = section(boundary, "**Brain write access.**", "\n6. ")
        for phrase in ("§Worktrees and brain writes", "ordinary worktree", "before editing code",
                       "/brain-init <path>", "non-isolated session", "Bash, Python"):
            self.assertIn(phrase, step)
        self.assertIn("pending/<branch>.md", section(IMPLEMENT, "## 6. Keep state accurate", "## 7."))

    def test_update_follows_the_same_rule(self):
        rule = section(UPDATE, "**Isolated worktree sessions.**", "\n\n")
        for phrase in ("§Worktrees and brain writes", "Bash, Python", "non-isolated session",
                       "ordinary worktree", "pending/<branch>.md", "/brain-init <path>"):
            self.assertIn(phrase, rule)


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
