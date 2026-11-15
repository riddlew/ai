"""Static hierarchy-contract tests; no agent behavior is asserted."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "brain-init" / "scripts" / "validate_feature_docs.py"
spec = importlib.util.spec_from_file_location("feature_validator", SCRIPT)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)

LEVELS = {
    "brief": "01-brief",
    "specification": "02-specifications",
    "component": "03-components",
    "implementation-plan": "04-implementation-plans",
    "task": "05-tasks",
}


class FeatureDocumentContract(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.feature = Path(self.temp.name) / "features" / "start-machine"
        self.feature.mkdir(parents=True)
        self.write("BRF-001", "brief")
        self.write("SPEC-001", "specification", parents=["BRF-001"],
                   body="# Spec\n\n## Requirements\n- REQ-001: StartMachine is accepted\n- REQ-002: Invalid requests are rejected")
        self.write("CMP-001", "component", parents=["SPEC-001"],
                   requirements=["SPEC-001#REQ-001", "SPEC-001#REQ-002"])
        self.write("PLAN-001", "implementation-plan", parents=["CMP-001"],
                   requirements=["SPEC-001#REQ-001", "SPEC-001#REQ-002"])
        self.write("TASK-001", "task", parents=["PLAN-001"],
                   requirements=["SPEC-001#REQ-001", "SPEC-001#REQ-002"])

    def write(self, doc_id, kind, parents=None, requirements=None, depends_on=None,
              status="approved", body="# Example"):
        def yaml_list(values):
            return "[" + ", ".join(values or []) + "]"
        parent_hashes = []
        for parent in parents or []:
            for parent_kind, directory in LEVELS.items():
                parent_file = self.feature / directory / f"{parent}.md"
                if parent_file.exists():
                    parent_hashes.append(f"{parent}@{validator.git_blob_sha(parent_file)}")
                    break
        content = (f"---\nid: {doc_id}\nkind: {kind}\nstatus: {status}\n"
                   f"parents: {yaml_list(parents)}\n"
                   f"requirements: {yaml_list(requirements)}\n"
                   f"depends_on: {yaml_list(depends_on)}\n"
                   f"parent_hashes: {yaml_list(parent_hashes)}\n---\n{body}\n")
        directory = self.feature / LEVELS[kind]
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / f"{doc_id}.md"
        path.write_text(content, encoding="utf-8")
        return path

    def test_valid_full_hierarchy_and_coverage(self):
        self.assertEqual([], validator.validate_feature(self.feature, True))

    def test_broken_parent_is_rejected(self):
        self.write("TASK-002", "task", parents=["PLAN-999"])
        self.assertIn("unknown parent PLAN-999", "\n".join(validator.validate_feature(self.feature)))

    def test_wrong_level_parent_is_rejected(self):
        self.write("TASK-002", "task", parents=["TASK-001"])
        self.assertIn("must be from an earlier level",
                      "\n".join(validator.validate_feature(self.feature)))

    def test_dependency_cycle_is_rejected(self):
        self.write("TASK-001", "task", parents=["PLAN-001"], depends_on=["TASK-002"])
        self.write("TASK-002", "task", parents=["PLAN-001"], depends_on=["TASK-001"])
        self.assertIn("dependency cycle", "\n".join(validator.validate_feature(self.feature)))

    def test_unknown_requirement_is_rejected(self):
        self.write("TASK-002", "task", parents=["PLAN-001"],
                   requirements=["SPEC-001#REQ-999"])
        self.assertIn("unknown requirement SPEC-001#REQ-999",
                      "\n".join(validator.validate_feature(self.feature)))

    def test_uncovered_requirement_is_rejected_when_checking_coverage(self):
        self.write("TASK-001", "task", parents=["PLAN-001"],
                   requirements=["SPEC-001#REQ-001"])
        self.assertIn("no approved document covers SPEC-001#REQ-002",
                      "\n".join(validator.validate_feature(self.feature, True)))
        self.assertEqual([], validator.validate_feature(self.feature, False))

    def test_skipped_middle_levels_are_allowed(self):
        for level in ("03-components", "04-implementation-plans"):
            for path in (self.feature / level).glob("*.md"):
                path.unlink()
        self.write("TASK-001", "task", parents=["SPEC-001"],
                   requirements=["SPEC-001#REQ-001", "SPEC-001#REQ-002"])
        self.assertEqual([], validator.validate_feature(self.feature, True))

    def test_approved_child_rejects_unapproved_parent(self):
        self.write("PLAN-001", "implementation-plan", parents=["CMP-001"],
                   requirements=["SPEC-001#REQ-001", "SPEC-001#REQ-002"],
                   status="needs-revision")
        self.assertIn("approved document has unapproved parent PLAN-001",
                      "\n".join(validator.validate_feature(self.feature)))

    def test_requirement_must_be_in_parent_scope(self):
        self.write("CMP-001", "component", parents=["SPEC-001"],
                   requirements=["SPEC-001#REQ-001"])
        self.assertIn("not supported by a parent",
                      "\n".join(validator.validate_feature(self.feature)))

    def test_duplicate_spec_requirements_are_rejected(self):
        self.write("SPEC-001", "specification", parents=["BRF-001"],
                   body="- REQ-001: First rule\n- REQ-001: Conflicting rule")
        self.assertIn("duplicate declared requirement ID",
                      "\n".join(validator.validate_feature(self.feature)))

    def test_partial_draft_stage_does_not_claim_total_coverage(self):
        self.write("CMP-001", "component", parents=["SPEC-001"],
                   requirements=["SPEC-001#REQ-001"])
        self.write("CMP-002", "component", parents=["SPEC-001"],
                   requirements=["SPEC-001#REQ-002"], status="draft")
        errors = validator.validate_feature(self.feature, True)
        self.assertFalse(any("03-components" in error and "no approved document covers"
                             in error for error in errors))

    def test_absent_features_directory_is_valid_empty_brain(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual([], validator.validate_features(Path(tmp) / ".brain" / "features", True))

    def test_non_directory_features_path_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / "features"
            file.write_text("not a directory")
            self.assertIn("expected directory", "\n".join(validator.validate_features(file)))

    def test_approved_task_rejects_unapproved_dependency(self):
        self.write("TASK-002", "task", parents=["PLAN-001"],
                   requirements=["SPEC-001#REQ-001"], status="draft")
        self.write("TASK-001", "task", parents=["PLAN-001"],
                   requirements=["SPEC-001#REQ-001", "SPEC-001#REQ-002"],
                   depends_on=["TASK-002"])
        self.assertIn("approved document has unapproved dependency TASK-002",
                      "\n".join(validator.validate_feature(self.feature)))

    def test_parent_revision_invalidates_approved_children(self):
        spec = self.feature / "02-specifications" / "SPEC-001.md"
        spec.write_text(spec.read_text() + "\nAn approved behavior changed.\n")
        errors = "\n".join(validator.validate_feature(self.feature))
        self.assertIn("stale parent hash for SPEC-001", errors)

    def test_approved_child_needs_parent_hash(self):
        path = self.feature / "03-components" / "CMP-001.md"
        content = path.read_text()
        content = content.replace("parent_hashes: [SPEC-001@", "parent_hashes: [INVALID@")
        path.write_text(content)
        errors = "\\n".join(validator.validate_feature(self.feature))
        self.assertIn("approved document missing parent hash for SPEC-001", errors)

    def test_hash_helper_reports_current_parent(self):
        child = self.feature / "03-components" / "CMP-001.md"
        self.assertEqual(
            [f"SPEC-001@{validator.git_blob_sha(self.feature / '02-specifications' / 'SPEC-001.md')}"],
            validator.describe_parent_hashes(child),
        )

    def test_block_yaml_list_is_supported(self):
        path = self.feature / "05-tasks" / "TASK-001.md"
        content = path.read_text().replace("parents: [PLAN-001]",
                                             "parents:\n  - PLAN-001")
        path.write_text(content)
        self.assertEqual([], validator.validate_feature(self.feature))


if __name__ == "__main__":
    unittest.main()
