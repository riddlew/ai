# crate

crate — a command-line tool for DJs to organize tracks into crates.

## Usage

    python -m crate.cli add-track warmup "Track" "Artist" 124
    python -m crate.cli list-crate warmup
    python -m crate.cli filter warmup --bpm-min 120 --bpm-max 128

Set `CRATE_DB` to choose the database file (default `~/.crate.db`).

## Development

    pytest
