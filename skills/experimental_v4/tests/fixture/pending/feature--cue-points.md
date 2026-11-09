# Pending brain changes: feature/cue-points

Branch: feature/cue-points
Base: __A_SHA__
Updated: __B_SHA__ (2026-11-08)

Apply these to the root files when the branch merges, after checking each against the merged code.

## 02_features.md

- **Add:** `cue add <track> <seconds>` stores a cue point on the first track with that title. `list-crate` and `filter` print each track's cue points after its BPM.

## 04_data_model.md

- **Add:** table `cue_points` (`track_id` → `tracks.id`, `seconds` REAL). `Track.cue_points` is a list of floats, in seconds.
- **Add:** column `cue_points.position_ms` (INTEGER), the cue position in milliseconds.
