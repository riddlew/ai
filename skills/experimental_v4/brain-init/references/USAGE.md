# Brain Skills — Usage Guide

This guide explains when to use `brain-brainstorm` versus `brain-plan`, then demonstrates seven example workflows: five involving existing TCP/UDP client and server applications, one multi-session ZPL printer library and YAML-driven CLI project, and one example of revising approved work after implementation has started.

The prompts, file names, code examples, review findings, and test results are **illustrative**, not results from a real repository. Adapt them to your codebase and the capabilities of your installed skills.

**Model labels** below are the README's **default main-session recommendations**, not automatic model switches or mandatory requirements. Deviate for task difficulty as the README describes; delegated subagents follow `CLAUDE.local.md` role assignments.

---

# Choosing `brain-brainstorm` vs. `brain-plan`

The distinction is **what you're trying to resolve**:

- **`brain-brainstorm`** — Use when you haven't fully decided *what to build or how it should work*.
- **`brain-plan`** — Use when you know what you want, but need to organize *how to get from the current codebase to that result*.

They're complementary, not necessarily sequential.

| Situation | Use | Default model |
|---|---|---|
| Exploring several possible architectures | `brain-brainstorm` | **Opus** |
| Deciding component ownership or design patterns | `brain-brainstorm` | **Opus** |
| Clarifying ambiguous requirements or behavior | `brain-brainstorm` | **Opus** |
| Understanding dependencies across several modules | `brain-plan` | **Opus** |
| Organizing a large feature into stages and deliverables | `brain-plan` | **Opus** |
| Coordinating work over multiple sessions | `brain-plan` | **Opus** |
| Designing exact classes, APIs, and method signatures | `brain-design-implementation` | **Opus** |

## Example: TCP messaging with unsettled architecture

You know the exact wire format but haven't decided where serialization, buffering, and message dispatch should live. Start with **`brain-brainstorm`** to settle those architectural decisions. Use `brain-plan` if implementation then requires coordinating multiple modules, milestones, or investigations. Use `brain-write-spec` and `brain-design-implementation` as appropriate to record binding requirements and agree on the code-level design.

## Example: Large feature with settled architecture

You already know the protocol, component ownership, requirements, and implementation approach. **Skip brainstorming.** Use `brain-plan` to organize work across the client, server, shared library, and integration tests. Then create the specification or blueprint needed by the project and implement it.

## Example: Small feature

You want to display the most recent UDP heartbeat timestamp, and the necessary state already exists. **Skip both** `brain-brainstorm` and `brain-plan`; go straight to `brain-implement`.

## Decision rule

1. **Are there unresolved product or architectural choices?** If yes, use `brain-brainstorm`.
2. **Is the work large enough to require coordinated stages, dependencies, or multiple sessions?** If yes, use `brain-plan`.

If both are true, use both. **`brain-plan` is not a substitute for `brain-design-implementation`:** planning decides work breakdown and sequencing; blueprinting defines the code-level implementation. You do not need every skill for every feature. Use the smallest workflow that resolves the actual uncertainty and complexity.

For a brand-new, multi-session project, see [Scenario 6: ZPL printer library and YAML CLI](#scenario-6--build-a-zpl-printer-library-and-yaml-cli-across-multiple-sessions) for an example of project-level brainstorming followed by repeated feature cycles.

---

For a complete traceability example including ADR references, negative-path requirements, component ownership, technical plans, and executable task mappings, read `${CLAUDE_SKILL_DIR}/../brain-init/references/start-machine-example.md`. This is a planning example, not an implemented TCP feature.

## Hierarchical feature workflow

For nontrivial features, use `.brain/features/<slug>/01-brief/` → `02-specifications/` → `03-components/` → `04-implementation-plans/` → `05-tasks/`. `brain-brainstorm` establishes intent, `brain-write-spec` records behavior, `brain-decompose-feature` defines coherent functional responsibilities, `brain-design-implementation` specifies code-level implementation, and `brain-write-tasks` produces executable tasks. `brain-implement` writes verification and progress separately to `execution.md`. Read the authoritative schema at `${CLAUDE_SKILL_DIR}/../brain-init/references/feature-document-contract.md` in the installed skills. Skip unhelpful intermediate stages for simple work.

## Understand changes after implementation

**Model (main session):** **Sonnet** (`brain-explain-changes`).

Run `/brain-explain-changes` to walk through the working-tree changes (or the latest commit if the tree is clean). Pass a file, symbol, or commit range to focus it, for example `/brain-explain-changes connection_manager`. Claude starts with a plain-language overview, traces actual application calls in small steps, and pauses for questions rather than giving a full code review. This skill reads files but does not edit them or create reports.

---

# Shared client/server example project (Scenarios 1–5)

Assume a repository contains two applications:

- **Client:** Connects to the server, sends commands, receives responses, and tracks connection state.
- **Server:** Accepts TCP connections, processes commands, sends responses, and sends certain time-sensitive updates over UDP.

The applications already exist and their architecture, APIs, and established decisions are described in `.brain/`. Under the collaboration policy, established requirements and approved decisions remain authoritative. Collaborative implementation is the default: Claude works in small, verifiable increments and pauses for your review.

---

# Scenario 1 — Implement a large feature with a rigid binary protocol

**Goal:** Implement bidirectional TCP messaging across the client and server. Frame layouts, message identifiers, byte order, and per-message payload formats are fixed **before** brainstorming begins. The protocol is non-negotiable; Claude may design the implementation but cannot modify the wire contract to simplify it.

## Step 0: Establish authoritative requirements before brainstorming

**Model (main session):** No skill-specific tier for reviewing source material; the following `brain-brainstorm` step defaults to **Opus**.

Suppose `protocol/wire-v1.md` defines the following **12-byte header**:

| Offset | Field | Size | Encoding |
|---|---|---|---|
| 0 | Magic | 2 bytes | `CA FE` |
| 2 | Version | 1 byte | `01` |
| 3 | Message type | 1 byte | Defined enum |
| 4 | Flags | 1 byte | Bitmask |
| 5 | Reserved | 1 byte | Must be `00` |
| 6 | Payload length | 2 bytes | Unsigned, big-endian |
| 8 | Sequence number | 4 bytes | Unsigned, big-endian |
| 12 | Payload | Variable | Message-specific |

The same authoritative document defines payloads:

- `DATA` (`0x10`): two-byte channel ID, two-byte data length, followed by exactly that many data bytes.
- `ACK` (`0x11`): four-byte acknowledged sequence number and one-byte status.

For instance, a `DATA` frame with sequence 42, channel 7, and the UTF-8 bytes for `Hi` must be exactly:

```text
CA FE 01 10 00 00 00 06 00 00 00 2A
00 07 00 02 48 69
```

There are **18 bytes total**: 12 header bytes and 6 payload bytes. A different byte sequence is incorrect even if the client and server happen to communicate successfully with one another.

## Step 1: `/brain-brainstorm` — Set architectural direction

**Model (main session):** **Opus** (`brain-brainstorm`).

**Example prompt:**

> `/brain-brainstorm`
>
> I want to implement the TCP messaging protocol described in `protocol/wire-v1.md` across the client and server.
>
> The frame layout, message type values, field formats, and byte ordering are mandatory. Do not propose changes to them.
>
> I want to explore the architecture before implementation. My preferences are:
>
> - One shared codec implementation, if both applications can use it.
> - Network transport separated from message serialization.
> - TCP sessions should own their connections.
> - Avoid a generic event bus or messaging framework.
>
> Investigate the existing architecture and recommend how to integrate the protocol with minimal disruption.

Claude should read the project brain and relevant source code, examine connection ownership, and compare approaches without revisiting predetermined protocol details.

**Illustrative findings:**

- `ClientConnection` owns the client's TCP socket.
- `ServerSession` owns each accepted server connection.
- Both currently serialize headers independently.
- An existing `shared/` package could host a stateless codec.

**Proposed direction:** Introduce a shared codec, preserve the current connection owners, and avoid a new transport-management layer.

**Legitimate unresolved questions:**

- Should a malformed frame terminate a TCP session, or should recovery be attempted? (The protocol defines invalid-frame detection but not connection recovery.)
- Should unknown message types be rejected during decoding or passed to application dispatch?

Claude should **not** ask whether fields are little-endian or big-endian: the protocol already decides that.

**Approval checkpoint:** Agree on the architectural direction and the genuinely unresolved failure semantics.

## Step 2: `/brain-write-spec` — Define correctness

**Model (main session):** **Opus** (`brain-write-spec`).

**Example prompt:**

> `/brain-write-spec`
>
> Write the TCP messaging specification from our approved direction. Treat `protocol/wire-v1.md` as authoritative. Include conformance examples for each message type and important framing edge cases.

The resulting feature specification might include:

| ID | Requirement |
|---|---|
| R1 | Encode each frame exactly according to protocol v1. |
| R2 | Decode each message payload using its specified field layout. |
| R3 | Handle TCP fragmentation and coalescing correctly. |
| R4 | Reject malformed frames according to the approved error policy. |
| R5 | Preserve existing client/server connection ownership. |
| R6 | Support bidirectional messaging without introducing another transport manager. |

Require **golden byte vectors**: literal input values and expected byte sequences for each message type, including invalid cases. A round-trip test alone does not prove protocol compliance.

Also spell out stream behavior: one TCP receive call may return part of a frame, several frames, or an arbitrary mixture. TCP does **not** preserve message boundaries.

**Approval checkpoint:** Approve expected behavior, conformance examples, error handling, and binding architectural constraints.

**Optional coordination:** If the feature spans many modules or sessions, use `brain-plan` to organize phases and dependencies. Use `brain-decompose-feature` before code-level design when distinct functional responsibilities need definition; generate tasks with `brain-write-tasks` **after** the technical plans are approved. Neither replaces the specification.

## Step 3: `/brain-decompose-feature` — Define functional components

**Model (main session):** **Sonnet** (`brain-decompose-feature`).

For a substantial TCP messaging feature, first map the approved requirements to functional components such as message contract, framing/stream handling, dispatch, and lifecycle behavior. Produce `03-components/` documents with `CMP-` identifiers and qualified `SPEC-...#REQ-...` coverage; get approval of functional boundaries. Do not assume each functional component becomes a software class or service.

## Step 4: `/brain-design-implementation` — Agree on the actual code design

**Model (main session):** **Opus** (`brain-design-implementation`).

**Example prompt:**

> `/brain-design-implementation`
>
> Create a collaborative implementation blueprint from the approved specification.
>
> I want to review the actual classes, responsibilities, important method signatures, buffer management, and call flow before implementation.
>
> Prefer the smallest changes to the existing connection classes. Show which code will be shared and which code remains client/server-specific.

**Illustrative proposal:**

| File | Responsibility |
|---|---|
| `shared/wire_codec.py` | Pure frame and payload encoding/decoding. |
| `shared/stream_decoder.py` | Incremental TCP buffering and complete-frame extraction. |
| `client/connection.py` | Existing client socket owner; uses codec. |
| `server/session.py` | Existing server socket owner; uses codec. |
| `server/dispatch.py` | Existing application dispatch; receives decoded messages. |

**Proposed interfaces (illustrative Python):**

```python
class WireCodec:
    @staticmethod
    def encode(frame: Frame) -> bytes:
        """Return the exact protocol-defined bytes."""

    @staticmethod
    def decode(frame_bytes: bytes) -> Frame:
        """Validate and decode one complete frame."""


class StreamDecoder:
    def feed(self, data: bytes) -> list[Frame]:
        """
        Accumulate arbitrary TCP chunks.
        Extract complete frames in order.
        Preserve incomplete frames.
        Reject invalid lengths before unbounded buffering.
        """
```

**Explicitly unchanged:** Existing connection ownership, session lifecycle, application message handlers, and protocol-defined field formats.

Now suppose you disagree with a separate stream-decoder class:

> I don't want a separate `StreamDecoder` class. I'd rather keep the receive buffer inside each existing connection object and use a stateless codec to identify and decode complete frames. Show me how that works.

Claude should evaluate the alternative, revise the blueprint if valid, and explain any concrete correctness risks. It might retain `WireCodec` while using a private buffer method in each current connection owner.

The blueprint should label **binding decisions** separately from **suggested signatures or pseudocode**.

**Approval checkpoint:** You explicitly approve the code-level design before production code is modified.

## Step 5: `/brain-write-tasks` — Define executable work

**Model (main session):** **Sonnet** (`brain-write-tasks`).

From the approved code-level plans, create `05-tasks/` files with `TASK-` IDs, concrete technical actions, genuine dependencies, and verification criteria. Preserve the plan's decisions and map each requirement to the tasks that implement it. Skip task files when one small change can be implemented directly.

## Step 6: `/brain-implement` — Build and review coherent increments

**Model (main session):** **Sonnet** (`brain-implement`).

In collaborative mode, Claude implements a small testable behavior, verifies it, presents the actual code changes, and **waits for approval** before advancing.

**Increment 1 — Wire encoding/decoding**

- Write protocol-conformance tests first.
- Implement shared encoding and decoding.
- Verify exact bytes for supported message types and invalid inputs.
- Review data structures, byte encoding, field validation, and signatures.

**Increment 2 — TCP stream handling**

- Support incomplete frames, multiple frames per read, and malformed lengths.
- Preserve the existing session-owned receive buffers and lifecycle.
- Review buffering, state ownership, errors, and cleanup.

**Increment 3 — Client/server integration**

- Wire the codec into both real send and receive paths.
- Verify dispatch, ACKs, bidirectional communication, and partial writes.
- Review call flow and responsibility boundaries.

**Increment 4 — End-to-end conformance**

- Test required message types, invalid frames, lifecycle behavior, and interoperability.
- Inspect the complete feature diff and integration results.

**Illustrative result after increment 1:**

> Increment 1 ready for review.
>
> Changed: `shared/wire_codec.py`, `tests/test_wire_codec.py`.
>
> Golden-vector tests and invalid-length tests pass. Exact bytes match the specification. No approved-design deviations.
>
> Waiting for your review before TCP stream handling.

You inspect the code and request a refinement:

> Extract common field constraints into one validation function. I want one authoritative place for message field ranges, but encoding and decoding should remain separate. Show the revised diff and rerun the tests.

Claude makes the correction and presents the revised increment. Only after you approve does work continue.

## Step 7: `/brain-review-code` — Independent final review

**Model (main session):** **Sonnet** (`brain-review-code`).

**Example prompt:**

> `/brain-review-code`
>
> Review the entire TCP messaging implementation against its pre-implementation Git baseline.
>
> Use the approved protocol specification, feature specification, and implementation blueprint.
>
> Pay particular attention to exact byte layouts, TCP fragmentation, malformed frames, connection lifecycle, client/server interoperability, and deviations from the approved architecture.

The review should assess:

| Area | Questions |
|---|---|
| Correctness | Can malformed packets, partial reads/writes, concurrency, or lifecycle failures break behavior? |
| Requirements | Does each message match its golden vector and the approved specification? |
| Repository fit | Were ownership, dependency direction, and scope preserved? |

**Illustrative finding:**

> **High — TCP send path does not handle partial writes.** `client/connection.py:148` calls `socket.send(frame_bytes)` once and assumes all bytes were transmitted. A partial send can silently truncate a frame. Use the established blocking or nonblocking send strategy to ensure all bytes are transmitted without changing ownership.

Claude proposes a focused correction, you review it, and the tests run again. For substantial work, `brain-implement` may invoke `brain-review-code` as part of its final review; avoid duplicating the same assessment unnecessarily.

Finally, `brain-update` records durable verified knowledge according to the project's branch and ownership rules.

**Completion condition:** Approved requirements are covered, blocking review findings are resolved, verification is recorded, and collaborative checkpoints are approved.

---

# Scenario 2 — Implement a smaller feature

**Goal:** Display the timestamp of the most recently received UDP heartbeat in the client's connection-status panel. The protocol and timeout logic already exist and do not need modification.

## Step 1: Go directly to `/brain-implement`

**Model (main session):** **Sonnet** (`brain-implement`).

**Example prompt:**

> `/brain-implement`
>
> Add the last-received UDP heartbeat time to the client status panel.
>
> Requirements:
> - Use the existing UDP heartbeat receiver.
> - Display the timestamp in local time.
> - Show "Never received" before the first heartbeat.
> - Do not change the UDP packet format or existing timeout logic.
> - Follow existing UI patterns.
>
> This is a small, settled change. No separate blueprint is needed. Use collaborative mode.

Claude reads relevant project knowledge and inspects the heartbeat receiver, connection state, status panel, and tests. Suppose `lastHeartbeatReceivedAt` already exists but is not displayed. Claude should reuse it rather than redesign heartbeat handling.

## Step 2: Implement one reviewable increment

**Model (main session):** **Sonnet** (`brain-implement`).

Illustrative files:

```text
client/
  network/heartbeat_receiver.py  (unchanged)
  state/connection_status.py      (possibly unchanged)
  ui/connection_panel.py          (modified)
  tests/test_connection_panel.py  (modified)
```

Claude implements the UI behavior, verifies it, presents the diff, and waits for approval.

You might respond:

> Use our existing date formatter instead of adding a new one.

Claude adjusts the code, reruns verification, and presents the revised diff.

## Step 3: Finish

**Models (main session):** **Sonnet** (`brain-implement`); **Sonnet** (`brain-update`).

`brain-update` is optional when durable project knowledge needs synchronization.

After approval, Claude checks relevant regressions and reports the result. `brain-update` is appropriate only if the work introduces meaningful durable project knowledge.

**Skills:** `brain-implement`, with `brain-update` as appropriate. No brainstorming, feature plan, spec, tickets, or blueprint is necessary for this settled, local change.

---

# Scenario 3 — Fix a server-to-client binary message bug

**Goal:** Fix an ACK payload serialized using little-endian instead of the required big-endian order.

For sequence 42 and status 0:

**Expected 5-byte payload:**

```text
00 00 00 2A 00
```

**Actual incorrect payload:**

```text
2A 00 00 00 00
```

## Step 1: `/brain-diagnose` — Trace the fault before editing

**Model (main session):** **Sonnet** (`brain-diagnose`).

**Example prompt:**

> `/brain-diagnose`
>
> The server is emitting malformed ACK messages.
>
> For acknowledged sequence 42 and status 0, the payload should be `00 00 00 2A 00`, but we observe `2A 00 00 00 00`.
>
> Investigate the cause. Trace the complete server-side serialization path, compare it with the authoritative protocol specification, and identify the smallest correct fix.
>
> Diagnose only for now; don't change code.

Claude follows the real outbound ACK path rather than assuming the first matching function is responsible. Suppose it finds:

```python
def encode_ack(sequence: int, status: int) -> bytes:
    return sequence.to_bytes(4, "little") + bytes([status])
```

An appropriate diagnosis is that ACK payload encoding uses the wrong byte order while the shared frame header uses big-endian correctly. This isolates the likely scope to ACK payload serialization, subject to tracing callers and tests.

**Checkpoint:** You approve the minimal corrective approach.

## Step 2: Apply the smallest fix with a literal regression test

**Models (main session):** **Sonnet** (`brain-diagnose`); **Sonnet** (`brain-implement`).

A bounded authorized repair can stay in `brain-diagnose`; use `brain-implement` if implementation is handed off.

**Example prompt:**

> Apply the minimal fix. Add a regression test asserting the exact expected bytes. Don't change the codec API or other message types.

**Illustrative regression test:**

```python
def test_ack_payload_uses_big_endian():
    result = encode_ack(sequence=42, status=0)
    assert result == bytes.fromhex("00 00 00 2A 00")
```

The implementation should use the protocol's big-endian encoding and otherwise remain within scope.

**Important:** Do not rely exclusively on `decode(encode(value)) == value`. An encoder and decoder that share the same endianness bug could pass that round-trip test. Assert a literal authoritative byte vector.

Claude checks related message encoders for the same defect, runs verification, and presents the changed code.

## Step 3: Decide whether broader review is warranted

**Models (main session):** **Sonnet** (`brain-diagnose`); **Sonnet** (`brain-review-code`); **Sonnet** (`brain-update`).

Code review and Brain synchronization are conditional; they are not required for every isolated fix.

For an isolated one-line defect with a strong regression test, proportional self-review may suffice. If multiple message types have inconsistent byte ordering, expand the scope deliberately and consider `brain-review-code`.

**Skills:** `brain-diagnose` → focused implementation/fix → optional `brain-review-code` → `brain-update` if durable knowledge needs recording. Do not require brainstorming or a blueprint for a well-understood isolated repair.

---

# Scenario 4 — Review and simplify spaghetti architecture

**Goal:** Improve a client/server design with tangled networking, serialization, business logic, logging, retry behavior, and unclear APIs. You want simpler ownership and better separation of concerns, guided by SOLID and DRY rather than dogmatic pattern adoption.

## Step 1: `/brain-review-architecture` — Discover evidence

**Model (main session):** **Opus** (`brain-review-architecture`).

Standalone architecture reviews save a revision-specific report under `.brain/reviews/architecture/<NN>-<slug>/review.md` when a writable brain exists. Subsequent reviews validate prior findings against current code rather than assuming they remain correct.

**Example prompt:**

> `/brain-review-architecture`
>
> Review the client/server architecture for maintainability problems.
>
> I'm particularly concerned about:
> - Excessively coupled modules and services.
> - Violations of single responsibility.
> - Duplicated serialization and networking logic.
> - Difficult-to-understand APIs.
> - Unclear state and lifecycle ownership.
>
> Use SOLID and DRY as evaluation principles, but don't recommend abstractions just to satisfy a pattern.
>
> Investigate the existing implementation, explain concrete problems, and suggest opportunities to simplify it.
>
> Do not modify code.

Claude reads the project brain, then investigates actual dependencies, callers, state transitions, and tests. A useful report names concrete problems instead of announcing that the entire codebase needs replacement.

**Illustrative findings:**

1. **Duplicated wire serialization:** Client and server independently encode the same message types. Validation is repeated in several modules, increasing drift risk.
2. **Excessive `ServerSession` responsibilities:** The class owns socket I/O, parses frames, executes commands, writes database records, and creates responses. Business changes require touching networking code.
3. **Unnecessary wrapper layers:** `ClientMessageService` mostly delegates to `ClientConnection` and adds little meaningful behavior.

You decide to investigate the first two findings.

## Step 2: Focus the architectural alternatives

**Model (main session):** **Opus** (`brain-review-architecture`).

**Example prompt:**

> `/brain-review-architecture`
>
> Focus on serialization duplication and excessive responsibilities in `ServerSession`.
>
> Compare minimal refactoring against introducing separate codec and dispatch components.
>
> I want cleaner APIs, but I don't want a collection of managers, factories, and interfaces unless they solve real problems.

Claude compares a small extraction with a more substantial redesign. An illustrative separation is:

```text
ClientConnection / ServerSession
    | Own sockets, send queues, receive buffers,
    | and connection lifecycle
    v
WireCodec                 MessageDispatcher
    | Serialize/parse     | Route decoded messages
    | protocol data       | to existing handlers
```

These are **proposals**, not approved changes. Claude may recommend first extracting a shared codec and then simplifying dispatch as a separate increment.

## Step 3: `/brain-brainstorm` — Choose an approved direction

**Model (main session):** **Opus** (`brain-brainstorm`).

**Example prompt:**

> `/brain-brainstorm`
>
> I want to proceed with simplifying serialization and server-side dispatch.
>
> My preferences:
> - Preserve socket ownership in existing connection classes.
> - Use a stateless shared codec.
> - Keep message handlers independent of raw TCP buffers.
> - Prefer direct, explicit dispatch over a generic event bus.
> - Avoid adding interfaces where there's only one implementation and no meaningful need for substitution.
>
> Help me resolve the remaining architectural choices and migration constraints.

Claude identifies genuinely consequential questions: Are public connection APIs allowed to change? Must existing behavior and error semantics remain byte-for-byte compatible? Can responsibility move between components? The approved choices become binding design constraints.

## Step 4: `/brain-write-spec` and `/brain-design-implementation`

**Models (main session):** **Opus** (`brain-write-spec`); **Opus** (`brain-design-implementation`).

For refactoring, the specification should emphasize what **must not change**:

- Existing commands must produce the same protocol-defined bytes.
- Public API compatibility remains unless a specific change is approved.
- Connection lifecycle and error semantics remain unchanged.
- The new architecture must not introduce duplicate state ownership.

Then use `brain-design-implementation` to design actual responsibilities and APIs.

**Before (illustrative):**

```python
class ServerSession:
    def on_bytes(self, data: bytes):
        # Accumulates bytes
        # Parses frames
        # Decodes messages
        # Executes commands
        # Writes database records
        # Sends responses
        ...
```

**After (initial proposal):**

```python
class ServerSession:
    def on_bytes(self, data: bytes) -> None:
        # Frame extraction remains session-owned.
        # Pass decoded messages to the dispatcher.
        ...


class WireCodec:
    def decode(self, frame: bytes) -> Message:
        # Protocol-specific parsing and validation.
        ...


class MessageDispatcher:
    def dispatch(
        self, message: Message, session: ServerSession
    ) -> None:
        # Route messages to existing business handlers.
        ...
```

You may object:

> I don't want the dispatcher receiving the entire `ServerSession`. That exposes connection internals to the business layer. Give it a narrower interface for sending responses.

Claude should revise the API and evaluate dependency direction before you approve the blueprint. The point is to catch these design issues **before** implementing the refactor.

## Step 5: `/brain-implement` — Refactor in verified slices

**Model (main session):** **Sonnet** (`brain-implement`).

A safe order is:

1. Add characterization tests for the existing protocol and session behavior.
2. Extract shared serialization and prove it emits identical bytes.
3. Route client/server serialization through the shared codec.
4. Extract server dispatch responsibilities without changing observable behavior.
5. Remove obsolete duplication and unnecessary wrappers.
6. Run full regression and architecture/code reviews.

In collaborative mode, each increment has a diff, verification, and your approval before further changes.

**Skills:** `brain-review-architecture` → `brain-brainstorm` → `brain-write-spec` → `brain-design-implementation` → `brain-implement` → `brain-review-code`.

**Boundary:** Architecture reviews provide evidence and recommendations; they do **not** automatically authorize a redesign.

---

# Scenario 5 — Thoroughly review a merge request

**Goal:** Evaluate a GitLab merge request from another developer implementing client/server messaging behavior. Understand the real system and protocol before recommending whether to merge. This is a **read-only** review unless you separately authorize changes.

## Step 1: `/brain-review-merge-request` — Provide MR and requirements

**Model (main session):** **Sonnet** (`brain-review-merge-request`).

**Example prompt:**

> `/brain-review-merge-request`
>
> Review GitLab MR !184 targeting `release/2.3`.
>
> Jira story NET-482 requires:
> - Support the new TCP DATA and ACK messages.
> - Follow the binary protocol v1 specification exactly.
> - Correctly handle fragmented and coalesced TCP frames.
> - Reject malformed message lengths.
> - Preserve existing connection ownership and public APIs.
>
> Perform a full review.
>
> Understand the existing architecture, callers, and established decisions before assessing the changes.
>
> Investigate correctness, edge cases, protocol compliance, concurrency, resource management, test coverage, and architectural fit.
>
> Do not modify code or post review comments.

## Step 2: Establish the actual review baseline and context

**Model (main session):** **Sonnet** (`brain-review-merge-request`).

Claude should load `.brain` root knowledge and relevant specifications and ADRs, then identify the **actual target branch and source commit** rather than assuming `main`.

| Context | What to examine |
|---|---|
| Change set | The real target/source commits, complete MR changes, and relevant history. |
| Protocol | Wire format, message types, field encodings, golden vectors. |
| Client | Changed and unchanged callers, receive buffering, outbound flow, lifecycle. |
| Server | Session ownership, command dispatch, response generation. |
| Tests | What existing and new tests actually demonstrate. |
| Git/CI | Relevant commits, reported checks, prior findings, and any outstanding failures. |

**Do not review only the diff in isolation.** A changed method may appear sound while violating an unchanged caller's assumptions.

## Step 3: Independent code assessments

**Models (main session):** **Sonnet** (`brain-review-merge-request`); **Sonnet** (`brain-review-code`).

Optional specialist reviews use **Opus** (`brain-review-security` or `brain-review-architecture`); delegated reviewer models follow the role policy.

`brain-review-merge-request` uses `brain-review-code` to investigate:

- **Correctness:** Bugs, failure paths, resource lifecycle, concurrency, and network edge cases.
- **Requirements:** Protocol and product-contract conformance, including byte-level golden vectors.
- **Repository fit:** Architectural ownership, API compatibility, coupling, and unintended scope expansion.

For broad changes, separate reviewer contexts and specialist reviews may be appropriate. Security or architecture specialist skills are useful when the evidence warrants them; avoid invoking everything by default.

## Step 4: Report actionable, evidence-backed findings

**Model (main session):** **Sonnet** (`brain-review-merge-request`).

**Illustrative finding R1 — High: Coalesced frames can be lost**

- **Location:** `client/connection.py:214` (example only).
- **Evidence:** The receive path calls `decode_one()` once and clears its buffer.
- **Impact:** If two complete frames arrive in a single TCP read, the second message is discarded.
- **Required correction:** Process all complete frames, retaining any incomplete remainder.

**Illustrative finding R2 — High: ACK payload byte ordering is wrong**

- **Location:** `server/messages/ack.py:57` (example only).
- **Evidence:** The ACK encoder produces `2A 00 00 00` for sequence 42 instead of the required `00 00 00 2A`.
- **Impact:** Standards-conforming clients cannot interpret the affected ACK messages correctly.
- **Required correction:** Use the specified encoding and add a literal golden-vector test.

Claude should also show requirements coverage:

| Requirement | Illustrative result |
|---|---|
| DATA message support | Met |
| ACK message support | Unmet — R2 |
| TCP fragmentation | Met |
| TCP coalescing | Unmet — R1 |
| Malformed length rejection | Met |
| Preserve architecture | Met |

This makes it clear that the existence of required classes and methods does not establish protocol correctness.

## Step 5: Give an advisory merge recommendation

**Model (main session):** **Sonnet** (`brain-review-merge-request`).

**Illustrative outcome:**

> **Recommendation: Request changes.** The MR contains two high-severity correctness defects that prevent compliance with the protocol. The remaining architectural changes appear consistent with established connection ownership. R1 and R2 block merge pending corrections and verification.

The review should identify what tests and CI checks actually ran, and what could not be verified. It should **not** change the MR's approval state or post comments unless explicitly authorized.

## Step 6: Re-review the updated MR

**Model (main session):** **Sonnet** (`brain-review-merge-request`).

After the developer pushes fixes:

> `/brain-review-merge-request`
>
> Re-review MR !184.
>
> Verify that R1 and R2 are resolved. Also check whether the new commits introduce regressions.
>
> Evaluate the entire current merge request, not just the newest patch.

Claude checks the new MR head, relevant verification, and the entire resulting change set. It classifies prior findings as resolved, partially resolved, unresolved, or no longer applicable, and gives an updated recommendation.

**Skills:** `brain-review-merge-request` → `brain-review-code`, with specialist review where justified. There is no need to brainstorm or write a blueprint for a read-only MR review.

---

# Scenario 6 — Build a ZPL printer library and YAML CLI across multiple sessions

This example walks through developing a new project with two components:

1. **A reusable ZPL library** that constructs and renders labels and sends ZPL to compatible printers over TCP, USB, or other approved transports.
2. **A CLI application** that reads YAML label definitions, validates them, renders ZPL using the library, and optionally sends jobs to a printer.

The goal is to build the project over **multiple Claude sessions** while retaining architectural decisions in `.brain/`, reviewing important implementation choices before code is written, and approving small increments of working code.

> **Example assumptions:** The language is Python; initial platforms and printer models are to be decided. API names, file layouts, YAML schemas, and commands shown below are proposals, not established requirements. Confirm them during brainstorming and specification. A transport successfully sending bytes is not proof that the physical label printed.

## Choosing the development workflow

For a project like this, **default to a project-level brainstorm followed by repeated feature-level cycles**. Use `brain-plan` when there are several interdependent unknowns to research or decisions to coordinate across sessions; it is not required simply because the overall project is large.

| Situation | Start with | Why |
|---|---|---|
| The product goals or architecture are undecided | `brain-brainstorm` | Decide *what to build* and key boundaries |
| Multiple technical investigations must be completed before decisions can be made | `brain-plan` | Track research, dependencies, and unresolved questions |
| A feature's requirements are established | `brain-write-spec` or `brain-design-implementation` | Avoid unnecessary preliminary stages |
| The public behavior and code design are already settled | `brain-implement` | Deliver the smallest verified change |

The recurring feature workflow is:

```text
brain-brainstorm (Opus, when needed)
        ↓
brain-write-spec (Opus)
        ↓
brain-decompose-feature (Sonnet, if useful)
        ↓
brain-design-implementation (Opus)
        ↓
brain-write-tasks (Sonnet, if useful)
        ↓
brain-implement (Sonnet by default; collaborative)
        ↓
brain-review-code (Sonnet) / brain-review-security (Opus, as warranted)
        ↓
brain-update (Sonnet)
```

Each skill must respect established specifications, ADRs, and approved decisions. A blueprint does not supersede a specification, and a review finding does not authorize an unapproved redesign.

---

## Session 1 — Initialize the project

**Skill:** `brain-init`  
**Model (main session):** **Sonnet** (`brain-init`).

Create the repository and an initial Git commit, then initialize `.brain/`.

**Example prompt**

```text
/brain-init

I'm starting a project with two components:
- A reusable ZPL library for generating labels and communicating
  with compatible printers.
- A CLI application that reads YAML label definitions and uses
  the library to render or print labels.

The project will be developed incrementally across multiple sessions.
I want collaborative approval of architecture and code-level design,
with small implementation checkpoints.
```

At this stage, distinguish **planned capabilities** from **implemented facts**. Record the project's purpose, users, initial scope, terminology, known constraints, and unresolved questions. Do not invent settled printer compatibility or transport guarantees.

**Checkpoint:** The project has an initialized brain and collaboration policy; no architecture has been implemented merely because it was discussed.

## Session 2 — Brainstorm the project-level direction

**Skill:** `brain-brainstorm`  
**Model (main session):** **Opus** (`brain-brainstorm`).

Define the broad architecture and first usable release without trying to specify every feature.

**Example prompt**

```text
/brain-brainstorm

Help me establish the architecture and MVP for a ZPL printing library
and a YAML-based CLI.

My preferences:
- The core library must not depend on the CLI or YAML parsing.
- Label rendering must work without a connected printer.
- Transport implementations should deliver ZPL, not generate it.
- Prefer explicit, maintainable APIs over plugin frameworks.
- I want to design and implement one feature at a time.

Investigate any existing code and project decisions. Challenge my
preferences if they cause concrete correctness or maintenance problems.
Don't design every internal method yet.
```

Topics to settle or record as open questions:

- Supported printers, platforms, and ZPL capabilities for the first release.
- Whether label data is immutable, mutable, or builder-based.
- Whether rendering returns `str` or encoded `bytes`, and where encoding is defined.
- How the CLI depends on the library's public APIs.
- How printing errors and unknown delivery outcomes are represented.
- Which features belong in the MVP versus later releases.

**Possible approved direction (illustrative):**

```text
YAML CLI ────────> Public library API
                        ├── Label model
                        ├── ZPL renderer
                        └── Printer transports
                                  ├── TCP (MVP)
                                  └── USB (later)
```

**Checkpoint:** Approve architectural boundaries and MVP scope. Record durable decisions in `.brain/` without prematurely committing to private helper names.

## Optional Session 3 — Plan investigations with `brain-plan`

**Skill:** `brain-plan`  
**Model (main session):** **Opus** (`brain-plan`).

**Use this only when needed.** For example, if USB printing across Windows, Linux, and macOS is in scope but the supported printer interfaces, driver requirements, permissions, and reliability guarantees are unclear, create a multi-session investigation plan.

**Example prompt**

```text
/brain-plan

Plan the investigations needed for cross-platform USB printing.
Research the supported printer models, OS print queues, direct USB
access, drivers, permissions, printer status reporting, and transport
failure semantics.

Identify dependencies and decisions that must be resolved before an
implementation design is approved. Don't create a generic backlog or
start implementing USB support.
```

Example planning topics:

```text
.brain/planning/usb-printing/
├── INDEX.md
├── 001-printer-and-os-matrix.md
├── 002-connection-mechanisms.md
├── 003-permissions-and-drivers.md
├── 004-status-and-failure-semantics.md
└── 005-test-hardware.md
```

The planning artifacts organize **research and decisions**. They are not a substitute for feature specifications, implementation tickets, or blueprints. After research, return to `brain-brainstorm` for remaining architectural choices.

**Checkpoint:** Investigations have evidence and identified unresolved decisions; no unverified assumption has been recorded as a requirement.

---

## Feature cycle 1 — Render a basic text label

### A. Brainstorm the feature

**Skill:** `brain-brainstorm`  
**Model (main session):** **Opus** (`brain-brainstorm`).

```text
/brain-brainstorm

Let's implement the first vertical slice: construct a label in Python
and render correct ZPL for a text element.

Help me decide the public Label API, element representation, units,
validation, and where encoding belongs. Respect our approved rule
that rendering cannot depend on a printer or the CLI.
```

For example, decide whether label positions are represented in **printer dots**. Supporting millimeters later would require explicit DPI-dependent conversion and rounding behavior.

### B. Write the specification

**Skill:** `brain-write-spec`  
**Model (main session):** **Opus** (`brain-write-spec`).

```text
/brain-write-spec

Write the spec for constructing and rendering a text label.
Capture the approved API constraints, supported commands, limits,
invalid inputs, and exact expected ZPL examples.
Do not add barcodes, YAML, or printing to this feature's scope.
```

An example golden output for a simple label:

```zpl
^XA
^PW600
^LL400
^FO20,30
^A0N,30,30
^FDHello World^FS
^XZ
```

This is an **illustrative test vector** until checked against the approved renderer behavior and target printer requirements. Tests should compare expected command output, not merely check that rendering returns a nonempty string.

### C. Approve a code-level blueprint

**Skill:** `brain-design-implementation`  
**Model (main session):** **Opus** (`brain-design-implementation`).

```text
/brain-design-implementation

Design the minimal code structure for the approved label-rendering spec.
Show the package layout, public API, element types, important method
signatures, validation flow, and tests.

I want to review and adjust the interfaces before implementation.
Distinguish binding design decisions from illustrative private helpers.
```

An illustrative blueprint might propose:

```python
@dataclass(frozen=True)
class Label:
    width_dots: int
    height_dots: int
    elements: tuple[LabelElement, ...]


def render_zpl(label: Label) -> bytes:
    """Serialize a validated label into ZPL bytes."""
```

You might instead request `Label.render()` or a builder API. Claude should evaluate the alternatives and **revise the blueprint before coding**. The approved design belongs in the feature's `.brain/impl_plans/` document.

### D. Implement collaboratively

**Skill:** `brain-implement`  
**Model (main session):** **Sonnet** (`brain-implement`). Opus can be appropriate for unusually difficult design or encoding concerns.

```text
/brain-implement

Implement the approved basic label-rendering blueprint in
collaborative mode. Write targeted specification-derived tests first.
After each small, working increment, present the diff and test results
and wait for my approval before proceeding. Preserve any manual edits.
```

Possible increments:

1. Label model and validation.
2. Text field rendering with exact expected ZPL.
3. Unsupported or malformed input handling.

**Checkpoint:** The library can render a label correctly without YAML or a printer. Review the resulting API *before* building other features on it.

---

## Feature cycle 2 — Read and validate YAML labels

**Skills:** `brain-brainstorm` → `brain-write-spec` → `brain-design-implementation` → `brain-implement`  
**Models (main session):** **Opus** (`brain-brainstorm`); **Opus** (`brain-write-spec`); **Opus** (`brain-design-implementation`); **Sonnet** (`brain-implement`).

The YAML schema is a **public contract**. Decide its shape deliberately rather than letting the CLI parser invent one while coding.

**Brainstorm prompt**

```text
/brain-brainstorm

Design a versioned, human-readable YAML label format that maps to
our existing library models. Start with text elements; allow a future
barcode type without unnecessary abstraction.

Discuss required fields, defaults, unknown properties, validation,
error messages, and how text containing ZPL control characters is
handled safely. Do not change the existing library API without approval.
```

**Illustrative YAML**

```yaml
version: 1
label:
  width_dots: 600
  height_dots: 400
  elements:
    - type: text
      x: 20
      y: 30
      value: "Hello World"
      font_size: 30
```

**Spec prompt**

```text
/brain-write-spec

Write a focused specification for YAML v1 parsing and validation.
Include valid examples, malformed YAML, missing required fields,
unknown elements, invalid values, and expected error semantics.
```

**Blueprint prompt**

```text
/brain-design-implementation

Design the smallest YAML loader that converts validated input into
existing public library models. The library must not import YAML or
CLI modules. Show functions, errors, and tests before coding.
```

**Implementation prompt**

```text
/brain-implement

Implement YAML validation and conversion in collaborative increments.
First cover parsing and validation with tests, then the render CLI
command. Show each verified diff and stop for review.
```

Proposed CLI commands (subject to approval):

```bash
zplcli validate label.yaml
zplcli render label.yaml --output label.zpl
```

**Checkpoint:** The CLI can validate and render from YAML without interacting with hardware. Input cannot inject unintended ZPL commands via unsafely interpolated text.

---

## Feature cycle 3 — Add TCP printing

**Skills:** `brain-brainstorm` (if needed) → `brain-write-spec` → `brain-design-implementation` → `brain-implement`  
**Models (main session):** **Opus** (`brain-brainstorm`); **Opus** (`brain-write-spec`); **Opus** (`brain-design-implementation`); **Sonnet** (`brain-implement`). Implementation may warrant Opus for unusually complex concurrency or failure semantics.

**Feature prompt**

```text
/brain-brainstorm

Add TCP delivery for rendered ZPL. Keep socket ownership inside the
transport and keep rendering independent of network I/O.

Help decide the transport API, timeouts, partial-send behavior,
exceptions, retry policy, and what counts as successful delivery.
Don't claim a physical print succeeded without printer confirmation.
```

The specification must make failure behavior testable. The blueprint should show the transport's public API, connection lifetime, resource cleanup, and how the CLI invokes it.

**Illustrative interface**

```python
class TcpPrinter:
    def __init__(self, host: str, port: int = 9100) -> None:
        ...

    def send(self, zpl: bytes) -> None:
        """Transmit ZPL completely or report a delivery error."""
```

The port is a common default for raw TCP printing, not a universal printer guarantee. The exact transport contract remains subject to approved requirements.

**Implementation prompt**

```text
/brain-implement

Implement the approved TCP transport and CLI print command.
Use a local fake-printer TCP endpoint in tests. Verify exact bytes,
connection errors, timeouts, interrupted/partial sends, and resource
cleanup. Do not print to real hardware during automated tests.

Work in collaborative mode and stop after each verified increment.
```

Proposed CLI command:

```bash
zplcli print label.yaml --tcp 192.168.1.50:9100
```

**Checkpoint:** A fake printer receives the expected exact bytes, and a controlled test with a real compatible printer is completed where hardware is available. Hardware-dependent claims remain explicitly unverified otherwise.

---

## Feature cycle 4 — Add barcodes and richer layout

**Skills:** `brain-brainstorm` → `brain-write-spec` → `brain-design-implementation` → `brain-implement` (use only needed stages)  
**Models (main session):** **Opus** (`brain-brainstorm`); **Opus** (`brain-write-spec`); **Opus** (`brain-design-implementation`); **Sonnet** (`brain-implement`).

```text
/brain-brainstorm

Extend the library and YAML v1 format to support Code 128 barcodes.
Use the established label model and renderer architecture. Identify
barcode-specific constraints, field encoding rules, validation, and
printer compatibility without changing existing text behavior.
```

Example YAML element to discuss:

```yaml
- type: code128
  x: 20
  y: 100
  value: "123456789"
  height: 80
```

Produce golden ZPL tests for the supported barcode behavior and regression tests proving existing text labels remain unchanged. Use the blueprint to approve any necessary changes to the element model before implementation.

**Checkpoint:** The renderer and YAML schema remain coherent and backward compatible with the approved v1 behavior.

---

## Feature cycle 5 — Add USB printing

**Skills:** `brain-plan` (if feasibility is unresolved) → `brain-brainstorm` → `brain-write-spec` → `brain-design-implementation` → `brain-implement`  
**Models (main session):** **Opus** (`brain-plan`); **Opus** (`brain-brainstorm`); **Opus** (`brain-write-spec`); **Opus** (`brain-design-implementation`); **Sonnet** (`brain-implement`).

USB is not simply TCP with a different address. Supported printer interfaces, OS queues, permissions, drivers, and bidirectional status capabilities may differ.

**Design prompt**

```text
/brain-design-implementation

Design USB printing for the approved printer/OS support matrix and
connection mechanism. Reuse the existing rendering and print-job path.

Evaluate whether adding a shared transport contract is now justified
by two real implementations. Show public APIs, lifecycle, failure
semantics, permissions, and tests. Do not assume direct USB access is
available on every target platform.
```

Only implement after you approve the design. Where actual supported hardware or OS environments are unavailable, distinguish simulated tests from real-device verification.

**Checkpoint:** USB support is verified on each platform and printer model the project claims to support, or those claims are narrowed accordingly.

---

## Session — Independent code and security reviews

**Skills:** `brain-review-code`, optionally `brain-review-security` and `brain-review-architecture`  
**Models (main session):** **Sonnet** (`brain-review-code`); **Opus** (`brain-review-security`); **Opus** (`brain-review-architecture`). Delegated reviewers follow `CLAUDE.local.md` role assignments.

Run a full review at meaningful release milestones, even if individual increments were already tested and reviewed.

**Code-review prompt**

```text
/brain-review-code

Review the ZPL library and CLI against their approved specifications,
blueprints, and current source code. Include relevant callers and
integration paths, not only changed lines.

Focus on ZPL correctness, escaping and encoding, YAML validation,
resource cleanup, TCP/USB failures, public API stability, test gaps,
architectural boundaries, and unsupported hardware claims.

Report evidence-backed, actionable findings. Do not silently expand
scope or implement unapproved redesigns.
```

**Security-review prompt**

```text
/brain-review-security

Assess untrusted YAML input, ZPL command injection, user-supplied
printer destinations, network and filesystem access, dependency risk,
and safe CLI failure handling. Identify concrete risks and feasible
mitigations without speculative redesign.
```

Claude should distinguish **blocking bugs**, **unverified risks**, and **optional improvements**. Fix blocking defects in reviewable increments and re-review the corrected code.

---

## Final session — Package, document, and release

**Skills:** `brain-implement`, `brain-update`  
**Models (main session):** **Sonnet** (`brain-implement`); **Sonnet** (`brain-update`).

```text
/brain-implement

Finish packaging the approved ZPL library and CLI for release.
Verify installation in a clean environment, public imports, console
entry points, sample YAML files, CLI usage, exit codes, and the
supported printer/platform matrix.

Use collaborative checkpoints for meaningful changes. Do not claim
hardware verification that wasn't performed.
```

Illustrative end-user workflow:

```bash
pip install zplkit
zplcli validate label.yaml
zplcli render label.yaml --output label.zpl
zplcli print label.yaml --tcp 192.168.1.50:9100
```

These are proposed distribution and command names, not real package-installation instructions until the project adopts and publishes them.

Run `brain-update` to record verified current architecture, API behavior, supported transports, implementation status, and durable decisions. Preserve source references where detailed ZPL or platform behavior comes from authoritative documentation.

**Release criteria:** Approved specifications are covered, automated checks pass, blocking review findings are resolved, packaging works from a clean environment, and remaining limitations are explicit.

---

## Resuming the work in a new Claude session

**Model (main session):** **Sonnet** (`brain-implement`).

Each session should consult the project brain, relevant specifications, the approved blueprint, the current implementation plan, and Git state. Progress notes are continuity aids, not proof that code is current or tested.

**Continuation prompt**

```text
Continue the ZPL toolkit from the current `.brain` state.

Identify the next approved, actionable feature or increment. Read the
relevant decision records, specification, and blueprint, then verify
that prior progress still matches the current code and Git state.
Preserve any manual changes I made since the previous session.

Use collaborative implementation: deliver one coherent, tested
increment, show the diff and verification, and stop for my approval.
Don't reopen established decisions without concrete new evidence.
```

### Where each kind of information lives

| Location | Responsibility |
|---|---|
| `.brain/` root knowledge | Project purpose, current architecture, APIs, terminology, decisions, feature state |
| `.brain/planning/` | Optional multi-session investigations and unresolved dependencies |
| `.brain/specs/` | Approved, testable feature requirements |
| `.brain/tickets/` | Implementation deliverables, when tickets are useful |
| `.brain/impl_plans/` | Approved code-level blueprint and execution checkpoints |
| `.brain/adrs/` | Durable architectural decisions and their rationale |
| Original technical sources | Exact ZPL commands, supported device behavior, platform contracts, and other authoritative details |

### Recommended first milestone

Complete **an end-to-end TCP label-printing path** before pursuing broad printer compatibility:

- Construct and render a text label with the public library API.
- Validate and render versioned YAML via the CLI.
- Print through raw TCP with clear failure semantics.
- Add Code 128 and other label elements as specifically approved.
- Verify exact generated ZPL and bytes sent to a fake printer.
- Perform a controlled real-printer test where possible.

Defer USB, discovery, detailed printer status, advanced layout, and more transports until the core API has been exercised and validated.

**Guiding principle:** Let the project brainstorm establish the architectural foundation, then iterate feature by feature through specification, approved blueprint, collaborative implementation, and independent review. Bring in `brain-plan` only when the path to a decision genuinely requires coordinated investigation.

---

# Scenario 7 — Change an approved feature during implementation

**Default: call `/brain-change` once the change is proposed or decided.** It identifies and invokes only the required documentation skills in order, pausing for your approvals. You do **not** need to select `brain-write-spec` or `brain-design-implementation` yourself. It never runs `brain-implement` or treats a plan approval as permission to write code. When skill invocation is unavailable, it supplies the exact next command instead of silently editing another skill's files.

**After `brain-brainstorm` (with the agreed decision recorded):**

```text
/brain-change yaml-cli

Reconcile our confirmed decision to warn instead of error on unknown
YAML fields. Invoke only the affected document-owning skills and obtain
required approvals. Do not implement code.
```

**After an ordinary conversation (no brainstorming required):**

```text
/brain-change yaml-cli

I want unknown YAML fields to generate warnings instead of errors.
Identify unresolved consequential details and reconcile affected specs,
components, plans and tasks through their owning skills.
Do not implement code.
```

**Model (main session):** **Opus** (`brain-change`; Sonnet is appropriate for a narrow, settled change). The longer steps below describe the manual fallback and approval gates, not a mandatory list of commands to type after `/brain-change`.

Suppose the ZPL YAML CLI from Scenario 6 has an **approved specification and implementation plan**. `brain-implement` has already added parsing and tests, but you decide that unknown YAML fields should produce **warnings** instead of errors. That changes observable behavior, so simply editing `.brain/09_user_decisions.md`, discussing it in chat, or modifying implementation code is **not enough**: the owning feature documents and affected approvals must be reconciled.

**Choose the smallest revision path:**

| Kind of change | Workflow before resuming implementation |
|---|---|
| Undecided behavior or consequential architecture | `brain-brainstorm` first; then the applicable owning skills below |
| New or changed requirement, invariant, public error, or acceptance example | `brain-write-spec` → review affected components/plans/tasks through their owners |
| Only the binding code design changes; required behavior stays the same | `brain-design-implementation` → `brain-write-tasks` if affected tasks exist; **skip `brain-write-spec`** |
| Only task sequencing or acceptance evidence changes, within an approved design | `brain-write-tasks` when existing tasks need revision; otherwise `brain-implement` |
| A small reversible implementation detail consistent with approved plans | Continue in `brain-implement`; no document rewrite needed |

## Step 1: Pause affected implementation and preserve evidence

**Model (main session):** **Sonnet** (`brain-implement`).

Before changing an approved requirement, stop only the affected work. Preserve already-reviewed increments, uncommitted changes and the real test results. Independent, authorized work whose governing documents are unchanged may continue.

**Example prompt in the active implementation session:**

```text
/brain-implement

Pause implementation of the YAML unknown-field behavior. I may change
its acceptance rule. Record the current verified status, remaining
work, and the affected scope in execution.md. Preserve existing code
and tests; do not implement the proposed behavior yet.
```

## Step 2: Resolve the new decision, if necessary

**Model (main session):** **Opus** (`brain-brainstorm`).

If you already made an unambiguous decision, **skip this step**. You can discuss the change with Claude directly; `brain-brainstorm` is useful when semantics, compatibility or consequences still need a decision.

**Optional prompt:**

```text
/brain-brainstorm

For the YAML CLI, I am considering warnings instead of errors for
unknown fields. Compare rejecting, ignoring, and warning; cover nested
fields, forward compatibility, and CLI exit status. Preserve other
approved validation rules. Do not edit implementation code.
```

A conversation or updated brief records the agreed direction, **not** automatic approval of an as-yet-unwritten revised specification or plan.

## Step 3: Revise the specification if behavior changed

**Model (main session):** **Opus** (`brain-write-spec`).

For the example, this step is necessary because the accepted input and failure behavior change.

```text
/brain-write-spec

Revise the existing YAML-validation specification to reflect the
approved unknown-field warning behavior. Preserve existing document,
requirement, and example IDs; assign new IDs only where needed.

Show the changed requirements, examples, compatibility constraints,
and expected CLI results. Mark a materially revised approved spec
needs-revision until I explicitly approve the written revision.

Identify which components, implementation plans, and tasks depend on
this specification. Do not edit their documents or approval states.
Do not implement code.
```

`brain-write-spec` owns `02-specifications/`. It should report affected descendants, **not** silently rewrite `03-components/`, `04-implementation-plans/` or `05-tasks/`. The spec revision must be explicitly approved before affected downstream work resumes.

## Step 4: Revalidate functional decomposition, if used and affected

**Model (main session):** **Sonnet** (`brain-decompose-feature`).

Skip this step when no component documents exist or none is affected. Otherwise review requirement coverage and existing boundaries; preserve stable IDs and unaffected approvals.

```text
/brain-decompose-feature

Reconcile the YAML feature's component documents with the newly
approved specification. Check which components cover the changed
requirement, review dependency and coverage links, and renew affected
approvals and parent fingerprints only after validation.

Do not invent new owners or change binding code design.
```

## Step 5: Revalidate or revise affected implementation plans

**Model (main session):** **Opus** (`brain-design-implementation`).

**You do not always need a new design.** If the revised behavior fits the existing binding design, review and renew affected plan approvals and parent fingerprints as required. If it changes interfaces, error propagation, ownership, lifecycle or another binding choice, revise the design collaboratively and get explicit approval. If a plan's governing documents and binding decisions are unaffected, leave it alone.

```text
/brain-design-implementation

Compare the revised approved YAML specification and any component
documents against the existing implementation plans and current code.

Determine whether the unknown-field warning behavior changes any
binding API, error flow, or ownership decision. Reuse existing plan
IDs and preserve unaffected decisions. Revise affected plans, validate
their governing parent references/fingerprints, and present any
binding changes for my explicit approval.

Do not edit production code or execution.md.
```

A stale parent fingerprint is a **review requirement**, not permission to update a hash without checking the changed parent.

## Step 6: Reconcile affected tasks, if any

**Model (main session):** **Sonnet** (`brain-write-tasks`).

If `05-tasks/` was used and its work items are affected, update their acceptance criteria, examples, dependencies or coverage **after** their governing plans are approved. Reuse existing task IDs; do not reset verified implementation progress. Skip this step when there are no tasks or their approved scope is unaffected.

```text
/brain-write-tasks

Review existing YAML feature tasks against the approved revised
requirements and implementation plans. Revise only affected tasks,
preserve IDs and genuine dependencies, validate coverage and parent
fingerprints, and request any required task approval.

Do not rewrite execution.md or implement code.
```

## Step 7: Explicitly resume implementation

**Model (main session):** **Sonnet** (`brain-implement`).

A revised spec, plan or task approval is **not** implementation authorization. Start a fresh implementation session with an explicit request, inspect actual Git/code/test state and `execution.md`, and verify that all **affected** governing documents are approved and current.

```text
/brain-implement

Resume implementation of the YAML CLI's approved unknown-field
warning behavior. I explicitly authorize the revised implementation.

Read the revised approved spec, applicable component/design/task
documents, and execution.md. Reconcile existing code and tests with
the last reviewed increment and current Git state. Stop if affected
approvals or parent fingerprints are still stale.

Continue in collaborative mode, show each small verified diff and
test result, and wait for approval before proceeding.
```

**If only architecture changed:** skip Steps 2–4 when requirements and functional ownership remain valid; begin at Step 5, then Step 6 only if tasks are affected, followed by Step 7. **If only an illustrative helper or other local implementation detail changed:** stay in `brain-implement` without revisiting the spec or blueprint. A consequential change already approved in conversation still needs to be recorded and validated in its owning document.

`brain-update` may synchronize shared root knowledge, ADRs and indexes after a producing skill records the revision. It does **not** own or reapprove feature specs, components, plans or tasks. A material change to an approved parent requires review of its **affected** descendants; do not automatically invalidate independent work or silently refresh approval hashes.

---

# Quick workflow reference

| Situation | Typical skill sequence | Your involvement |
|---|---|---|
| Large feature, rigid protocol | `brain-brainstorm` → `brain-write-spec` → optional `brain-decompose-feature` → `brain-design-implementation` → optional `brain-write-tasks` → `brain-implement` → `brain-review-code`; use `brain-plan` separately for unresolved research | Approve architecture, spec, blueprint, and implementation increments. |
| Small, settled feature | `brain-implement` | Review the focused change and verification. |
| Isolated protocol bug | `brain-diagnose` → focused fix → optional `brain-review-code` | Review the diagnosis and correction. |
| Architecture cleanup | `brain-review-architecture` → `brain-brainstorm` → `brain-write-spec` → `brain-design-implementation` → `brain-implement` → `brain-review-code` | Choose improvements and shape the exact design. |
| Third-party merge request | `brain-review-merge-request` (uses `brain-review-code`) | Evaluate findings and advisory merge recommendation. |
| New multi-session project (ZPL library + YAML CLI) | `brain-init` → project `brain-brainstorm` → feature-level `brain-write-spec` → `brain-design-implementation` → `brain-implement` → reviews; use `brain-plan` when research needs coordination | Approve core architecture, then review each feature and its code increments. |
| Approved feature changes during implementation | **`brain-change`** invokes only affected owning skills (spec → components → plan → tasks); request `brain-implement` separately after approvals. | Confirm unresolved decisions and approve revised documents; explicitly request implementation. |

## How to communicate an intended design

When you already know how you want the code organized, tell Claude **before** blueprinting:

> I want `TcpSession` to own the connection and receive buffer. I want `WireCodec` to be stateless and handle serialization only. The dispatcher should operate on decoded message objects and have no access to socket internals. I want to review public interfaces, method responsibilities, and call flow before implementation. Challenge any part of this design that creates a concrete correctness or maintainability problem.

The most useful repeated pattern for design-sensitive work is:

**User-directed design → approved specification and blueprint → small testable increments → independent final review.**

For binary protocols, maintain an authoritative conformance suite with **literal golden byte vectors**. It gives implementers and reviewers an objective definition of correctness, independent of style or architectural preferences.
