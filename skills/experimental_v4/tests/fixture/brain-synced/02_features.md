# Features

## Crate management

- `add-track <crate> <title> <artist> <bpm>` — appends a track to a crate, creating the crate if needed.
- `list-crate <crate>` — prints the crate's tracks in order.

## Tempo filtering

- `filter <crate> --bpm-min N --bpm-max M` — prints the crate's tracks whose BPM is within the range, in crate order. Behavior: `specs/01-bpm-filter.md`.
