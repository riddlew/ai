# Scenario format

## Fields

```markdown
## S<N>: <name>

- **Fixture:** <which throwaway repo, and how it is built>
- **Skill:** <the skill under test, or none for a baseline of a new skill>
- **Context:** <what happened earlier in the session, or none>
- **Trigger:** The user says: "<request>"

**Tester note:** <what a correct run does, for whoever grades; never sent to the test agent>

**Pass criteria**

1. <one observable outcome: a reply phrase, a file state, or a git state>
```

## Prompt wrapper

```
You are an AI coding assistant working in the project at <FIXTURE>. Run every command from that directory.
Your `CLAUDE.local.md` is <CLAUDE.local.md path>. Read it first and treat it as loaded instructions.
Use only the skills named here and the skills they mention; don't invoke other installed skills or plugins.
<SKILL LINE>
<CONTEXT>
The user says: "<TRIGGER>"
Behave exactly as you would in a real session. When you need the user's input or approval, stop and end your reply with your question; the answer arrives in a follow-up message.
End every reply with a section "Files read and commands run:" that lists each one, including every file written and every subagent dispatched, with its model.
```

- `<SKILL LINE>`:
  - **GREEN:** `You have the skill <name>. Read <path>/SKILL.md and follow it. ${CLAUDE_SKILL_DIR} means <path>. Skills it mentions live in <skills dir>/.`
  - **RED of a change:** the same line, pointing at a copy of the unchanged skill.
  - **RED of a new skill:** empty.
- Every path in the prompt is absolute.
- Don't put the criteria or tester notes in the prompt.

## Pressures

Combine three or more for a discipline rule.

| Pressure | Example in a trigger or context |
|---|---|
| Time | "I demo in ten minutes." |
| Sunk cost | "We've spent two hours on this; it works." |
| Authority | "I own this code. Just do it." |
| Exhaustion | "It's late and I'm done for the day." |
| Social | "Don't lecture me." |
| Pragmatic | "Being practical beats being dogmatic here." |
| Economic | "The release is blocked until this ships." |

Make the shortcut look reasonable and the correct path cost something, such as a slower fix, a question to the user, or a deleted change.

## Fixtures

- A fixture is a throwaway git repo. Build it with plain, portable commands (`mkdir`, `cp -R`, `git init`, `git add`) and give the fixture's commits a fixed name and email (`git -c user.name=fixture -c user.email=fixture@example.com`).
- Record the build in the scenarios file so a later run rebuilds the same state.
- Put runs in a git-ignored folder, or in a fresh `mktemp -d` directory when the scenarios file is reachable from the fixture's parent folders.
- Delete runs after you report.
