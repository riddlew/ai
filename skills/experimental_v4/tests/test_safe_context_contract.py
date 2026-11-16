"""Conservative selective-context parity across Python, Node and POSIX shell."""
from __future__ import annotations
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = ROOT / "brain-init/scripts/brain-context"
RUNTIMES = ("python", "node", "sh")


def run(runtime, *args, ok=True):
    p = subprocess.run(["sh", str(LAUNCHER), *map(str, args)],
                       text=True, capture_output=True,
                       env={**os.environ, "BRAIN_RUNTIME": runtime})
    if ok and p.returncode:
        raise AssertionError((runtime, args, p.stdout, p.stderr))
    return p


def lines(result, key):
    return [line.split("\t", 1)[1] for line in result.stdout.splitlines()
            if line.startswith(key + "\t")]


@unittest.skipUnless(shutil.which("node") and shutil.which("git"),
                     "Node and Git needed for parity")
class SafeContextContract(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.brain = Path(temporary.name) / ".brain"
        self.brain.mkdir()
        self.documents = {
            "00_index.md": "# Index\n\n11_search.md is catalogued here.\n",
            "01_about.md": "# About\n",
            "03_architecture.md": "# Architecture\n",
            "09_user_decisions.md": "# Decisions\n",
            "state.md": "# State\n",
            "open_questions.md": "# Questions\n",
            "10_gateway.md": "# Payments\nSee knowledge/payments/rules.md.\n",
            "11_search.md": "# Search\nUnrelated search indexing.\n",
            "knowledge/payments/rules.md": "# Rules\nSource map: sources/payment-api.md.\n",
            "knowledge/payments/validation.md": "# Validation\nSee 10_gateway.md for invariants.\n",
            "sources/payment-api.md": "# API\nPayment protocol and source coverage.\n",
            "features/payments/02-specifications/settlement.md": "# Settlement\n",
            "pending/feature--payments.md": "# Pending\n",
        }
        for name, data in self.documents.items():
            target = self.brain / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(data)
        generated = run("python", "map", "--brain", self.brain).stdout
        mapping = []
        for row in generated.splitlines():
            if row.startswith("#"):
                mapping.append(row)
                continue
            cols = row.split("\t")
            name = cols[0]
            if name == "10_gateway.md":
                cols[1:3] = ["scoped", "path:src/payments/"]
            elif name == "11_search.md":
                cols[1:3] = ["scoped", "path:src/search/"]
            elif name == "09_user_decisions.md":
                cols[1:3] = ["scoped", "feature:search"]
            elif name.startswith(("knowledge/", "sources/")):
                cols[1:3] = ["scoped", "feature:billing"]
            mapping.append("\t".join(cols))
        (self.brain / "context-map.tsv").write_text("\n".join(mapping) + "\n")

    def outputs(self, action, *options, ok=True):
        results = [run(rt, action, "--brain", self.brain, *options, ok=ok)
                   for rt in RUNTIMES]
        if ok:
            self.assertEqual(results[0].stdout, results[1].stdout,
                             "Node differs from Python")
            self.assertEqual(results[0].stdout, results[2].stdout,
                             "shell differs from Python")
        return results

    def selected(self, *args):
        output = self.outputs("plan", *args)[0]
        return (lines(output, "MODE")[0], lines(output, "REASON")[0],
                set(lines(output, "READ")))

    def test_relevant_governing_docs_and_reverse_links(self):
        mode, reason, files = self.selected(
            "--feature", "payments", "--path", "src/payments/processor.py",
            "--branch", "feature/payments")
        self.assertEqual((mode, reason), ("selective", "mapped-and-linked"))
        required = {
            "00_index.md", "03_architecture.md", "09_user_decisions.md",
            "open_questions.md", "state.md", "10_gateway.md",
            "knowledge/payments/rules.md", "knowledge/payments/validation.md",
            "sources/payment-api.md",
            "features/payments/02-specifications/settlement.md",
            "pending/feature--payments.md",
        }
        self.assertTrue(required.issubset(files), required - files)
        self.assertNotIn("11_search.md", files)
        self.assertNotIn("README.md", files)

    def test_pending_is_branch_specific(self):
        mode, _, files = self.selected("--feature", "payments",
                                       "--path", "src/payments/service.py",
                                       "--branch", "main")
        self.assertEqual(mode, "selective")
        self.assertNotIn("pending/feature--payments.md", files)

    def test_unmapped_path_and_feature_force_full(self):
        mode, reason, files = self.selected("--path", "src/security/validator.py",
                                             "--branch", "main")
        self.assertEqual((mode, reason), ("full", "unmapped-code-path"))
        self.assertIn("11_search.md", files)
        mode, reason, _ = self.selected("--feature", "unregistered", "--branch", "main")
        self.assertEqual((mode, reason), ("full", "unmapped-feature"))

    def test_stale_or_missing_map_forces_full(self):
        map_file = self.brain / "context-map.tsv"
        map_file.unlink()
        mode, reason, _ = self.selected("--feature", "payments", "--branch", "main")
        self.assertEqual((mode, reason), ("full", "missing-map"))
        map_file.write_text(self.outputs("map")[0].stdout)
        (self.brain / "11_search.md").write_text("# Revised\n")
        mode, reason, files = self.selected("--feature", "payments", "--branch", "main")
        self.assertEqual((mode, reason), ("full", "stale-map"))
        self.assertIn("11_search.md", files)

    def test_new_root_knowledge_forces_full(self):
        (self.brain / "12_security.md").write_text("# Security\nCritical invariant.\n")
        mode, reason, files = self.selected("--feature", "payments", "--branch", "main")
        self.assertEqual((mode, reason), ("full", "incomplete-map"))
        self.assertIn("12_security.md", files)

    def test_unknown_branch_and_scope_force_full(self):
        mode, reason, _ = self.selected("--feature", "payments")
        self.assertEqual((mode, reason), ("full", "unknown-branch"))
        mode, reason, _ = self.selected("--branch", "main")
        self.assertEqual((mode, reason), ("full", "unknown-scope"))

    def test_duplicate_map_entry_forces_full(self):
        m = self.brain / "context-map.tsv"
        m.write_text(m.read_text() + "10_gateway.md\tglobal\t-\t" + "a"*40 + "\n")
        mode, reason, files = self.selected("--feature", "payments",
                                             "--path", "src/payments/service.py",
                                             "--branch", "main")
        self.assertEqual((mode, reason), ("full", "duplicate-map-path"))
        self.assertIn("11_search.md", files)

    def test_path_component_boundary_not_prefix(self):
        mode, reason, _ = self.selected("--path", "src/payments-old/process.py",
                                         "--branch", "main")
        self.assertEqual((mode, reason), ("full", "unmapped-code-path"))

    def test_generated_map_matches_all_runtimes(self):
        self.outputs("map")

    def test_invalid_paths_and_symlinks_rejected(self):
        for bad in ("../private", "/etc/passwd", "src/../../oops"):
            for runtime in RUNTIMES:
                p = run(runtime, "plan", "--brain", self.brain,
                        "--path", bad, ok=False)
                self.assertNotEqual(p.returncode, 0, (runtime, bad))
        external = self.brain.parent / "external.md"
        external.write_text("# External\n")
        (self.brain / "knowledge/escape.md").symlink_to(external)
        for runtime in RUNTIMES:
            p = run(runtime, "plan", "--brain", self.brain,
                    "--branch", "main", "--feature", "payments", ok=False)
            self.assertNotEqual(p.returncode, 0, runtime)


if __name__ == "__main__":
    unittest.main()
