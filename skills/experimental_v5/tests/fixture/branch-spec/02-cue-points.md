# Cue Points

## Problem

DJs mark the moments in a track they jump to while mixing, and want those marks kept with the track.

## Desired Outcome

`crate cue add <track> <seconds>` stores a cue point, and `list-crate` and `filter` show each track's cue points.

## Behavior and Invariants

- A cue point is a position in seconds from the start of the track, stored as a float.
- A track may have any number of cue points, listed in ascending order.
- If no track has the given title, the command exits with status 1 and prints `no such track: <track>`.

## Examples

- E1: `cue add "Opening" 32.5`, then `list-crate warmup` shows `Opening ... cues: 32.5s`.
