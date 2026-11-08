# Visual companion

A browser tab that shows mockups, diagrams, and side-by-side options while a decision is discussed in the terminal. The scripts are in `${CLAUDE_SKILL_DIR}/scripts/`, need Node.js, and make no network request beyond localhost.

## Use it per question

The test: would the user understand this question better by seeing it than reading it?

- **Browser:** screen or page layouts, output formats, wireframes, flow or state diagrams, and side-by-side designs that would look different from each other.
- **Terminal:** requirements, scope, behavior, tradeoffs, and approaches described in words.

A question about a UI topic isn't automatically visual. "Should the page filter one crate or all crates?" is a scope question for the terminal. "Which of these two layouts fits?" belongs in the browser.

## Start a session

Start it only after the user accepts.

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/start-server.sh --open
```

The script backgrounds the server and prints one line of JSON:

```json
{"type":"server-started","port":52341,"url":"http://localhost:52341/?key=ab12…","screen_dir":"/tmp/brainstorm-12345-1706000000/content","state_dir":"/tmp/brainstorm-12345-1706000000/state"}
```

- Keep `screen_dir` and `state_dir`. The session directory is their parent.
- Give the user the **complete** `url`, including `?key=`. The server rejects requests without the key. With `--open`, the browser opens on the first screen. Share the URL anyway, in case it doesn't.
- Session files live in the system temp directory, not the project, and the stop script deletes them. Don't pass `--project-dir`.
- If the JSON wasn't captured, read `$STATE_DIR/server-info`.
- **Windows (Git Bash):** the script runs in the foreground, which blocks the call. Start it with the Bash tool's `run_in_background: true`, then read `$STATE_DIR/server-info` on the next turn. Other environments that reap background processes need `--foreground` and their own background mechanism.
- **Remote or container setups:** add `--host 0.0.0.0 --url-host localhost` if the URL can't be reached.

## The loop

1. **Check the server is alive.** `$STATE_DIR/server-info` exists and `$STATE_DIR/server-stopped` doesn't. If it stopped (it exits after 4 hours idle), start it again and give the new URL.
2. **Write a screen.** Use the file-writing tool to create a new file in `screen_dir`. Never use a shell heredoc.
   - Give each screen a new semantic name, such as `layout.html` or `layout-v2.html`; the server shows the newest file.
   - Write a content fragment, with no `<html>` or `<!DOCTYPE`. The server wraps it in the page frame.
3. **Tell the user what's on screen and end your turn.** Repeat the URL, summarize the screen in one line, and ask for their answer in the terminal. They can also click an option.
4. **Read the answer.** The terminal message comes first. `$STATE_DIR/events`, if it exists, holds their clicks as JSON lines, for example `{"type":"click","choice":"a","text":"…","timestamp":…}`. The last click is usually the choice. Pushing a new screen clears the file.
5. **Record the decision** in the decision table, in text, like any other answer.
6. **Clear stale screens.** When the next question is text, push `waiting.html`:

   ```html
   <div style="display:flex;align-items:center;justify-content:center;min-height:60vh">
     <p class="subtitle">Continuing in the terminal…</p>
   </div>
   ```

## Content fragments

```html
<h2>Which layout fits?</h2>
<p class="subtitle">One crate at a time, as `crate filter` works today</p>

<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div>
    <div class="content"><h3>Sidebar list</h3><p>Crates on the left, tracks on the right</p></div>
  </div>
  <div class="option" data-choice="b" onclick="toggleSelect(this)">
    <div class="letter">B</div>
    <div class="content"><h3>Dropdown</h3><p>Crate picker above one wide table</p></div>
  </div>
</div>
```

Classes the frame provides:

- **Choices:** `.options` holding `.option` blocks (add `data-multiselect` to the container for several choices). Each `.option` has `data-choice` and `onclick="toggleSelect(this)"`, and holds a `.letter` and a `.content`.
- **Visual designs:** `.cards` holding `.card` blocks, each with a `.card-image` and a `.card-body`.
- **Mockups:** `.mockup` holding a `.mockup-header` and a `.mockup-body`.
- **Comparison:** `.split` for side by side, and `.pros-cons` holding `.pros` and `.cons`.
- **Wireframe parts:** `.mock-nav`, `.mock-sidebar`, `.mock-content`, `.mock-button`, `.mock-input`, `.placeholder`.
- **Text:** `h2` titles, `h3` headings, `.subtitle`, `.section`, `.label`.

See `${CLAUDE_SKILL_DIR}/scripts/frame-template.html` for the full CSS.

Design tips:

- Show two to four options per screen.
- Put the question at the top of each screen.
- Match fidelity to the question: wireframes for layout, more detail only when look and feel is the question.
- Use real content (crate names, track titles) when placeholder text would hide the problem.

## Stop the session

When the user is done with the browser, or the brainstorm ends:

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/stop-server.sh <session_dir>
```

The script stops the server and deletes the temp session directory.
