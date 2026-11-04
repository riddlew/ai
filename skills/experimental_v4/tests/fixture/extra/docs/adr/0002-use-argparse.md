# Use argparse for the CLI

## Context

crate has a handful of subcommands and no runtime dependencies.

## Decision

Parse arguments with the standard library's `argparse`.

## Rationale

Keeps the zero-dependency install. Click was considered but adds a dependency.
