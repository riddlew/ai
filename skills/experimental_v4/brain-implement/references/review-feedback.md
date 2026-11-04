# Handling review feedback

Use these rules for every review finding, whether you are the main session or an implementer in a fix round.

1. Read all findings before changing anything.
2. Verify each finding against the code and the governing spec before acting.
3. Decide per finding:
   - Correct: fix it.
   - Wrong: push back with evidence, such as `file:line` or test output.
   - Unclear: ask the reviewer. If the answer is consequential under the root `CLAUDE.md`, ask the user.
4. Skip performative agreement. Do not write "you're right", "great catch", or similar before verifying. State what changed, or why nothing did.
5. Apply YAGNI. Before adding a capability a reviewer suggests, check that a requirement or real use needs it. If none does, say so and leave it out.
6. Fix in severity order, Critical first. Rerun the covering tests after each fix. For behavior fixes, write the failing test first.

Report each finding as fixed, pushed back (with evidence), or asked (with the question).
