# The God Code skill pack

God Code is a programming language that reads like scripture. Write real software in words of faith, in your own language, and watch it run. Human-readable, safe, and built for humans and AI creating together. Created in Botswana, open to the world.

This pack teaches your AI assistant to write, run, check, and debug God Code scrolls (`.god` files). One install, and Muse, Claude Code, Cursor, Codex, OpenCode, Gemini, Zed, or Copilot can generate God Code, validate it with `godcode check --json`, fix it from machine-readable diagnostics, and run it safely in the sandbox.

## Quick install

```bash
pip install godcode-engine      # the CLI, needed by every harness
./install.sh                    # detects your harnesses and installs the right adapter
```

Other shapes:

```bash
./install.sh --all                  # every adapter
./install.sh --harness cursor       # one harness: claude, claude-plugin, cursor, codex, universal
```

Then ask your assistant: "write a God Code scroll that blesses the morning bread." It will generate, check, fix, and run it.

## What is inside

- `skills/godcode/SKILL.md`: the core skill: what God Code is, the agent workflow (generate, check, fix, run in sandbox), permission manifests, language gotchas, and pointers to the references.
- `skills/godcode/references/cli.md`: the full CLI reference with JSON shapes.
- `skills/godcode/references/language.md`: language essentials with tiny examples.
- `skills/godcode/references/examples.md`: three complete runnable scrolls.
- `skills/godcode/references/troubleshooting.md`: error codes and the usual fixes.
- `plugin/.claude-plugin/plugin.json`: Claude Code plugin manifest (marketplace style install).
- `adapters/cursor/godcode.mdc`: Cursor rule, applies to `**/*.god` files.
- `adapters/codex/AGENTS.godcode.md`: drop-in section for `~/.codex/AGENTS.md`.
- `adapters/universal/GODCODE.md`: one page of rules for OpenCode, Gemini, Zed, Copilot, or any agent.

## Per-harness notes

**Muse** (`--harness claude`). The skill lands in `~/.claude/skills/godcode`. Muse picks it up on its own whenever you ask for God Code.

**Claude Code plugin** (`--harness claude-plugin`). Installs a plugin into `~/.claude/plugins/godcode`. Restart Claude Code to load it. Or add the marketplace straight from GitHub:

```
/plugin marketplace add godcodeengine/Godcode-engine
/plugin install godcode@godcode-marketplace
```

**Cursor** (`--harness cursor`). The rule lands in `~/.cursor/rules/godcode.mdc` and applies to every `.god` file. For one project only, copy it into that project's `.cursor/rules/` instead.

**Codex** (`--harness codex`). Appends the God Code section to `~/.codex/AGENTS.md`. Re-running the installer will not duplicate it.

**Anything else** (`--harness universal`). `GODCODE.md` lands in `~/.config/agents/`. Point your agent's instructions at it.

## The agent loop, in one breath

Generate, `godcode check --json`, fix from the hints, `godcode run --sandbox --json`, read the output. Never run a scroll you did not write without `--sandbox`. Scrolls should declare their permission manifest at the top. Drift from a declared intent gets gentle counsel, never a failed run.

The engine teaches as it corrects. Go and breathe worlds into being.
