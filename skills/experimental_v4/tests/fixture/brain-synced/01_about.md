# About

crate is a personal command-line tool for gigging DJs to prepare sets offline. It organizes tracks into crates (named, ordered collections) and finds tracks that fit a tempo range.

Users: the author and a few DJ friends, on their own laptops, without a network connection.

Core concepts: **Crate**, **Track**, **BPM** (see `glossary.md`).

How it works: each command opens a local SQLite database, reads or writes crates and tracks, prints results, and exits.
