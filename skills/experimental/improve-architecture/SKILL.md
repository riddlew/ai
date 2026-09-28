---
name: improve-architecture
description: Explore a codebase for evidence-backed architectural improvement opportunities and present the strongest hypotheses for focused review.
---

# Improve Architecture

Use this skill when the user wants to improve a codebase's architecture but has not already selected one specific architectural decision for focused review.

The user may provide a subsystem, module, pain point, or other search direction.

This skill discovers architectural improvement opportunities. It does not implement them or perform detailed architectural design.

## Build an architectural picture

Begin by understanding the repository's current architectural shape.

Inspect enough of the codebase to identify:

- major modules or subsystems;
- important dependency boundaries;
- domain or context boundaries;
- where significant responsibilities appear to live;
- relevant tests and integration surfaces.

If the user provides an area of interest, center the investigation there while still reading enough surrounding structure to understand its architectural role.

Before proposing changes, read the domain records: root `CONTEXT-MAP.md` and the relevant contexts' `CONTEXT.md` (otherwise root `CONTEXT.md`), and relevant ADRs in root `docs/adr/` and each relevant context's `docs/adr/`.

Use the project's established domain language when describing the architecture.

Treat existing ADRs as intentional constraints. Reconsider one only when current repository evidence gives a substantive reason to question whether the recorded decision still serves the system.

## Find change-risk areas

From the architectural picture, identify areas where the current structure appears likely to make ordinary development unnecessarily costly or error-prone.

Prioritize areas where changes repeatedly require coordination across boundaries or where ownership is difficult to determine.

Possible evidence sources include:

- implementation structure;
- dependency relationships;
- tests;
- repeated patterns of cross-module editing;
- recent version-control history;
- recurring fixes or rework;
- duplicated coordination logic;
- comments or documentation describing known friction.

Version-control history is one source of evidence, not the default discovery mechanism.

If the initial investigation does not reveal meaningful architectural friction, expand into other structurally important parts of the repository.

## Examine architectural friction

Organize findings around the kind of development problem they create rather than around a generic architecture checklist.

### Change propagation

Look for changes whose impact spreads farther than the underlying behavior appears to justify.

Examples include:

- one domain change requiring edits across many unrelated modules;
- repeated synchronized changes between areas that are nominally independent;
- small behavioral changes requiring broad integration work.

### Ownership ambiguity

Look for concepts or behaviors without a clear architectural owner.

Signals may include:

- the same responsibility appearing in several modules;
- callers needing knowledge that should belong behind another boundary;
- neighboring components making competing decisions about the same concept;
- domain responsibilities that do not align with existing module boundaries.

### Coordination overhead

Look for structures that require excessive sequencing or indirection to perform conceptually simple work.

Examples include:

- behavior passing through several coordination layers without distinct responsibilities;
- multiple abstractions that must be understood together to change one concept;
- duplicated orchestration spread across callers.

### Dependency direction

Look for dependencies that undermine intended boundaries.

Examples include:

- lower-level concepts depending on application-specific policy;
- domain code depending unnecessarily on delivery or infrastructure concerns;
- nominally independent architectural areas reaching into each other's internals;
- cycles or reciprocal dependencies that make isolated change difficult.

### Test friction

Look for architecture that obscures the behavior that actually needs verification.

Examples include:

- important behavior only testable through large unrelated surfaces;
- interfaces exposing implementation seams rather than meaningful behavior;
- test-only abstractions increasing indirection without creating a useful boundary;
- responsibilities distributed so broadly that meaningful tests require excessive setup.

These are investigation signals, not automatic defects.

## Validate a hypothesis

Before presenting an architectural issue as a candidate, evaluate it independently through four lenses.

### Ownership clarity

Would the proposed direction make responsibility for the affected behavior easier to identify and maintain?

### Change radius

Would likely future changes touch fewer unrelated architectural areas, or make the affected set more predictable?

### Coupling

Would the direction reduce unnecessary knowledge or coordination between components without hiding necessary dependencies?

### Test observability

Would important behavior become easier to verify through meaningful interfaces or boundaries?

A proposal does not need to improve every dimension.

Reject or qualify a hypothesis when improvement in one dimension simply creates equivalent or worse problems elsewhere.

Prefer hypotheses supported by present repository behavior and actual development friction.

Do not propose architectural work solely for hypothetical scale, speculative reuse, theoretical cleanliness, or stylistic preference.

## Use parallel exploration selectively

When the repository is large, independent areas may be explored concurrently to reduce investigation cost.

Treat parallel or background exploration only as an execution optimization.

Each delegated investigation should have a bounded scope and return concrete repository evidence. The architectural method and candidate evaluation remain the same regardless of whether exploration is performed directly or in parallel.

## Form architectural hypotheses

Turn observed friction into a hypothesis only when there is enough evidence to explain:

1. what architectural property appears to be causing difficulty;
2. how that property manifests in current development;
3. what broad direction might reduce the problem.

Keep the proposed direction architectural and intentionally incomplete.

Do not design detailed interfaces, schemas, class structures, or APIs during discovery.

If a hypothesis conflicts with an ADR, describe the conflict only when current evidence provides a substantive reason to revisit the recorded decision.

## Present the discovery report

Produce a temporary Markdown report containing the strongest architectural hypotheses.

For each hypothesis include:

### Hypothesis

State the architectural problem being proposed for deeper investigation.

### Evidence

Describe the concrete repository evidence supporting it.

Distinguish direct observations from inference.

Where useful, identify the kind of evidence involved, such as:

- current structure;
- dependency analysis;
- tests;
- repeated change patterns;
- version-control history.

State material uncertainty explicitly.

### Affected decisions and boundaries

Identify the responsibilities, modules, domain boundaries, dependency rules, or existing architectural decisions implicated by the hypothesis.

### Potential direction

Describe the broad architectural direction that may address the problem without designing the final interface or implementation.

### Expected architectural effect

Explain the likely effect on:

- ownership clarity;
- change radius;
- coupling;
- test observability.

### Risks

Identify important costs, regressions, migrations, or new coupling the direction might introduce.

### Questions to validate

List the unresolved questions that a focused architectural review would need to answer before the direction should be adopted.

Use visual structure when it materially improves understanding.

Tables, dependency sketches, Mermaid diagrams, boundary diagrams, or other compact representations are appropriate when they clarify the evidence or architectural relationship. Do not force a before/after diagram onto every hypothesis.

## Present choices without prescribing one

Present only hypotheses with enough evidence to justify further consideration.

Do not manufacture additional candidates for variety.

Do not rank the candidates or prescribe one as the mandatory next choice.

If the user provides a criterion such as highest maintenance cost, widest architectural impact, lowest migration risk, or most frequent source of defects, use that criterion to organize or compare the candidates.

Otherwise present the evidence and trade-offs so the user can choose which hypothesis, if any, deserves deeper investigation.

## Handoff

After the user selects a hypothesis, invoke `review-architecture` with:

- the selected hypothesis;
- the supporting evidence;
- relevant architectural boundaries;
- applicable ADRs and domain terminology;
- known risks and unresolved questions.

Let `review-architecture` own deeper validation, constraint discovery, architectural trade-off analysis, and any subsequent design work.

Do not implement the selected direction automatically.