from dataclasses import dataclass, field


@dataclass
class Track:
    title: str
    artist: str
    bpm: float


@dataclass
class Crate:
    """A named, ordered collection of tracks."""

    name: str
    tracks: list[Track] = field(default_factory=list)
