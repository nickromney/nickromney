# nickromney agent guide

README.md is the public GitHub profile. Keep operational notes out of it.

## Verify

```sh
uv run --locked python tools/check-profile.py
```

This is the pre-push gate in `lefthook.yml` (`lefthook install` once to enable it).
Requires `uv`. It checks local image references and SVG well-formedness, and that
`github.com/nickromney/<repo>` links match sibling checkouts under
`~/Developer/personal` (override with `--repos-root`). It does not fetch external
links, so link destinations and profile claims remain unverified.

## Hazards

- Profile edits are public as soon as they are pushed.
- Credential and certification claims need evidence from their source.
- `assets/profile-header.svg` is the source for the header image.
