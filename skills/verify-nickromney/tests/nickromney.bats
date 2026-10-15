#!/usr/bin/env bats

setup() {
  SKILL_DIR="$(cd "$BATS_TEST_DIRNAME/.." && pwd)"
  SCRIPT="$SKILL_DIR/scripts/control.sh"
  export VERIFY_BASE_DIR="$BATS_TEST_TMPDIR/base"
  export VERIFY_EVIDENCE_ROOT="$BATS_TEST_TMPDIR/evidence"
  export VERIFY_RUN_ID="profile-run"
  BIN="$BATS_TEST_TMPDIR/bin"
  mkdir -p "$BIN"
  UV="$BIN/uv-real"
  cat > "$UV" <<'SH'
#!/bin/sh
echo "fake uv reached with HOME=$HOME"
echo "profile failure detail"
exit 37
SH
  chmod +x "$UV"
  cat > "$BIN/mise" <<'SH'
#!/bin/sh
[ "$1" = which ] && [ "$2" = uv ] || exit 2
printf '%s\n' "$TEST_UV_PATH"
SH
  chmod +x "$BIN/mise"
  export TEST_UV_PATH="$UV"
  export PATH="$BIN:/usr/bin:/bin"
}

@test "profile resolves uv through mise and prints failed check log" {
  run /bin/bash "$SCRIPT" --execute launch
  [ "$status" -eq 0 ]
  run /bin/bash "$SCRIPT" --execute profile
  [ "$status" -eq 37 ]
  [[ "$output" == *"fake uv reached with HOME=$VERIFY_BASE_DIR/$VERIFY_RUN_ID/state/home"* ]]
  [[ "$output" == *"profile failure detail"* ]]
  [ "$(cat "$VERIFY_EVIDENCE_ROOT/$VERIFY_RUN_ID/evidence/profile-check.log")" = $'fake uv reached with HOME='"$VERIFY_BASE_DIR/$VERIFY_RUN_ID/state/home"$'\nprofile failure detail' ]
}
