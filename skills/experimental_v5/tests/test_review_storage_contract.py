"""Static guardrails for the review report layout; not an agent behavior test."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KINDS = {
    "architecture": "brain-review-architecture",
    "code": "brain-review-code",
    "merge-request": "brain-review-merge-request",
    "security": "brain-review-security",
}


class ReviewStorageContract(unittest.TestCase):
    def test_all_review_skills_use_nested_reports_and_shared_rules(self):
        for kind, skill in KINDS.items():
            with self.subTest(kind=kind):
                content = (ROOT / skill / "SKILL.md").read_text()
                self.assertIn("references/report-storage.md", content)
                self.assertIn(f".brain/reviews/{kind}/<NN>-<short-slug>/review.md", content)
                self.assertNotRegex(content, rf"\.brain/reviews/{re.escape(kind)}/<NN>-<short-slug>\.md")

    def test_code_review_preserves_three_assessments_with_proportional_repo_fit(self):
        skill = (ROOT / "brain-review-code/SKILL.md").read_text(encoding="utf-8")
        details = (ROOT / "brain-review-code/references/code-review-details.md").read_text(encoding="utf-8")
        for assessment in ("Correctness", "Requirement fit", "Repository fit"):
            with self.subTest(assessment=assessment):
                self.assertIn(f"### {assessment}", details)
        self.assertIn("scope Repository fit proportionally", skill)
        self.assertIn("Always perform this third assessment", details)
        self.assertIn("small localized change", details)
        self.assertIn("deeper structural analysis only when", details)
        self.assertIn("complete Requirement fit coverage unchanged", details)
        self.assertIn("one status row for each in-scope Example", skill)
        self.assertIn("Only if the user selected subagents", details)

    def test_code_review_uses_current_brain_document_paths(self):
        skill = (ROOT / "brain-review-code/SKILL.md").read_text(encoding="utf-8")
        details = (ROOT / "brain-review-code/references/code-review-details.md").read_text(encoding="utf-8")
        self.assertIn(".brain/features/<feature-slug>/02-specifications/", skill)
        self.assertIn(".brain/features/<feature-slug>/02-specifications/", details)
        self.assertIn(".brain/features/<feature-slug>/execution.md", details)
        self.assertIn("05-tasks/", details)
        self.assertNotIn(".brain/specs/", details)
        self.assertNotIn(".brain/impl_plans/", details)

    def test_shared_rules_cover_legacy_and_baseline(self):
        storage = (ROOT / "brain-review-code/references/report-storage.md").read_text()
        for phrase in ("legacy flat", "Never overwrite", "relevant previous", "brain-update"):
            self.assertIn(phrase, storage)

    def test_architecture_continuity_and_persistence(self):
        architecture = (ROOT / "brain-review-architecture/SKILL.md").read_text()
        policy = (ROOT / "brain-init/references/CLAUDE.local.md").read_text()
        for phrase in ("coverage summary", "still supported", "resolved", "no longer applicable", "unverified", "by default"):
            self.assertIn(phrase, architecture)
        self.assertIn("standalone `brain-review-architecture` saves a baseline by default", policy)
        self.assertIn("invoked solely as a specialist", architecture)

    def test_template_preserves_nested_review_layout_without_legacy_migration(self):
        template = (ROOT / "brain-update/references/templates.md").read_text()
        initializer = (ROOT / "brain-init/SKILL.md").read_text()
        self.assertIn("`reviews/architecture/01-<slug>/review.md`", template)
        self.assertIn("Do not move, import, or translate legacy feature documents", initializer)


if __name__ == "__main__":
    unittest.main()
