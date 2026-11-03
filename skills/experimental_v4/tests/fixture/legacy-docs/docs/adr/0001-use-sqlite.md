# Use SQLite for storage

## Context

crate runs offline on a DJ's laptop. No server is available.

## Decision

Store crates and tracks in a local SQLite file through Python's `sqlite3`.

## Rationale

Zero setup, a single file, and it ships with Python. A JSON file was considered but makes ordering and filtering harder.
