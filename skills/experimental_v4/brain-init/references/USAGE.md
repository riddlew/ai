# Brain Skills — Usage Guide

This guide explains when to use `brain-brainstorm` versus `brain-plan-feature`, then demonstrates five end-to-end workflows using hypothetical client and server applications that communicate over TCP and UDP.

The prompts, file names, code examples, review findings, and test results are **illustrative**, not results from a real repository. Adapt them to your codebase and the capabilities of your installed skills.

---

# Choosing `brain-brainstorm` vs. `brain-plan-feature`

The distinction is **what you're trying to resolve**:

- **`brain-brainstorm`** — Use when you haven't fully decided *what to build or how it should work*.
- **`brain-plan-feature`** — Use when you know what you want, but need to organize *how to get from the current codebase to that result*.

They're complementary, not necessarily sequential.

| Situation | Use |
|---|---|
| Exploring several possible architectures | `brain-brainstorm` |
| Deciding component ownership or design patterns | `brain-brainstorm` |
| Clarifying ambiguous requirements or behavior | `brain-brainstorm` |
| Understanding dependencies across several modules | `brain-plan-feature` |
| Organizing a large feature into stages and deliverables | `brain-plan-feature` |
| Coordinating work over multiple sessions | `brain-plan-feature` |
| Designing exact classes, APIs, and method signatures | `brain-blueprint` |

## Example: TCP messaging with unsettled architecture

You know the exact wire format but haven't decided where serialization, buffering, and message dispatch should live. Start with **`brain-brainstorm`** to settle those architectural decisions. Use `brain-plan-feature` if implementation then requires coordinating multiple modules, milestones, or investigations. Use `brain-write-spec` and `brain-blueprint` as appropriate to record binding requirements and agree on the code-level design.

## Example: Large feature with settled architecture

You already know the protocol, component ownership, requirements, and implementation approach. **Skip brainstorming.** Use `brain-plan-feature` to organize work across the client, server, shared library, and integration tests. Then create the specification or blueprint needed by the project and implement it.

## Example: Small feature

You want to display the most recent UDP heartbeat timestamp, and the necessary state already exists. **Skip both** `brain-brainstorm` and `brain-plan-feature`; go straight to `brain-implement`.

## Decision rule

1. **Are there unresolved product or architectural choices?** If yes, use `brain-brainstorm`.
2. **Is the work large enough to require coordinated stages, dependencies, or multiple sessions?** If yes, use `brain-plan-feature`.

If both are true, use both. **`brain-plan-feature` is not a substitute for `brain-blueprint`:** planning decides work breakdown and sequencing; blueprinting defines the code-level implementation. You do not need every skill for every feature. Use the smallest workflow that resolves the actual uncertainty and complexity.

---

# Shared example project

Assume a repository contains two applications:

- **Client:** Connects to the server, sends commands, receives responses, and tracks connection state.
- **Server:** Accepts TCP connections, processes commands, sends responses, and sends certain time-sensitive updates over UDP.

The applications already exist and their architecture, APIs, and established decisions are described in `.brain/`. Under the collaboration policy, established requirements and approved decisions remain authoritative. Collaborative implementation is the default: Claude works in small, verifiable increments and pauses for your review.

---

# Scenario 1 — Implement a large feature with a rigid binary protocol

**Goal:** Implement bidirectional TCP messaging across the client and server. Frame layouts, message identifiers, byte order, and per-message payload formats are fixed **before** brainstorming begins. The protocol is non-negotiable; Claude may design the implementation but cannot modify the wire contract to simplify it.

## Step 0: Establish authoritative requirements before brainstorming

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

**Optional coordination:** If the feature spans many modules or sessions, use `brain-plan-feature` to organize phases and dependencies. Use `brain-write-tickets` when independently verifiable work items are valuable. Neither replaces the specification or code-level blueprint.

## Step 3: `/brain-blueprint` — Agree on the actual code design

**Example prompt:**

> `/brain-blueprint`
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

## Step 4: `/brain-implement` — Build and review coherent increments

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

## Step 5: `/brain-review-code` — Independent final review

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

For an isolated one-line defect with a strong regression test, proportional self-review may suffice. If multiple message types have inconsistent byte ordering, expand the scope deliberately and consider `brain-review-code`.

**Skills:** `brain-diagnose` → focused implementation/fix → optional `brain-review-code` → `brain-update` if durable knowledge needs recording. Do not require brainstorming or a blueprint for a well-understood isolated repair.

---

# Scenario 4 — Review and simplify spaghetti architecture

**Goal:** Improve a client/server design with tangled networking, serialization, business logic, logging, retry behavior, and unclear APIs. You want simpler ownership and better separation of concerns, guided by SOLID and DRY rather than dogmatic pattern adoption.

## Step 1: `/brain-review-architecture` — Discover evidence

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

## Step 4: `/brain-write-spec` and `/brain-blueprint`

For refactoring, the specification should emphasize what **must not change**:

- Existing commands must produce the same protocol-defined bytes.
- Public API compatibility remains unless a specific change is approved.
- Connection lifecycle and error semantics remain unchanged.
- The new architecture must not introduce duplicate state ownership.

Then use `brain-blueprint` to design actual responsibilities and APIs.

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

A safe order is:

1. Add characterization tests for the existing protocol and session behavior.
2. Extract shared serialization and prove it emits identical bytes.
3. Route client/server serialization through the shared codec.
4. Extract server dispatch responsibilities without changing observable behavior.
5. Remove obsolete duplication and unnecessary wrappers.
6. Run full regression and architecture/code reviews.

In collaborative mode, each increment has a diff, verification, and your approval before further changes.

**Skills:** `brain-review-architecture` → `brain-brainstorm` → `brain-write-spec` → `brain-blueprint` → `brain-implement` → `brain-review-code`.

**Boundary:** Architecture reviews provide evidence and recommendations; they do **not** automatically authorize a redesign.

---

# Scenario 5 — Thoroughly review a merge request

**Goal:** Evaluate a GitLab merge request from another developer implementing client/server messaging behavior. Understand the real system and protocol before recommending whether to merge. This is a **read-only** review unless you separately authorize changes.

## Step 1: `/brain-review-merge-request` — Provide MR and requirements

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

`brain-review-merge-request` uses `brain-review-code` to investigate:

- **Correctness:** Bugs, failure paths, resource lifecycle, concurrency, and network edge cases.
- **Requirements:** Protocol and product-contract conformance, including byte-level golden vectors.
- **Repository fit:** Architectural ownership, API compatibility, coupling, and unintended scope expansion.

For broad changes, separate reviewer contexts and specialist reviews may be appropriate. Security or architecture specialist skills are useful when the evidence warrants them; avoid invoking everything by default.

## Step 4: Report actionable, evidence-backed findings

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

**Illustrative outcome:**

> **Recommendation: Request changes.** The MR contains two high-severity correctness defects that prevent compliance with the protocol. The remaining architectural changes appear consistent with established connection ownership. R1 and R2 block merge pending corrections and verification.

The review should identify what tests and CI checks actually ran, and what could not be verified. It should **not** change the MR's approval state or post comments unless explicitly authorized.

## Step 6: Re-review the updated MR

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

# Quick workflow reference

| Situation | Typical skill sequence | Your involvement |
|---|---|---|
| Large feature, rigid protocol | `brain-brainstorm` → `brain-write-spec` → optional `brain-plan-feature` / `brain-write-tickets` → `brain-blueprint` → `brain-implement` → `brain-review-code` | Approve architecture, spec, blueprint, and implementation increments. |
| Small, settled feature | `brain-implement` | Review the focused change and verification. |
| Isolated protocol bug | `brain-diagnose` → focused fix → optional `brain-review-code` | Review the diagnosis and correction. |
| Architecture cleanup | `brain-review-architecture` → `brain-brainstorm` → `brain-write-spec` → `brain-blueprint` → `brain-implement` → `brain-review-code` | Choose improvements and shape the exact design. |
| Third-party merge request | `brain-review-merge-request` (uses `brain-review-code`) | Evaluate findings and advisory merge recommendation. |

## How to communicate an intended design

When you already know how you want the code organized, tell Claude **before** blueprinting:

> I want `TcpSession` to own the connection and receive buffer. I want `WireCodec` to be stateless and handle serialization only. The dispatcher should operate on decoded message objects and have no access to socket internals. I want to review public interfaces, method responsibilities, and call flow before implementation. Challenge any part of this design that creates a concrete correctness or maintainability problem.

The most useful repeated pattern for design-sensitive work is:

**User-directed design → approved specification and blueprint → small testable increments → independent final review.**

For binary protocols, maintain an authoritative conformance suite with **literal golden byte vectors**. It gives implementers and reviewers an objective definition of correctness, independent of style or architectural preferences.
