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
        "title TEXT NOT NULL, artist TEXT NOT NULL, bpm TEXT NOT NULL)"
    )
    conn.execute(
        "CREATE TABLE IF NOT EXISTS cue_points ("
        "track_id INTEGER NOT NULL REFERENCES tracks(id), "
        "seconds REAL NOT NULL)"
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


def add_cue(conn: sqlite3.Connection, track_title: str, seconds: float) -> None:
    row = conn.execute(
        "SELECT id FROM tracks WHERE title = ? ORDER BY id LIMIT 1", (track_title,)
    ).fetchone()
    if row is None:
        raise ValueError(f"no track titled {track_title!r}")
    conn.execute(
        "INSERT INTO cue_points (track_id, seconds) VALUES (?, ?)", (row[0], seconds)
    )
    conn.commit()


def load_crate(conn: sqlite3.Connection, crate_name: str) -> Crate:
    rows = conn.execute(
        "SELECT t.id, t.title, t.artist, t.bpm FROM tracks t "
        "JOIN playlists p ON p.id = t.playlist_id "
        "WHERE p.name = ? ORDER BY t.position",
        (crate_name,),
    ).fetchall()
    tracks = []
    for track_id, title, artist, bpm in rows:
        cues = [
            seconds
            for (seconds,) in conn.execute(
                "SELECT seconds FROM cue_points WHERE track_id = ? ORDER BY seconds",
                (track_id,),
            )
        ]
        tracks.append(Track(title, artist, bpm, cues))
    return Crate(crate_name, tracks)
