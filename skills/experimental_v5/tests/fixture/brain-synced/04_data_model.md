# Data Model

## Entities

- **Track** — `title: str`, `artist: str`, `bpm: float`.
- **Crate** — `name: str`, `tracks: list[Track]` (ordered).

## Schema

| Table | Columns | Notes |
|---|---|---|
| `playlists` | `id`, `name` (unique) | One row per Crate |
| `tracks` | `id`, `playlist_id`, `position`, `title`, `artist`, `bpm` | `position` keeps crate order |
