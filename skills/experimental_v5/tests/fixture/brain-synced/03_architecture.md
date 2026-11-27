# Architecture

- **Language and runtime:** Python ≥ 3.11, standard library only; `pytest` for tests.
- **Storage:** SQLite through `sqlite3` (decision: `adrs/0001-use-sqlite.md`).
- **Platforms:** any OS with Python 3.11.

## Components

| Module | Owns |
|---|---|
| `crate/models.py` | `Track` and `Crate` dataclasses |
| `crate/store.py` | Database connection, schema creation, all SQL |
| `crate/cli.py` | Argument parsing, command dispatch, output, `filter_by_bpm` |

Dependency direction: `cli` → `store` → `models`.
