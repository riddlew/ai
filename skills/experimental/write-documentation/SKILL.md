---
name: write-documentation
description: Create concise repository documentation from verified project structure, configuration, and developer workflows.
---

# Write Documentation

Create or update concise project documentation from evidence in the repository.

Use repository-specific facts rather than generic boilerplate. Do not invent commands, configuration, architecture, or project behavior.

## Inspect the repository

Before writing, inspect enough of the repository to determine:

- what the project does;
- its primary runtime, language, or toolchain requirements;
- how it is installed or built;
- how it is run;
- how tests are executed;
- major directories and their responsibilities;
- relevant configuration;
- useful scripts or developer tasks.

Prefer authoritative repository evidence such as:

- package or dependency manifests;
- build-system files;
- task or script definitions;
- container configuration;
- application entry points;
- test configuration;
- environment templates;
- CI configuration;
- existing project documentation.

Do not infer a command merely because it is conventional for the detected technology.

If important information cannot be verified, omit it unless the missing value itself is useful to surface. Use a `<placeholder>` only when necessary.

Never include secrets, credentials, tokens, or sensitive values.

## Choose the document

Use the repository's existing primary project documentation when one is clearly established.

Prefer root `README.md` for the primary repository overview.

If the project intentionally uses another root documentation file, preserve that convention.

Do not overwrite substantial existing human-written documentation without incorporating relevant existing content. Update it to reflect the repository rather than replacing it blindly.

If no primary project documentation exists, create root `README.md`.

## Write for a new contributor

Keep the document concise and skimmable, but include enough verified information for a developer to understand and work with the project.

Include only sections that apply.

Typical sections include:

```markdown
# <Project Name>

## Overview

What the project does and, when evident, who or what it is for.

## Quick Start

Requirements and the verified commands needed to install, build, run, or otherwise use the project.

## Structure

The important top-level directories or files and their responsibilities.

## Configuration

Configuration that a developer needs to know about, including environment variables when documented by the repository.

## Development

Useful scripts, tasks, testing commands, formatting, linting, or other established workflows.

## Notes

Important limitations, unusual setup requirements, or other information a contributor should know.
```

Adapt the headings to the project.

For example:

- a library may need `Usage` instead of `Run`;
- a command-line application may need example invocation;
- a service may need startup and configuration instructions;
- a monorepo may need workspace-specific structure.

Do not create empty or irrelevant sections.

## Keep it evidence-based

Every factual statement should be supportable from the current repository.

When existing documentation conflicts with code, configuration, or build files, prefer current repository evidence and correct the stale documentation.

Keep commands exact and copyable.

Prefer concise explanations over exhaustive internal detail. The goal is practical repository documentation, not an architecture specification or generated inventory.