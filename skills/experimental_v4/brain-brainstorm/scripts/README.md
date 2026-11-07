# Visual companion scripts

These scripts come from the `brainstorming` skill in [obra/superpowers](https://github.com/obra/superpowers) v7.0.0, used under the MIT license in `LICENSE`.

Changes from upstream:
- `server.cjs`: the page header is a local label. Upstream loads a logo from a third-party site unless telemetry is disabled, and reads a version from a `package.json` three folders up. Both were removed, so the companion makes no network request beyond localhost.
- `frame-template.html`: the page title.

The server needs Node.js and has no npm dependencies. `references/visual-companion.md` describes how the skill uses the scripts.
