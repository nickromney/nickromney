#!/usr/bin/env bash
# shellcheck disable=SC2034 # VK_* settings are read by the sourced verify-lib.sh
set -euo pipefail

VK_SCRIPT="$0"
VK_APP="nickromney-profile"
VK_DESCRIPTION="Verify the profile assets, SVGs, and linked local repositories."
VK_DEFAULT_BASE_DIR="${TMPDIR:-/tmp}/verify-kit/nickromney-profile"
VK_DEFAULT_EVIDENCE_ROOT="${TMPDIR:-/tmp}/verify-evidence/nickromney-profile"
# shellcheck source=verify-lib.sh disable=SC1091
. "$(cd "$(dirname "$0")" && pwd)/verify-lib.sh"

vk_commands_help() {
  cat <<'HELP'
  launch                 create isolated run directories
  doctor                 check the profile inputs exist
  profile                run the documented profile checker and retain its output
  cleanup                remove this run's state; evidence is kept
HELP
}
vk_sample_commands() { printf '%s\n' verify launch doctor profile cleanup; }
vk_paths() {
  STATE="$VK_BASE_DIR/$VK_RUN_ID/state"
  EVIDENCE="$VK_EVIDENCE_ROOT/$VK_RUN_ID/evidence"
  REPOS_ROOT="${VERIFY_REPOS_ROOT:-$VK_ROOT/..}"
}
vk_plan() {
  case "$1" in
    verify) vk_plan_line "check profile inputs, run uv run --locked python tools/check-profile.py --repos-root '$REPOS_ROOT', assert its local verification result, remove state, keep evidence at $EVIDENCE" ;;
    launch) vk_plan_line "create isolated HOME, UV cache, and project environment under $STATE; prepare $EVIDENCE" ;;
    doctor) vk_plan_line "check README.md, tools/check-profile.py, and assets/profile-header.svg" ;;
    profile) vk_plan_line "run the repository's documented local profile checker; capture output in $EVIDENCE/profile-check.log" ;;
    cleanup) vk_plan_line "remove only $STATE and keep $EVIDENCE" ;;
    *) vk_unknown_command ;;
  esac
}
cmd_launch() {
  mkdir -p "$STATE/home" "$STATE/uv-cache" "$STATE/uv-env" "$EVIDENCE"
  vk_mark_current
  printf '%s\n' "$VK_RUN_ID" > "$STATE/run-id"
  vk_record_revision "$EVIDENCE/revision.txt"
  vk_say "ready run=$VK_RUN_ID state=$STATE evidence=$EVIDENCE"
}
cmd_doctor() {
  if [ ! -d "$STATE" ] || [ ! -f "$STATE/run-id" ] || [ "$(cat "$STATE/run-id")" != "$VK_RUN_ID" ]; then
    vk_fail "no isolated state for run $VK_RUN_ID; launch first"
    return 1
  fi
  if [ ! -f "$VK_ROOT/README.md" ] || [ ! -f "$VK_ROOT/tools/check-profile.py" ] || [ ! -f "$VK_ROOT/assets/profile-header.svg" ]; then
    vk_fail "profile checker input is missing"
    return 1
  fi
  vk_say "OK profile checker inputs exist"
}
cmd_profile() {
  local log="$EVIDENCE/profile-check.log"
  (
    cd "$VK_ROOT"
    HOME="$STATE/home" UV_CACHE_DIR="$STATE/uv-cache" \
      UV_PROJECT_ENVIRONMENT="$STATE/uv-env" UV_NO_SYNC=1 \
      uv run --locked python tools/check-profile.py --repos-root "$REPOS_ROOT"
  ) > "$log" 2>&1
  cat "$log"
}
cmd_cleanup() {
  rm -rf "${STATE:?}"
  rmdir "$VK_BASE_DIR/$VK_RUN_ID" 2>/dev/null || true
  vk_clear_current
  vk_say "removed state for run=$VK_RUN_ID; evidence kept at $EVIDENCE"
}
vk_verify_recipes() {
  cmd_profile
  vk_expect_contains "$EVIDENCE/profile-check.log" "Local profile assets verified:"
  vk_expect_contains "$EVIDENCE/profile-check.log" "owned repository links matched local remotes"
}
vk_dispatch() {
  local cmd="$1"; shift
  case "$cmd" in
    launch) cmd_launch ;;
    doctor) cmd_doctor ;;
    profile) cmd_profile ;;
    cleanup) cmd_cleanup ;;
    *) vk_unknown_command ;;
  esac
}
vk_main "$@"
