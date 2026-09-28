---
name: implement
description: Implement work from a specification or ticket set using the project's existing TDD and review-code workflows.
disable-model-invocation: true
---

# Implement

Implement the user-provided specification, tickets, or equivalent established requirements.

## Establish the implementation boundary

Before modifying production code:

1. Identify the specification, ticket set, or equivalent requirements governing the work.
2. Read the project's domain records, skipping any that do not exist:
   - root `CONTEXT-MAP.md`, to locate the relevant context's `CONTEXT.md`; otherwise root `CONTEXT.md`;
   - relevant ADRs in root `docs/adr/` and the relevant context's `docs/adr/`.

   Use the established domain vocabulary and treat applicable ADRs as constraints.
3. Create or switch to the implementation branch according to repository conventions.
4. Record the branch's current Git `HEAD` as the implementation base.

The recorded base defines the change set that `review-code` will review after implementation.

Do not replace it later with an inferred branch point or guessed base reference.

## Implement

Implement only the requested work.

At each TDD boundary, invoke `tdd`.

During implementation, repeatedly run:

- linting or equivalent static checks;
- relevant targeted tests.

Prefer targeted feedback during development rather than repeatedly running the complete test suite.

## Final validation

When implementation is complete:

1. run linting or equivalent static checks;
2. run all relevant targeted tests;
3. run the complete test suite once.

Do not proceed to final review while known validation failures remain unexplained.

## Commit

Commit the validated work before review. `review-code` reviews committed changes only, so uncommitted work would be invisible to it.

Follow repository branch and commit conventions when available.

## Review

Invoke `review-code` on the completed changes.

Provide it with:

- the implementation base recorded before changes began;
- the governing specification or ticket source when one exists;
- confirmation that the reviewed range is the work produced by this implementation session.

This invocation supplies an explicit workflow-established comparison base. `review-code` should not ask the user to choose another base unless the recorded base is invalid or no longer represents the intended implementation boundary.

Address review findings that fall within the authorized implementation scope. Rerun the relevant checks and commit the fixes.

If a finding requires a material redesign, broader scope, or a new product or architectural decision, surface it rather than silently expanding the implementation.

Do not consider the work complete until `review-code` has run.

## Rules

- Use `tdd` for test-driven development unless the user or governing requirements explicitly specify otherwise.
- Do not rely on the complete test suite as the primary feedback loop during implementation.
- Do not skip final full-suite validation.
- Preserve the implementation base captured before code changes.
- Pass that base explicitly to `review-code`; never make `review-code` infer it.
- Keep implementation within the established specification or ticket boundary.
- Follow repository branch, testing, and commit conventions when available.