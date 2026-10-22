# Backlog refinement checklist

Use this to prompt useful questions, **not** to enforce a checklist on every story. A story can be ready without documenting every item here.

| Area | Look for | Useful suggestion when genuinely relevant |
| --- | --- | --- |
| Outcome | Who benefits? What observable outcome is expected? | Ask for the success condition without inventing a persona. |
| Scope | Which behavior is included, excluded, and changed? | Clarify boundaries and compatibility needs. |
| Acceptance criteria | Can a tester independently decide pass/fail? | Propose Given/When/Then examples with explicit expected behavior. |
| Negative paths | What happens on validation failure, empty input, timeout, or partial completion? | Ask for a decision or suggest a test scenario. |
| Authorization/privacy | Are roles, access, sensitive fields, and logs relevant? | Ask who can access data; don't assume the policy. |
| Integration dependencies | Do linked issues, APIs, teams, or contracts affect delivery? | Cite linked tickets and distinguish potential dependencies. |
| Nonfunctional requirements | Are performance, accessibility, usability, reliability, or observability material? | Ask about the constraint only if the feature implies it. |
| Testability | Are expected results and test fixtures knowable? | Propose a precise example/fixture. |
| Slicing | Can a large request yield incremental user value? | Suggest vertical slices with acceptance criteria, not technical-layer splits alone. |

Severity:
- **Blocking refinement:** the team cannot determine what to build or how to verify the main behavior.
- **Worth clarifying:** plausible material ambiguity that should be addressed before implementation.
- **Minor:** useful follow-up that should not block refinement.

Confidence reflects completeness and directness of retrieved evidence:
- **High:** source contains explicit behavior and relevant criteria.
- **Medium:** source partly supports the interpretation; at least one substantive ambiguity remains.
- **Low:** the description or relevant fields are unavailable, truncated, or too vague for a firm assessment.
