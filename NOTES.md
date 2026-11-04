## How do you inject dynamic context?

The !`command` syntax runs shell commands before the skill content is sent to Claude. The command output replaces the placeholder, so Claude receives actual data rather than the command itself. This is preprocessing. Claude only sees the final result.

This skill summarizes a pull request by fetching live PR data with the GitHub CLI:

```markdown
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Your task
Summarize this pull request...
```

When this skill runs, each !`command` executes first, the output replaces the placeholder, and Claude receives the prompt with actual PR data already filled in.