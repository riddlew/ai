# Optional Hardening

Use this only after the root cause is identified or fixed, when the bad value crossed several layers before it caused a failure. The fix at the source stays the fix; hardening is extra.

## Layers to consider

- **Entry validation:** reject clearly invalid input at the boundary where it enters, with a clear error.
- **Business-logic checks:** assert that data makes sense for the specific operation, so a wrong value fails near where it was introduced.
- **Environment guards:** refuse dangerous operations in contexts where they are never right, such as writing outside a temporary directory during tests.
- **Diagnostics:** log context (arguments, caller, environment) before a risky operation, so a future failure is quick to trace.

Choose only the layers that would have caught this particular bug. Naming all four is not required.

## Opt-in only

Hardening adds code, behavior, and maintenance that the bug fix did not require. `CLAUDE.local.md` prefers the smallest coherent solution, and new validation can change error behavior or contracts.

- Never apply hardening unasked.
- Propose it in the report as `Optional hardening (not applied):`, naming each layer, where it would go, and what it would have caught.
- Wait for the user's approval before changing anything. If they approve, treat each addition as a separate change with its own test, and verify that existing behavior is unchanged.
- If the fix at the source is sufficient and the value crossed only one layer, do not offer it.
