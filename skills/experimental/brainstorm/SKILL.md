---
name: brainstorm
description: Stress-test a plan, decision, or idea by systematically resolving its open questions, assumptions, and tradeoffs.
---

# Brainstorm

Work with the user until the idea is sufficiently defined that no important decision or assumption remains unresolved.

Maintain a dependency graph of the decisions involved. A decision may become answerable only after one or more earlier choices have been settled.

## 1. Identify what is unresolved

From the conversation, distinguish between:

- decisions already made
- choices still requiring the user's judgment
- factual questions that can be investigated independently
- assumptions that have not yet been validated

Add newly discovered decisions to the dependency graph as the discussion develops.

Do not invent questions merely to prolong the session. A decision matters when different answers could meaningfully change the resulting plan.

## 2. Ask the currently available questions

Determine which unresolved decisions have no outstanding prerequisites.

Ask all such questions in the same turn. Do not unnecessarily postpone an independent question.

For every question:

- assign a number and short title
- explain the decision and relevant tradeoffs
- provide useful options when appropriate
- state your recommended answer and reasoning

Example:

```text
**Question 1 — Authentication model**

Should accounts support password authentication, external identity providers, or both?

- Password only
- External providers only
- Both

**Recommended:** Both, because it preserves a simple signup path while allowing external authentication where desired.

---

**Question 2 — Session lifetime**

How long should an inactive authenticated session remain valid?

**Recommended:** 24 hours unless the product has security requirements that justify a shorter duration.
```

After asking the available questions, wait for the user's answers before advancing dependent decisions.

Never ask two questions in the same batch when the second cannot be answered meaningfully until the first has been resolved.

## 3. Resolve facts independently

Do not ask the user for factual information that can reasonably be obtained from available files, tools, documentation, the repository, or the environment.

For example:

```text
Bad:
"What database does this project use?"

Better:
Inspect the project configuration and determine the database directly.
```

An unresolved factual investigation blocks only the decisions that depend on its result. Continue discussing other independent branches while that information is being established.

Keep ownership clear:

- facts should be discovered when possible
- preferences, priorities, requirements, scope, and tradeoffs belong to the user

Do not silently choose subjective requirements for the user.

## 4. Reevaluate after each answer

Update the dependency graph whenever the user responds.

Their answers may:

- settle existing decisions
- make other questions irrelevant
- expose previously hidden choices
- introduce new constraints
- unlock downstream decisions
- reveal conflicting assumptions

Recalculate which unresolved decisions are now answerable and present the next set together.

Example:

```text
If deployment strategy depends on whether the application must support offline operation, resolve the offline requirement first.

Once that decision is known, deployment questions depending on it may become eligible for the next round.
```

Do not follow a fixed questionnaire. Let the remaining questions be determined by the decisions already made.

## 5. Reach a shared result

Continue until the dependency graph contains no meaningful unresolved decisions and no important assumption remains implicit.

Before finishing, verify that:

- consequential choices have been addressed
- dependent branches have been followed
- discoverable facts have been investigated
- unresolved assumptions have been surfaced
- the user, rather than the assistant, made subjective decisions

Then summarize the resulting direction and ask the user to confirm that it matches their understanding.

Do not begin implementation or otherwise act on the resulting plan until the user confirms it.