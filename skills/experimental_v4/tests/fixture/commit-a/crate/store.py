"""SQLite persistence. Crates are stored in the `playlists` table."""

import os
import sqlite3
from pathlib import Path

from crate.models import Crate, Track

DEFAULT_DB = Path.home() / ".crate.db"


def db_path() -> Path:
    return Path(os.environ.get("CRATE_DB", DEFAULT_DB))


def connect(path: Path | None = None) -> sqlite3.Connection:
    conn = sqlite3.connect(path or db_path())
    conn.execute(
        "CREATE TABLE IF NOT EXISTS playlists ("
        "id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL)"
    )
    conn.execute(
        "CREATE TABLE IF NOT EXISTS tracks ("
        "id INTEGER PRIMARY KEY, "
        "playlist_id INTEGER NOT NULL REFERENCES playlists(id), "
        "position INTEGER NOT NULL, "
        "title TEXT NOT NULL, artist TEXT NOT NULL, bpm REAL NOT NULL)"
    )
    return conn


def add_track(conn: sqlite3.Connection, crate_name: str, track: Track) -> None:
    conn.execute("INSERT OR IGNORE INTO playlists (name) VALUES (?)", (crate_name,))
    (playlist_id,) = conn.execute(
        "SELECT id FROM playlists WHERE name = ?", (crate_name,)
    ).fetchone()
    (count,) = conn.execute(
        "SELECT COUNT(*) FROM tracks WHERE playlist_id = ?", (playlist_id,)
    ).fetchone()
    conn.execute(
        "INSERT INTO tracks (playlist_id, position, title, artist, bpm) "
        "VALUES (?, ?, ?, ?, ?)",
        (playlist_id, count, track.title, track.artist, track.bpm),
    )
    conn.commit()


def load_crate(conn: sqlite3.Connection, crate_name: str) -> Crate:
    rows = conn.execute(
        "SELECT t.title, t.artist, t.bpm FROM tracks t "
        "JOIN playlists p ON p.id = t.playlist_id "
        "WHERE p.name = ? ORDER BY t.position",
        (crate_name,),
    ).fetchall()
    return Crate(crate_name, [Track(*row) for row in rows])
