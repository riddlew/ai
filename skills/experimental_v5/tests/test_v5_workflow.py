"""V5 workflow and cross-runtime regression contracts."""
from __future__ import annotations
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "brain-init/scripts/validate_feature_docs.py"
TOOL = ROOT / "brain-init/scripts/brain-tool"
POLICY = ROOT / "brain-init/references/CLAUDE.local.md"

def run(*args, env=None, check=True):
    p = subprocess.run([str(a) for a in args], capture_output=True, text=True,
                       env={**os.environ, **(env or {})})
    if check and p.returncode:
        raise AssertionError(f"{args}:\n{p.stdout}\n{p.stderr}")
    return p

def doc(root: Path, folder: str, name: str, identity: str, kind: str,
        parents=(), requirements=(), depends=(), amends=(), supersedes=(), body=""):
    target = root / folder / name
    target.parent.mkdir(parents=True, exist_ok=True)
    def value(xs):
        return "[" + ", ".join(xs) + "]"
    target.write_text("---\n" +
        f"id: {identity}\nkind: {kind}\nparents: {value(parents)}\n" +
        f"requirements: {value(requirements)}\ndepends_on: {value(depends)}\n" +
        (f"amends: {value(amends)}\nsupersedes: {value(supersedes)}\n" if amends or supersedes else "") +
        "---\n# Document\n" + body, encoding="utf-8")
    return target

class V5FeatureContract(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / ".brain" / "features" / "demo"

    def validate(self, valid=True, coverage=False):
        p = run("python3", VALIDATOR, self.root.parent,
                *(["--check-coverage"] if coverage else []), check=False)
        self.assertEqual(p.returncode, 0 if valid else 1, p.stdout + p.stderr)
        return p.stdout + p.stderr

    def test_no_documents_needed(self):
        self.validate()

    def test_no_approval_or_parent_hash_required(self):
        doc(self.root, "02-specifications", "a.md", "SPEC-001", "specification", body="- REQ-001: must work\n")
        doc(self.root, "04-implementation-plans", "b.md", "PLAN-001", "implementation-plan",
            requirements=["SPEC-001#REQ-001"])
        self.validate()

    def test_historical_v4_approval_metadata_is_inert(self):
        p = doc(self.root, "02-specifications", "a.md", "SPEC-001", "specification",
                body="- REQ-001: expected\n")
        p.write_text(p.read_text().replace("kind: specification\n", "kind: specification\nstatus: needs-revision\nparent_hashes: [SPEC-999@000]\n"))
        self.validate()

    def test_invalid_parent_and_unknown_requirement_fail(self):
        doc(self.root, "04-implementation-plans", "bad.md", "PLAN-001", "implementation-plan",
            parents=["SPEC-999"], requirements=["SPEC-001#REQ-001"])
        out = self.validate(False)
        self.assertIn("unknown parent", out)
        self.assertIn("unknown requirement", out)

    def test_valid_focused_amendment(self):
        doc(self.root, "04-implementation-plans", "first.md", "PLAN-001", "implementation-plan",
            body="- dispatch-strategy: synchronous\n")
        doc(self.root, "04-implementation-plans", "second.md", "PLAN-002", "implementation-plan",
            amends=["PLAN-001"], supersedes=["PLAN-001#dispatch-strategy"],
            body="- dispatch-strategy: asynchronous\n")
        self.validate()

    def test_conflicting_amendments_detected(self):
        doc(self.root, "04-implementation-plans", "first.md", "PLAN-001", "implementation-plan",
            body="- dispatch-strategy: synchronous\n")
        for index in (2, 3):
            doc(self.root, "04-implementation-plans", f"{index}.md", f"PLAN-{index:03}",
                "implementation-plan", amends=["PLAN-001"],
                supersedes=["PLAN-001#dispatch-strategy"])
        self.assertIn("conflicting supersession", self.validate(False))

    def test_missing_supersession_anchor_detected(self):
        doc(self.root, "04-implementation-plans", "first.md", "PLAN-001", "implementation-plan")
        doc(self.root, "04-implementation-plans", "second.md", "PLAN-002", "implementation-plan",
            amends=["PLAN-001"], supersedes=["PLAN-001#not-real"])
        self.assertIn("anchor not found", self.validate(False))

    def test_amendment_cycle_detected(self):
        doc(self.root, "04-implementation-plans", "first.md", "PLAN-001", "implementation-plan",
            amends=["PLAN-002"], supersedes=["PLAN-002#strategy"], body="- strategy: one\n")
        doc(self.root, "04-implementation-plans", "second.md", "PLAN-002", "implementation-plan",
            amends=["PLAN-001"], supersedes=["PLAN-001#strategy"], body="- strategy: two\n")
        self.assertIn("cycle", self.validate(False))

    def test_requirement_coverage_checks_only_existing_stage(self):
        doc(self.root, "02-specifications", "a.md", "SPEC-001", "specification",
            body="- REQ-001: first\n- REQ-002: second\n")
        self.validate(coverage=True)
        doc(self.root, "04-implementation-plans", "p.md", "PLAN-001", "implementation-plan",
            requirements=["SPEC-001#REQ-001"])
        self.assertIn("no document covers SPEC-001#REQ-002", self.validate(False, coverage=True))

@unittest.skipUnless(shutil.which("node") and shutil.which("python3") and shutil.which("git"),
                     "requires Python, Node and Git for deterministic runtime parity")
class V5RuntimeContract(unittest.TestCase):
    def test_optional_doc_scaffolding_all_runtimes(self):
        for runtime in ("python", "node", "sh"):
            with self.subTest(runtime=runtime), tempfile.TemporaryDirectory() as temp:
                repo = Path(temp)
                run("git", "init", "-q", repo)
                run("git", "-C", repo, "-c", "user.name=CI", "-c", "user.email=ci@example.com",
                    "commit", "--allow-empty", "-qm", "baseline")
                brain = repo / ".brain"
                common = ("--apply", "--authorized-root", repo)
                env = {"BRAIN_RUNTIME": runtime}
                run("sh", TOOL, "init", "--brain", brain, "--repo", repo,
                    "--tracking", "tracked", *common, env=env)
                run("sh", TOOL, "doc", "--brain", brain, "--feature", "demo", "--kind",
                    "plan", "--slug", "direct", *common, env=env)
                plan = brain / "features/demo/04-implementation-plans/direct.md"
                self.assertTrue(plan.exists())
                self.assertIn("id: PLAN-001", plan.read_text())
                self.assertNotIn("status:", plan.read_text())
                self.assertNotIn("parent_hashes:", plan.read_text())
                p = run("sh", TOOL, "validate", "--brain", brain, env=env)
                self.assertIn("VALID feature documents", p.stdout)

    def test_cross_runtime_amendment_conflict(self):
        for runtime in ("python", "node", "sh"):
            with self.subTest(runtime=runtime), tempfile.TemporaryDirectory() as temp:
                brain = Path(temp) / ".brain"
                feature = brain / "features/demo"
                doc(feature, "04-implementation-plans", "one.md", "PLAN-001", "implementation-plan",
                    body="- strategy: initial\n")
                for n in (2, 3):
                    doc(feature, "04-implementation-plans", f"{n}.md", f"PLAN-{n:03}",
                        "implementation-plan", amends=["PLAN-001"],
                        supersedes=["PLAN-001#strategy"])
                p = run("sh", TOOL, "validate", "--brain", brain,
                        env={"BRAIN_RUNTIME": runtime}, check=False)
                self.assertNotEqual(p.returncode, 0, p.stdout + p.stderr)

class V5SkillPolicy(unittest.TestCase):
    def test_direct_implementation_is_first_class(self):
        impl = (ROOT / "brain-implement/SKILL.md").read_text()
        self.assertIn("No spec, plan, task list", impl)
        self.assertIn("inline is default", impl)
        self.assertIn("Stop when requested behavior", impl)

    def test_brain_update_is_explicitly_manual(self):
        update = (ROOT / "brain-update/SKILL.md").read_text()
        self.assertIn("disable-model-invocation: true", update)
        self.assertIn("only when the user explicitly invokes", update)
        policy = POLICY.read_text()
        self.assertIn("No skill automatically invokes", policy)

    def test_modes_and_optional_compact(self):
        pair = (ROOT / "brain-pair-program/SKILL.md").read_text()
        for mode in ("AI-led", "Developer-led", "Learning Mode"):
            self.assertIn(mode, pair)
        compact = (ROOT / "brain-compact/SKILL.md").read_text()
        self.assertIn("disable-model-invocation: true", compact)
        self.assertIn("Preview first", compact)

    def test_project_version_and_handoff(self):
        self.assertIn("Brain workflow version: experimental_v5", POLICY.read_text())
        self.assertIn("handoff.md", (ROOT / "brain-init/references/feature-document-contract.md").read_text())
        self.assertIn("one authoritative", POLICY.read_text().lower())

if __name__ == "__main__":
    unittest.main()
