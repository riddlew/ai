# Work Reconstruction

Use after implementation when a developer needs to understand and independently explain the finished change. This prompt narrows the `verify-handoff` skill to reconstruction rather than repeating its verification procedure.

## Prompt Template

```text
Use the verify-handoff skill to reconstruct the completed change.

Work item: [ISSUE-ID or work-item name]
Result directory: [path under .claude/results]
Change boundary: [commit, branch, pull request, or working-tree diff]
Audience: [developer experience level or reviewer role]

Read the investigation, approved combined plan, implementation record, relevant
diagnoses and reviews, final diff, and surrounding code. Explain the change in
implementation order, covering the end-to-end data flow, control flow, ownership
or state changes, important decisions, failure handling, and why each significant
file changed. Connect claims to repository evidence and distinguish approved
intent from behavior verified by tests or runtime checks.

Add the reconstruction to the verification and handoff artifact. Do not modify
source code or claim behavior that the available evidence does not establish.
Flag stale artifacts, unexplained changes, or gaps that prevent a trustworthy
reconstruction.
```

## Example

```text
Use the verify-handoff skill to reconstruct the completed change.

Work item: PAY-1842
Result directory: .claude/results/PAY-1842
Change boundary: Current branch compared with main
Audience: Backend engineer reviewing the payment retry behavior

Read the investigation, approved combined plan, implementation record, relevant
diagnoses and reviews, final diff, and surrounding code. Explain the change in
implementation order, covering how the checkout request produces a stable
idempotency key, how retries reuse it, how the provider response is handled, and
how failure and concurrent-request paths behave. Explain why each significant
file changed and connect claims to repository evidence and executed checks.

Add the reconstruction to the verification and handoff artifact. Do not modify
source code or claim behavior that the available evidence does not establish.
Flag stale artifacts, unexplained changes, or gaps that prevent a trustworthy
reconstruction.
```
