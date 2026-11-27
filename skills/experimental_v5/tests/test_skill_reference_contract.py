"""Static contract for bundled skill-file references and removed skill names."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = tuple(sorted(ROOT.glob("brain-*/SKILL.md")))
SKILL_REF = re.compile(r"\$\{CLAUDE_SKILL_DIR\}/((?:\.\./)*[\w./-]+\.(?:md|py|sh|js|cjs|html))")


class SkillReferenceContract(unittest.TestCase):
    def test_referenced_bundled_files_exist(self):
        self.assertTrue(SKILLS, "No skills discovered")
        for skill in SKILLS:
            body = skill.read_text(encoding="utf-8")
            for relative in SKILL_REF.findall(body):
                with self.subTest(skill=skill.parent.name, referenced=relative):
                    self.assertTrue((skill.parent / relative).is_file(),
                                    f"{skill} references missing file {relative}")

    @unittest.skip("Legacy v4 instruction contract superseded; see test_v5_workflow.py")

    def test_worked_example_is_packaged_with_brain_init(self):
        example = ROOT / "brain-init" / "references" / "start-machine-example.md"
        self.assertTrue(example.is_file())
        body = example.read_text(encoding="utf-8")
        for required in (
            "SPEC-001#REQ-001",
            "SPEC-001#REQ-002",
            "SPEC-001#REQ-003",
            "TASK-001",
            "TASK-002",
            ".brain/adrs/",
            "execution.md",
            "not a verified software implementation",
        ):
            with self.subTest(required=required):
                self.assertIn(required, body)

    def test_shared_validator_is_packaged_inside_brain_init(self):
        self.assertTrue((ROOT / "brain-init" / "scripts" / "validate_feature_docs.py").is_file())
        self.assertFalse((ROOT / "scripts" / "validate_feature_docs.py").exists())

    def test_no_old_ticket_writer_called(self):
        for skill in SKILLS:
            with self.subTest(skill=skill.parent.name):
                self.assertNotIn("brain-write-tickets", skill.read_text(encoding="utf-8"))
        self.assertFalse((ROOT / "brain-write-tickets" / "SKILL.md").exists())
        self.assertTrue((ROOT / "brain-write-tasks" / "SKILL.md").exists())

    @unittest.skip("Legacy v4 instruction contract superseded; see test_v5_workflow.py")

    def test_new_producers_use_canonical_feature_paths(self):
        cases = {
            "brain-brainstorm": "01-brief/",
            "brain-write-spec": "02-specifications/",
            "brain-decompose-feature": "03-components/",
            "brain-design-implementation": "04-implementation-plans/",
            "brain-write-tasks": "05-tasks/",
            "brain-implement": "execution.md",
        }
        for skill, path_part in cases.items():
            with self.subTest(skill=skill):
                self.assertIn(path_part, (ROOT / skill / "SKILL.md").read_text())


if __name__ == "__main__":
    unittest.main()
