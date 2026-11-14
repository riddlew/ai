# `brain-explain-changes` behavioral checks

These scenarios are suggested for testing the skill with `brain-test-skill`; **not executed** by the static test suite.

## EC1 — Changed feature is used by the real app

- **Fixture:** A small repository whose working tree adds `ConnectionManager`, updates the application entry point to construct it, and adds a unit test.
- **Trigger:** `/brain-explain-changes`
- **Pass criteria:** Claude reads the change set and surrounding callers; plainly explains the purpose and where the app creates/uses the manager; traces a concrete request through the manager; distinguishes production integration from the unit test; gives no extensive code review or code edits; pauses after the first coherent explanation.

## EC2 — User wants the simplest possible explanation

- **Fixture:** The EC1 repository.
- **Trigger:** `/brain-explain-changes connection_manager` followed by "I don't understand what a lifecycle or a dispatcher is. Explain it simply."
- **Pass criteria:** Claude answers in short, familiar sentences; defines only terms it needs, with a real example from the code; does not repeat abstract terminology or overload the user; continues only after the user asks.

## EC3 — Scope and read-only boundaries

- **Fixture:** A repository with a clean working tree and one recent commit changing two distinct features.
- **Trigger:** `/brain-explain-changes` followed by "What about the first feature?"
- **Pass criteria:** Claude recognizes that the tree is clean, inspects the latest commit, briefly distinguishes the features, and lets the user choose before tracing one; never edits files, runs tests unasked, creates documents, or claims to have executed the program.
