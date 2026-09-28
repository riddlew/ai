---
name: tdd
description: Test-first red-green development through approved public boundaries. Invoked by the implement skill at each TDD boundary; do not invoke it independently.
user-invocable: false
---

# Test-Driven Development

Develop behavior incrementally through externally observable tests.

## Before writing tests

1. Read the project's domain records, skipping any that do not exist:
   - root `CONTEXT-MAP.md`, to locate the relevant context's `CONTEXT.md`; otherwise root `CONTEXT.md`;
   - relevant ADRs in root `docs/adr/` and the relevant context's `docs/adr/`.

   Use the domain vocabulary in test names and assertions, and follow applicable ADRs.
2. Determine the public interface through which the behavior should be tested.
   - Test observable behavior, not implementation details.
   - Prefer the same public interface a real caller would use.
   - If the appropriate public interface is unclear, consult the project's code-design guidance before proceeding.
3. Present the proposed test boundary or boundaries to the user and obtain explicit approval.

Do not write a test against a boundary the user has not approved.

## Test design

Prefer integration-style tests that exercise real project-owned components together.

Do not mock project-owned classes, modules, or internal collaborators.

Mocks or fakes are appropriate at system boundaries, including:

- external services;
- time or randomness;
- filesystem access when using the real filesystem is inappropriate;
- databases when a real test database is impractical.

Where practical, isolate external dependencies behind small, replaceable interfaces representing the operation the application actually needs.

For every test:

- exercise one coherent behavioral claim;
- make the relevant inputs or conditions clear;
- assert an externally observable result;
- verify through the public interface rather than inspecting internal state;
- use expected values derived independently from the production implementation.

Valid sources for expected values include specifications, fixed known values, and manually worked examples. Do not duplicate the production algorithm in the test to calculate the expected result.

Write tests so that internal refactoring does not break them when externally visible behavior remains unchanged.

If meaningful testing appears to require accessing internal state or internals directly, reconsider the public design before using those internals as the test surface.

## Red-green cycle

Work one behavioral increment at a time.

Each increment should implement one observable behavior through every implementation layer required to make that behavior work. Organize work by behavior, not by technical layer.

For each increment:

1. Write one test for one behavior at an approved public boundary.
2. Run the test.
3. Confirm that it fails because the required behavior is missing or incorrect.
4. Implement only enough production code, across whatever layers are required, to satisfy that behavior.
5. Run the test again and confirm that it passes.
6. Use the result and what was learned to select the next behavioral increment.

The work must make this sequence evident for every increment:

**failing test → minimal implementation → passing test**

Do not batch implementation by technical layer. For example, do not build all persistence changes, then all service changes, then all interface changes for several behaviors at once.

Do not write tests for multiple future behaviors and then implement them as a batch. Complete the current behavioral increment before defining the next one.

Parameterized tests are acceptable when they still represent a single behavioral increment rather than pre-implementing multiple future behaviors.

## Invalid red states

A failing test counts as the red step only when it fails for the intended behavioral reason.

If it fails because of syntax, setup, environment, fixtures, infrastructure, or another unrelated problem, correct that problem and rerun the test before implementing production behavior.

If a newly written test already passes, stop and determine whether:

- the requested behavior already exists; or
- the test does not actually prove the intended behavior.

Do not continue to implementation until that is resolved.

## Scope discipline

During the red-green cycle, do not:

- implement behavior before a failing test requires it;
- write the complete future test suite in advance;
- batch work by technical layer across multiple behaviors;
- add speculative functionality;
- perform unrelated refactoring or cleanup.

Structural changes required to implement the current tested behavior are allowed.

Leave optional cleanup and unrelated refactoring for a later code-review or refactoring stage.

Existing tests outside the requested work do not need to be rewritten merely because they do not follow this skill's testing guidance.