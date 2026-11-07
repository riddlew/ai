# Tracing a Failure to Its Source

Use this when a failure crosses components, or an error surfaces deep in a call chain. The place where the error appears is rarely the place where it starts.

## Backward tracing

1. Find the immediate cause: the line that fails and the value it received.
2. Ask what called it, and with what value.
3. Keep going up the callers, checking the value at each step, until you reach the original trigger: the place where the bad value, state, or configuration first appears.
4. Fix at the source. Patching the symptom further down leaves the origin free to cause the next failure. If that fix changes input validation, error behavior, or stored data, consult the user first (root `CLAUDE.md`).

If you cannot trace by reading, add observation (below) rather than guessing. Record each step with its source location so the chain is checkable.

## Boundary instrumentation

For a system with several layers (for example CI, build, and signing; or API, service, and database), evidence is missing until you see what crosses each boundary.

- At each boundary, log what enters and what leaves, and confirm that environment and configuration are passed through.
- For secrets, log only whether each is set, never its value.
- Run once, then read the output to find the layer where the value first goes wrong. Investigate that layer.
- Log before the operation that fails, not after it, and include enough context (arguments, a stack trace, the working directory, relevant environment variables) to identify the caller.
- In tests, the logger may be suppressed; write to standard error or use the harness's own output.

## Rules for instrumentation

- It is temporary. Report what you added, and remove it before the fix by deleting exactly the lines and files you added. Never use `git checkout`, `git restore`, `git stash`, `git reset`, or `git clean` for this: they also discard the user's uncommitted changes. Confirm removal with `git status` and `git diff`.
- In diagnosis-only mode, first observe without touching code: existing logs, a debugger, the test harness's output. Adding temporary instrumentation needs the user's OK, and it is removed before you report. Confirm with `git status` that the tree matches its state before the run.
- Do not add instrumentation to shared or production environments without authorization.

## When the trace ends outside the code

If the origin is an input, an environment, or an external system, say so and stop tracing. Proposed handling still needs consultation under `SKILL.md` §5.
