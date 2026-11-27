# Key Filter

## Problem

DJs mix harmonically and need the tracks in a crate that share a key.

## Desired Outcome

`crate filter <crate> --key <key>` lists the matching tracks in crate order.

## Behavior and Invariants

- Keys use Camelot notation: a number 1–12 followed by `A` or `B` (for example `8A`).
- Key matching is exact and case-insensitive (`8a` matches `8A`).
- Output keeps crate order.
- An invalid key exits with status 2 and prints `invalid key: <key>`.
- If the crate does not exist, the command exits with status 1 and prints `no such crate: <crate>`.
- `--key` may be combined with `--bpm-min` and `--bpm-max`; a track must satisfy all given filters.

## Examples

- **E1:** Given tracks A (8A), B (9A), and C (8A), when filtering `--key 8A`, then A and C are listed, in that order.
- **E2:** Given the same tracks, when filtering `--key 8a`, then A and C are listed.
- **E3 (failure):** When filtering `--key 13C`, then the command exits with status 2 and prints `invalid key: 13C`.

## Technical Decisions

- Add a nullable `key` column to `tracks`; `add-track` gains an optional `--key`.

## Verification Strategy

Unit tests of the filter function for E1 and E2; a CLI test for E3.
