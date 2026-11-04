# `guidance.md` Template

Create `guidance.md` only when there are nontrivial discoveries a new session would otherwise need to rediscover. Never create an empty or boilerplate file. Keep entries concise and actionable.

```markdown
# External Communication — Implementation Guidance

## Where to Look

- `src/session.py` — owns connection state and application lifecycle
- `tests/test_session.py` — existing shutdown and connection test patterns

## Established Decisions

- Connection ownership stays in Session.
  Authority: `docs/specs/014-external-communication.md` (Technical Decisions).

## Verified Discoveries

- Session shutdown cancels pending reads before releasing the connection.
  Evidence: `src/session.py` shutdown path and existing shutdown test.
- The external client supports asynchronous reads.
  Evidence: client API usage in `src/service_client.py`.

## Implementation Caveats

- Preserve shutdown ordering when adding the receive path.

## Open Questions or Proposals

- None. (If present, label as unapproved and link to the blocker in `todo.md`.)
```

## Rules

- A code observation is evidence, not permission to change an approved ownership model.
- Label an unapproved idea as a proposal or open question, never as an established decision.
- Once an architectural choice is approved, update its specification, ADR, or domain record first, then adjust the reference here. Do not turn this file into an alternate ADR store.
- Edit or remove stale statements when implementation changes. Delete obsolete proposals, resolved caveats, duplicate explanations, and session narrative. Prefer pointers to sources over copied content. Remove the file if nothing useful remains.
