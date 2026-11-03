import argparse
import sys

from crate import store
from crate.models import Track


def filter_by_bpm(tracks: list[Track], bpm_min: float, bpm_max: float) -> list[Track]:
    return [t for t in tracks if bpm_min <= t.bpm <= bpm_max]


def _print_tracks(tracks: list[Track]) -> None:
    for t in tracks:
        print(f"{t.title} — {t.artist} ({t.bpm:g} BPM)")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="crate")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add-track", help="Add a track to a crate")
    add.add_argument("crate")
    add.add_argument("title")
    add.add_argument("artist")
    add.add_argument("bpm", type=float)

    lst = sub.add_parser("list-crate", help="List the tracks in a crate")
    lst.add_argument("crate")

    flt = sub.add_parser("filter", help="List tracks in a crate within a BPM range")
    flt.add_argument("crate")
    flt.add_argument("--bpm-min", type=float, required=True)
    flt.add_argument("--bpm-max", type=float, required=True)

    args = parser.parse_args(argv)
    try:
        conn = store.connect()
        if args.command == "add-track":
            store.add_track(conn, args.crate, Track(args.title, args.artist, args.bpm))
        elif args.command == "list-crate":
            _print_tracks(store.load_crate(conn, args.crate).tracks)
        elif args.command == "filter":
            tracks = store.load_crate(conn, args.crate).tracks
            _print_tracks(filter_by_bpm(tracks, args.bpm_min, args.bpm_max))
    except Exception as exc:
        print(f"crate: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
