# nickromney: agent operating model

Adopted 6 October 2026 from local source and command inspection.
GitHub profile README and branded header

## Read by intent

Start with the local agent guide and build manifest. For domain or behavior
changes, follow the owners below, then the relevant contract/test. These
documents retain product detail and historical evidence:

- [README.md](../README.md)

## System ownership

| Owner | Responsibility |
| --- | --- |
| [README.md](../README.md) | Public profile narrative |
| [assets/profile-header.svg](../assets/profile-header.svg) | Profile visual |

Intent selects the owning policy; that policy produces decisions or artifacts;
adapters perform effects; verification establishes the result. Change the
owner once and keep alternate surfaces on that same contract.

## Invariants

- Profile edits become public when pushed.
- credentials/certification claims need owner evidence.
- static SVG is source.

## Existing action interfaces

These are inspected command surfaces, not a report that they ran. Read current
help and recipes for arguments, dependencies and lifecycle hooks before use.
Examples containing placeholder paths or bracketed options are grammar.

| Command | Effects and evidence |
| --- | --- |
| `git diff --check` | Read-only whitespace check; no software build. |

## Observe, verify and retain

Establish source revision, dirty state and relevant input identity before
choosing an action. Keep intended settings, cached artifacts and observed
runtime state distinct. An existing artifact is not a freshness or readiness
claim. Use the smallest deterministic fixture at the changed seam first;
expand to process, browser, device or deployment checks only when that
claim needs them. Record unavailable evidence explicitly.

Retain the command/configuration, source and input identity, result, limitation
and next discriminating check. Reuse evidence only while its relevant inputs
remain applicable. Promote a reproducible failure to a regression fixture,
a design decision to its owning document, and a repeated operator correction
to one concise guide rule. Keep private observations in private artifacts.

## Implemented plan for this pass

- [x] Map current source ownership and existing interfaces.
- [x] Make command effects and evidence limits discoverable.
- [x] Route agent work here and retain detailed product plans at their owners.

Acceptance: owner paths and document links resolve; current instructions
match inspected source; catalog hashes bind this context to the reviewed
bytes. This is documentation/control navigation acceptance. Product runtime
checks retain their own scope and are not certified by this pass.

## Selected workflow acceptance

The scoped recipe below is implemented and its relevant synthetic/local gate has been run. The owning README or product document records the command and effect boundary. This acceptance does not certify deployment, personal accounts or private inputs:

Verify local profile asset references and record dated external-link review scope; acceptance: README stays clean public prose with no internal operational instructions.

## Profile acceptance receipt

Run `python3 tools/check-profile.py` to validate local rendered-image references without fetching profile destinations. On 6 October 2026 the external links were reviewed as authored destinations only; their live behavior and certification claims were not certified. README.md remains the public product, and operating guidance stays here/AGENTS.md.
