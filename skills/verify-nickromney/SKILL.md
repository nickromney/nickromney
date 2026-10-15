---
name: verify-nickromney
description: Verify the public profile's local image, SVG, and GitHub repository references.
---

# Verify the nickromney profile

Run `make verify` from this repository to execute the same local check documented in
`AGENTS.md`: `uv run --locked python tools/check-profile.py`. The harness adds the explicit
local sibling-repository root and records the check's output.

The check reads `README.md`, local SVG assets, and sibling Git remotes. It does not fetch web
links or certify profile claims. The run creates HOME, uv cache, and an empty project environment
with syncing disabled under
`$VERIFY_BASE_DIR/$VERIFY_RUN_ID/state`, then removes that state during cleanup. Evidence stays
at `$VERIFY_EVIDENCE_ROOT/$VERIFY_RUN_ID/evidence`; it contains the command output and source
revision/status. Defaults are under `$TMPDIR/verify-kit/nickromney-profile` and
`$TMPDIR/verify-evidence/nickromney-profile`. Set `VERIFY_REPOS_ROOT` to use another sibling
checkout directory.

Use `make verify-dry-run` to preview the cycle and `make verify-test` for the shared Bash 3.2
contract suite. `make verify` reports `VERIFY PASS` only after the checker output confirms local
assets, parsed SVGs, and owned repository links.
