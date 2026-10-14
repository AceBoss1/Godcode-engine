#!/usr/bin/env bash
# God Code skill pack installer.
# Copies the skill and the right adapter into each harness you use.
set -euo pipefail

PACK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MARKER="# >>> godcode-skill >>>"

say()  { printf '%s\n' "$1"; }
done_() { say "  installed: $1"; }

install_claude() {
  local dest="$HOME/.claude/skills/godcode"
  mkdir -p "$HOME/.claude/skills"
  rm -rf "$dest"
  cp -r "$PACK_DIR/skills/godcode" "$dest"
  done_ "Muse skill -> $dest"
}

install_claude_plugin() {
  local dest="$HOME/.claude/plugins/godcode"
  mkdir -p "$dest"
  rm -rf "$dest/.claude-plugin" "$dest/skills"
  cp -r "$PACK_DIR/plugin/.claude-plugin" "$dest/.claude-plugin"
  cp -r "$PACK_DIR/skills" "$dest/skills"
  done_ "Claude Code plugin -> $dest (restart Claude Code to load it)"
}

install_cursor() {
  local dest="$HOME/.cursor/rules"
  mkdir -p "$dest"
  cp "$PACK_DIR/adapters/cursor/godcode.mdc" "$dest/godcode.mdc"
  done_ "Cursor rule -> $dest/godcode.mdc (applies to **/*.god files)"
}

install_codex() {
  local dest="$HOME/.codex/AGENTS.md"
  mkdir -p "$HOME/.codex"
  if [ -f "$dest" ] && grep -qF "$MARKER" "$dest"; then
    say "  already present: Codex AGENTS.md (skipping)"
    return
  fi
  {
    echo ""
    echo "$MARKER"
    cat "$PACK_DIR/adapters/codex/AGENTS.godcode.md"
    echo "# <<< godcode-skill <<<"
  } >> "$dest"
  done_ "Codex section -> $dest"
}

install_universal() {
  local dest="$HOME/.config/agents"
  mkdir -p "$dest"
  cp "$PACK_DIR/adapters/universal/GODCODE.md" "$dest/GODCODE.md"
  done_ "Universal rules -> $dest/GODCODE.md (point OpenCode, Gemini, Zed, or Copilot at it)"
}

usage() {
  cat <<'EOF'
Usage: install.sh [--harness NAME] [--all]

Harnesses: claude, claude-plugin, cursor, codex, universal
With no flags, installs into every harness directory found on this machine.
EOF
}

HARNESS=""
DO_ALL=0
while [ $# -gt 0 ]; do
  case "$1" in
    --harness) HARNESS="${2:-}"; shift 2 ;;
    --all) DO_ALL=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) say "Unknown flag: $1"; usage; exit 2 ;;
  esac
done

run_one() {
  case "$1" in
    claude) install_claude ;;
    claude-plugin) install_claude_plugin ;;
    cursor) install_cursor ;;
    codex) install_codex ;;
    universal) install_universal ;;
    *) say "Unknown harness: $1"; usage; exit 2 ;;
  esac
}

if [ -n "$HARNESS" ]; then
  run_one "$HARNESS"
elif [ "$DO_ALL" -eq 1 ]; then
  for h in claude cursor codex universal; do run_one "$h"; done
else
  found=0
  [ -d "$HOME/.claude" ]  && { run_one claude; found=1; }
  [ -d "$HOME/.cursor" ]  && { run_one cursor; found=1; }
  [ -d "$HOME/.codex" ]   && { run_one codex;  found=1; }
  if [ "$found" -eq 0 ]; then
    say "No harness directories found. Installing the universal rules instead."
    run_one universal
  else
    say "Tip: ./install.sh --all installs every adapter, and --harness NAME picks one."
  fi
fi

say "Done. Your assistant can now write God Code."
say "Make sure the CLI is installed: pip install godcode-engine"
