from dataclasses import dataclass, field


@dataclass
class Track:
    title: str
    artist: str
    bpm: float
    # Cue points, in seconds from the start of the track.
    cue_points: list[float] = field(default_factory=list)


@dataclass
class Crate:
    """A named, ordered collection of tracks."""

    name: str
    tracks: list[Track] = field(default_factory=list)
