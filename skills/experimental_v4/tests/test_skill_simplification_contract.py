"""Contracts for concise primary skill instructions and preserved on-demand detail.

These check packaging and critical instructions; they are not agent behavior tests.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = sorted([*ROOT.glob("brain-*/SKILL.md"), ROOT / "write-human/SKILL.md"])
POLICY = ROOT / "brain-init/references/CLAUDE.local.md"


class SimplificationContract(unittest.TestCase):
    def test_every_entrypoint_has_a_valid_purpose_and_on_demand_details(self):
        self.assertEqual(19, len(SKILLS))
        for skill in SKILLS:
            with self.subTest(skill=skill.parent.name):
                content = skill.read_text(encoding="utf-8")
                self.assertTrue(content.startswith("---\nname: "))
                self.assertIn("\n---\n", content)
                self.assertIn("# ", content)
                self.assertLess(len(content.encode("utf-8")), 6500)
                self.assertIn("references/", content,
                              "Entry point must link to applicable details, checks or templates")
                self.assertNotIn("read **all** root", content.lower(),
                                 "No unconditional full-root read in every skill")
                self.assertNotIn("brain-context plan", content,
                                 "The context map must not become a mandatory skill gate")

    def test_cross_cutting_safety_is_visible_in_primary_instructions(self):
        policy = POLICY.read_text(encoding="utf-8")
        implement = (ROOT / "brain-implement/SKILL.md").read_text()
        update = (ROOT / "brain-update/SKILL.md").read_text()
        spec = (ROOT / "brain-write-spec/SKILL.md").read_text()
        for key in ("Worktrees and brain writes", "authorized filesystem boundaries",
                    "pending/<branch>.md", "consequential", "approval",
                    "read more", "context-map.tsv"):
            self.assertIn(key.lower(), policy.lower())
        for key in ("collaborative", "wait", "review base", "do not copy brain",
                    "approved", "tests", "execution.md", "brain-update"):
            self.assertIn(key.lower(), implement.lower())
        for key in ("Read **every project-knowledge root file**",
                    "Do not use selective context loading",
                    "never route around the restriction",
                    "pending/<branch>.md", "Last synced"):
            self.assertIn(key, update)
        for key in ("status: needs-revision", "not approval of the written revision",
                    "parent_hashes", "Unaffected:"):
            self.assertIn(key, spec)

    def test_context_discovery_is_not_a_scope_exclusion_or_map_gate(self):
        policy = POLICY.read_text(encoding="utf-8")
        guidance = (ROOT / "brain-init/references/safe-context-loading.md").read_text()
        details = (ROOT / "brain-init/references/safe-context-map-protocol.md").read_text()
        self.assertIn("optional discovery accelerators", policy)
        self.assertIn("not a gate or an exclusion list", policy)
        self.assertIn("Read matching documents and their references", policy)
        self.assertIn("read more", policy.lower())
        self.assertIn("not mandatory", guidance)
        self.assertIn("original sources", guidance)
        self.assertIn("context-map.tsv", details)
        for ext in ("brain-context.py", "brain-context.mjs", "brain-context.sh"):
            self.assertTrue((ROOT / "brain-init/scripts" / ext).exists())

    def test_separate_workflows_and_read_only_guards(self):
        review = (ROOT / "brain-review-merge-request/SKILL.md").read_text()
        architecture = (ROOT / "brain-review-architecture/SKILL.md").read_text()
        backlog = (ROOT / "brain-refine-backlog/SKILL.md").read_text()
        writing = (ROOT / "write-human/SKILL.md").read_text()
        tester = (ROOT / "brain-test-skill/SKILL.md").read_text()
        self.assertIn("read-only", review.lower())
        self.assertIn("standalone architecture review", architecture)
        self.assertIn("Strictly read-only", backlog)
        self.assertIn("explicit voice", writing.lower())
        self.assertIn("editing mode", writing.lower())
        self.assertIn("No test run", tester)
        init = (ROOT / "brain-init/SKILL.md").read_text()
        self.assertIn("Existing-project migration", init)
        self.assertIn("preserving project-specific instructions", init)

    def test_selected_workflow_skills_allow_automatic_invocation_without_waiving_approval(self):
        automatically_invocable = {
            "brain-design-implementation", "brain-decompose-feature", "brain-explain-changes",
            "brain-write-spec", "brain-write-tasks", "brain-implement",
        }
        intentionally_manual = {"brain-distill-content", "brain-review-merge-request", "write-human"}
        for name in sorted(automatically_invocable | intentionally_manual):
            with self.subTest(skill=name):
                header = (ROOT / name / "SKILL.md").read_text(encoding="utf-8").split("\n---\n", 1)[0]
                self.assertEqual(name in intentionally_manual,
                                 "disable-model-invocation: true" in header)
        implement = (ROOT / "brain-implement/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Automatic skill invocation is not authorization to modify code", implement)
        self.assertIn("user explicitly requests implementation", implement)
        self.assertIn("Approval of a specification, blueprint, or task list", implement)

    def test_all_skills_provide_a_non_executing_next_step(self):
        for skill in SKILLS:
            with self.subTest(skill=skill.parent.name):
                content = skill.read_text(encoding="utf-8")
                self.assertEqual(1, content.count("**Recommended next step:**"))
                recommendation = content.split("**Recommended next step:**", 1)[1]
                for required in ("final user-facing reply", "If blocked",
                                 "if complete", "not authorization",
                                 "outside copy-ready deliverables"):
                    self.assertIn(required, recommendation)
        writing = (ROOT / "write-human/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("without inserting commentary into it", writing)

    def test_model_tier_readme_covers_every_skill_once(self):
        readme = (ROOT / "brain-init/references/README.md").read_text(encoding="utf-8")
        heading = "## Model tiers and recommended models\n"
        self.assertEqual(1, readme.count(heading))
        section = readme.split(heading, 1)[1].split("\n## ", 1)[0]
        entries = re.findall(r"^\| `([^`]+)` \| \*\*(Sonnet|Opus)\*\* \|", section, re.M)
        names = [name for name, _ in entries]
        self.assertEqual(len(SKILLS), len(names))
        self.assertEqual(len(names), len(set(names)), "Each skill must appear exactly once")
        self.assertEqual({skill.parent.name for skill in SKILLS}, set(names))

    def test_renamed_skills_and_guides_are_consistent(self):
        renames = {
            "brain-blueprint": "brain-design-implementation",
            "brain-decompose": "brain-decompose-feature",
        }
        for old, new in renames.items():
            with self.subTest(skill=new):
                self.assertFalse((ROOT / old).exists())
                skill = (ROOT / new / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn("name: " + new + "\n", skill)
        for path in (
            ROOT / "brain-init/references/README.md",
            ROOT / "brain-init/references/USAGE.md",
            ROOT / "brain-init/references/CLAUDE.local.md",
            ROOT / "brain-init/references/feature-document-contract.md",
        ):
            content = path.read_text(encoding="utf-8")
            for old, new in renames.items():
                self.assertIsNone(re.search(r"(?<![A-Za-z0-9_-])" + re.escape(old) + r"(?![A-Za-z0-9_-])", content), str(path))
                self.assertIn(new, content, str(path))
        readme = (ROOT / "brain-init/references/README.md").read_text(encoding="utf-8")
        for name in (
            "brain-design-implementation", "brain-decompose-feature",
            "brain-explain-changes", "brain-implement", "brain-write-spec",
        ):
            self.assertNotIn("`" + name + "` **(manual)**", readme)

    def test_detailed_workflows_still_exist(self):
        pairs = {
            "brain-init": "init-details.md",
            "brain-brainstorm": "brainstorm-details.md",
            "brain-write-spec": "spec-details.md",
            "brain-decompose-feature": "decompose-details.md",
            "brain-design-implementation": "blueprint-details.md",
            "brain-write-tasks": "task-details.md",
            "brain-implement": "implement-details.md",
            "brain-update": "update-details.md",
            "brain-plan": "plan-details.md",
            "brain-review-code": "code-review-details.md",
            "brain-review-architecture": "architecture-review-details.md",
            "brain-review-security": "security-review-details.md",
            "brain-review-merge-request": "mr-review-details.md",
            "brain-diagnose": "diagnose-details.md",
            "brain-explain-changes": "explain-details.md",
            "brain-distill-content": "distill-details.md",
            "brain-refine-backlog": "refine-details.md",
            "brain-test-skill": "skill-testing-details.md",
            "write-human": "human-writing-details.md",
        }
        for skill, name in pairs.items():
            with self.subTest(skill=skill):
                doc = ROOT / skill / "references" / name
                self.assertTrue(doc.is_file())
                self.assertGreater(len(doc.read_text(encoding="utf-8")), 500)


if __name__ == "__main__":
    unittest.main()
