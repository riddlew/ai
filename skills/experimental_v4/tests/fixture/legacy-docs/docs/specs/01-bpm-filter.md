# BPM Filter

## Problem

DJs need to find the tracks in a crate that fit the tempo of the current set.

## Desired Outcome

`crate filter <crate> --bpm-min N --bpm-max M` lists the matching tracks in crate order.

## Behavior and Invariants

- Both bounds are inclusive: a track matches when bpm-min ≤ bpm ≤ bpm-max.
- Output keeps crate order.

## Examples

### Filtering

- **E1:** Given tracks at 120, 128, and 140 BPM, when filtering 125–135, then only the 128 BPM track is listed.
- **E2:** Given tracks at 120, 128, and 140 BPM, when filtering 120–128, then the 120 and 128 BPM tracks are listed.

## Verification Strategy

Unit tests of `filter_by_bpm` for E1 and E2.
