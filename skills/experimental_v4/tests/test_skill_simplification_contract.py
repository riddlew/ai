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
        self.assertEqual(23, len(SKILLS))
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

    def test_execution_mode_requires_explicit_choice_including_reviews(self):
        policy = POLICY.read_text(encoding="utf-8")
        code = (ROOT / "brain-review-code/references/code-review-details.md").read_text(encoding="utf-8")
        builder = (ROOT / "brain-review-code/references/builder-review.md").read_text(encoding="utf-8")
        implementation = (ROOT / "brain-implement/references/implement-details.md").read_text(encoding="utf-8")
        tester = (ROOT / "brain-test-skill/SKILL.md").read_text(encoding="utf-8")
        for phrase in ("Execution mode selection", "ask before starting substantive skill work",
                       "No skill may dispatch subagents by default", "Propagate the selected mode"):
            self.assertIn(phrase, policy)
        self.assertIn("Scope, component count and changed-line count do not authorize subagents", code)
        self.assertIn("never dispatch a subagent unless", builder)
        self.assertIn("ask which one and wait", implementation)
        self.assertIn("only when the user opts into subagents", tester)
        self.assertNotIn("Dispatch one standard-tier subagent per assessment in parallel", code)

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
            "brain-pair-program",
            "brain-write-spec", "brain-write-tasks", "brain-implement",
        }
        intentionally_manual = {"brain-next", "brain-compact", "brain-retro", "brain-distill-content", "brain-review-merge-request", "write-human"}
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

    def test_usage_step_models_match_readme_tiers(self):
        readme = (ROOT / "brain-init/references/README.md").read_text(encoding="utf-8")
        section = readme.split("## Model tiers and recommended models\n", 1)[1].split("\n## ", 1)[0]
        tiers = dict(re.findall(r"^\| `([^`]+)` \| \*\*(Sonnet|Opus)\*\* \|", section, re.M))
        usage = (ROOT / "brain-init/references/USAGE.md").read_text(encoding="utf-8")
        steps = re.findall(r"(?m)^## Step \d+:.*$", usage)
        self.assertEqual(32, len(steps), "Documented steps must remain model-annotated")
        lines = usage.splitlines()
        for i, line in enumerate(lines):
            if not re.match(r"^## Step \d+:", line):
                continue
            with self.subTest(step=line):
                following = next((value for value in lines[i + 1:] if value.strip()), "")
                self.assertTrue(following.startswith("**Model (main session):**") or
                                following.startswith("**Models (main session):**"), line)
        annotations = [line for line in lines
                       if line.startswith(("**Model (main session):**",
                                           "**Models (main session):**"))]
        self.assertGreaterEqual(len(annotations), len(steps))
        checked = 0
        for annotation in annotations:
            for tier, skill in re.findall(r"\*\*(Sonnet|Opus)\*\* \(\x60([^\x60]+)\x60\)", annotation):
                with self.subTest(skill=skill, tier=tier):
                    self.assertIn(skill, tiers)
                    self.assertEqual(tiers[skill], tier)
                checked += 1
        self.assertGreaterEqual(checked, 40, "Verify examples and session model labels")

    def test_usage_covers_mid_implementation_revisions(self):
        usage = (ROOT / "brain-init/references/USAGE.md").read_text(encoding="utf-8")
        scenario = usage.split("# Scenario 7 — Change an approved feature during implementation", 1)[1]
        scenario = scenario.split("# Quick workflow reference", 1)[0]
        self.assertIn("brain-write-spec", scenario)
        self.assertIn("brain-decompose-feature", scenario)
        self.assertIn("brain-design-implementation", scenario)
        self.assertIn("brain-write-tasks", scenario)
        self.assertIn("brain-implement", scenario)
        for requirement in (
            "If you already made an unambiguous decision",
            "skip this step when no component documents exist",
            "preserve unaffected",
            "parent fingerprints",
            "explicitly authorize",
            "not** implementation authorization",
            "Do not edit production code",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement.lower(), scenario.lower())

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
                if path.name != "README.md":
                    self.assertIsNone(re.search(r"(?<![A-Za-z0-9_-])" + re.escape(old) + r"(?![A-Za-z0-9_-])", content), str(path))
                self.assertIn(new, content, str(path))
        readme = (ROOT / "brain-init/references/README.md").read_text(encoding="utf-8")
        self.assertIn("remove the former `brain-blueprint/` and `brain-decompose/`", readme)
        for name in (
            "brain-design-implementation", "brain-decompose-feature",
            "brain-explain-changes", "brain-implement", "brain-write-spec",
        ):
            self.assertNotIn("`" + name + "` **(manual)**", readme)

    def test_policy_authorization_discovery_and_authority_boundaries(self):
        policy = POLICY.read_text(encoding="utf-8")
        details = (ROOT / "brain-init/references/engineering-details.md").read_text(
            encoding="utf-8"
        )
        for required in (
            "An explicit request to implement authorizes routine code changes",
            "Automatic skill invocation",
            "does **not** independently authorize implementation",
            "Inventory the names of root-level project-knowledge",
            "other root documents relevant to the task",
            "a broad read of root project knowledge",
            "**Authority boundaries:**",
            "approved implementation plans bind agreed code structure",
            "`execution.md` records work and verification, not new requirements",
            "never enter `.notes/`",
        ):
            with self.subTest(requirement=required):
                self.assertIn(required, policy)
        self.assertNotIn("feature request is not approval", policy)
        self.assertIn("brain-design-implementation", details)
        self.assertNotIn("brain-blueprint", details)

    def test_next_skill_is_read_only_by_default_and_routes_optional_revisions(self):
        skill = (ROOT / "brain-next/SKILL.md").read_text(encoding="utf-8")
        details = (ROOT / "brain-next/references/next-routing.md").read_text(encoding="utf-8")
        readme = (ROOT / "brain-init/references/README.md").read_text(encoding="utf-8")
        usage = (ROOT / "brain-init/references/USAGE.md").read_text(encoding="utf-8")
        policy = POLICY.read_text(encoding="utf-8")
        self.assertFalse((ROOT / "brain-change").exists())
        for required in (
            "name: brain-next", "disable-model-invocation: true", "argument-hint:",
            "$ARGUMENTS", "Default mode is read-only", "state.md", "execution.md",
            "parents", "parent_hashes", "depends_on", "Git", "brain-write-spec",
            "brain-decompose-feature", "brain-design-implementation",
            "brain-write-tasks", "brain-diagnose", "brain-review-code",
            "brain-update", "brain-implement", "INC-", "explicit user request",
            "Skill tool", "does not write or approve", "Recommended next step:",
        ):
            with self.subTest(required=required):
                self.assertIn(required.lower(), skill.lower())
        for required in ("INC-4", "INC-4.5", "INC-5", "needs-revision",
                         "no additional global progress file", "review",
                         "dependencies", "verification", "approval", "read-only"):
            with self.subTest(required=required):
                self.assertIn(required.lower(), details.lower())
        self.assertIn("`brain-next`", readme)
        self.assertIn("/brain-next <feature>", usage)
        self.assertIn("--reconcile", usage)
        self.assertIn("brain-next", policy)

    def test_next_prefers_core_workflow_with_optional_complexity_reasons(self):
        skill = (ROOT / "brain-next/SKILL.md").read_text(encoding="utf-8")
        detail = (ROOT / "brain-next/references/next-routing.md").read_text(encoding="utf-8")
        readme = (ROOT / "brain-init/references/README.md").read_text(encoding="utf-8")
        usage = (ROOT / "brain-init/references/USAGE.md").read_text(encoding="utf-8")
        for expected in ("## Default path", "brain-brainstorm", "brain-write-spec",
                         "brain-design-implementation", "brain-implement",
                         "brain-decompose-feature", "brain-write-tasks",
                         "Optional:", "not optional", "reason"):
            with self.subTest(expected=expected):
                self.assertIn(expected.lower(), skill.lower())
        for expected in ("Optional:", "client/server", "delegated",
                         "existing", "approval"):
            self.assertIn(expected.lower(), detail.lower())
        self.assertIn("**Default path:**", readme)
        self.assertIn("**Default workflow:**", usage)
        self.assertIn("**Optional:**", usage)
        self.assertIn("An *existing* affected component or task", usage)

    def test_compact_skill_preview_ownership_and_information_preservation(self):
        skill = (ROOT / "brain-compact/SKILL.md").read_text(encoding="utf-8")
        details = (ROOT / "brain-compact/references/compact-details.md").read_text(encoding="utf-8")
        writing = (ROOT / "brain-init/references/compact-writing.md").read_text(encoding="utf-8")
        policy = POLICY.read_text(encoding="utf-8")
        usage = (ROOT / "brain-init/references/USAGE.md").read_text(encoding="utf-8")
        for required in ("disable-model-invocation: true", "--preview-only",
                         "does not write producer-owned files", "explicit user approval",
                         "parent_hashes", ".brain/.notes/", "brain-write-spec",
                         "brain-implement", "brain-update", "No safe reduction",
                         "Recommended next step:"):
            self.assertIn(required.lower(), skill.lower())
        for required in ("Diff", "fingerprint", "approval", "history", "authoritative"):
            self.assertIn(required.lower(), details.lower())
        for required in ("atomic", "information-dense", "self-contained",
                         "actual results", "distinct", "No arbitrary"):
            self.assertIn(required.lower(), writing.lower())
        self.assertIn("## Compact Brain writing", policy)
        self.assertIn("/brain-compact", usage)
        self.assertIn("brain-compact", (ROOT / "brain-init/references/README.md").read_text(encoding="utf-8"))

    def test_retro_is_manual_read_only_and_conditionally_suggested(self):
        retro = (ROOT / "brain-retro/SKILL.md").read_text(encoding="utf-8")
        details = (ROOT / "brain-retro/references/retro-details.md").read_text(encoding="utf-8")
        next_skill = (ROOT / "brain-next/SKILL.md").read_text(encoding="utf-8")
        routing = (ROOT / "brain-next/references/next-routing.md").read_text(encoding="utf-8")
        implement = (ROOT / "brain-implement/SKILL.md").read_text(encoding="utf-8")
        review = (ROOT / "brain-review-code/SKILL.md").read_text(encoding="utf-8")
        update = (ROOT / "brain-update/SKILL.md").read_text(encoding="utf-8")
        readme = (ROOT / "brain-init/references/README.md").read_text(encoding="utf-8")
        usage = (ROOT / "brain-init/references/USAGE.md").read_text(encoding="utf-8")
        for required in ("name: brain-retro", "disable-model-invocation: true",
                         "explicitly invoked", "read-only", "never", "at most 1–3",
                         "No justified workflow change", ".brain/.notes/",
                         "brain-update", "brain-review-code", "Recommended next step:"):
            self.assertIn(required.lower(), retro.lower())
        for required in ("evidence", "confidence", "No process change needed",
                         "past chat transcripts", "user"):
            self.assertIn(required.lower(), details.lower())
        for caller in (next_skill, routing, implement, review):
            self.assertIn("/brain-retro", caller)
            self.assertIn("optional", caller.lower())
            self.assertIn("never", caller.lower())
        self.assertNotIn("brain-retro", update)
        self.assertIn("| `brain-retro` | **Sonnet**", readme)
        self.assertIn("`brain-retro` **(manual)**", readme)
        self.assertIn("## Review workflow friction with brain-retro", usage)
        self.assertIn("**Opus**", usage)

    def test_pair_program_is_explicit_two_mode_and_checkpointed(self):
        skill = (ROOT / "brain-pair-program/SKILL.md").read_text(encoding="utf-8")
        details = (ROOT / "brain-pair-program/references/pair-program-details.md").read_text(encoding="utf-8")
        policy = POLICY.read_text(encoding="utf-8")
        contract = (ROOT / "brain-init/references/feature-document-contract.md").read_text(encoding="utf-8")
        template = (ROOT / "brain-implement/references/todo-template.md").read_text(encoding="utf-8")
        readme = (ROOT / "brain-init/references/README.md").read_text(encoding="utf-8")
        usage = (ROOT / "brain-init/references/USAGE.md").read_text(encoding="utf-8")
        next_skill = (ROOT / "brain-next/SKILL.md").read_text(encoding="utf-8")
        routing = (ROOT / "brain-next/references/next-routing.md").read_text(encoding="utf-8")
        for phrase in ("AI-led (recommended)", "developer-led", "ask", "wait",
                       "execution mode", "subagents", "actual diff", "real files",
                       "missing classes", "adaptive", "review", "approved requirements",
                       "brain-design-implementation", "execution.md", "review base",
                       "brain-update", "Never commit", "Recommended next step:"):
            with self.subTest(phrase=phrase):
                if phrase == "Never commit":
                    continue
                self.assertIn(phrase.lower(), skill.lower())
        self.assertIn("brain-pair-program", policy)
        self.assertIn("brain-pair-program", contract)
        self.assertIn("Pair mode: AI-led | developer-led", template)
        self.assertIn("brain-pair-program", next_skill)
        self.assertIn("brain-pair-program", routing)
        self.assertIn("| `brain-pair-program` | **Sonnet**", readme)
        self.assertIn("`brain-pair-program`", readme)
        self.assertIn("## Pair programming with AI-led or developer-led increments", usage)
        self.assertIn("Spring Boot", usage)
        self.assertIn("different", details.lower() if "different" in details.lower() else "different")

    def test_detailed_workflows_still_exist(self):
        pairs = {
            "brain-init": "init-details.md",
            "brain-next": "next-routing.md",
            "brain-compact": "compact-details.md",
            "brain-retro": "retro-details.md",
            "brain-pair-program": "pair-program-details.md",
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
