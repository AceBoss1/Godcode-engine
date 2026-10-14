# God Code CLI reference

Install once:

```bash
pip install godcode-engine
```

Prefer `--json` for every command. It composes with `check` and `run`, and most other commands accept it too.

## check

```bash
godcode check --json scroll.god
```

Validates without running. Exit 0 is pure, 1 is diagnostics, 2 is a usage error.

```json
{
  "tool": "godcode",
  "command": "check",
  "file": "scroll.god",
  "ok": true,
  "diagnostics": [
    {"line": 7, "col": 12, "code": "LEXER_ERROR", "severity": "error",
     "message": "Malformed number '1.' ...",
     "hint": "Scan the reported line ..."}
  ]
}
```

`line` and `col` are 1-based. `col` may be null. Fix every diagnostic before running.

## run

```bash
godcode run --sandbox --json scroll.god
```

Same exit-code convention.

```json
{
  "tool": "godcode",
  "command": "run",
  "file": "scroll.god",
  "ok": true,
  "output": ["grace upon Sarah", "[SEAL] Covenant sealed ..."],
  "seals": [{"block": 0, "hash": "2ca3fe14..."}],
  "error": null,
  "intents": [
    {"rite": "evening_blessing", "declared": "bring peace to the household",
     "discerned": "Blessing of peace", "confidence": 0.09, "aligned": true}
  ],
  "permissions": {"read": [], "write": [], "network": [], "stdin": false, "summon": []},
  "stats": {"ms": 177}
}
```

- `output` holds every revealed line, plus engine notices (`[SEAL]`, `[INTENT]`, `[WARNING]`). On a runtime error it holds the lines revealed *before* the error.
- `error` carries `line`, `col`, `code`, `message`, and a `trace` when the run fails.
- `seals` lists covenant blocks written by `SEAL`. Under `--sandbox` the ledger is confined, so `seals` stays empty. Run without `--sandbox` only on scrolls you trust.
- `intents` holds one entry per invoked rite carrying `DECLARE INTENT`.
- `permissions` reports the run's permission manifest.

## new

```bash
godcode new my-scroll        # raises main.god, test_main.god, scroll.toml, README.md
godcode new my-scroll --json # machine-readable scaffold
```

## scroll (the registry)

```bash
godcode scroll list          # scrolls available in the registry
godcode scroll install <name>
godcode scroll publish <path>
godcode scroll info <name>
```

Add `--json` for machine-readable answers.

## fmt

```bash
godcode fmt scroll.god             # print the canonical rendering
godcode fmt --in-place scroll.god  # rewrite the file (renders canonical English)
```

## test

A test scroll is any `.god` file named `test_*.god` or `*_test.god`. Every rite named `TEST_*` is one test case. `TESTIFY` is the assertion: a testimony that holds passes, one that fails halts that test.

```bash
godcode test            # run the test scrolls in the current project
godcode test --json     # machine-readable results
```

## ledger

```bash
godcode ledger verify            # attest the covenant chain AND the anchor chain
```

## intent

```bash
godcode intent "words..."        # resolve the intent behind words through the Spirit engine
```

## permissions

```bash
godcode permissions scroll.god          # read the manifest without running anything
godcode permissions --json scroll.god   # {"read": [...], "write": [...], "network": [...], "stdin": bool, "summon": [...]}
```

## tools and bridge (the agent tool bridge)

Seven MCP-compatible tool schemas for agent frameworks:

```bash
godcode tools --json   # check, run, consult, intent, anchor_verify, ledger_verify, permissions
godcode bridge         # serve the tools as JSON-RPC 2.0 over stdio (initialize, ping, tools/list, tools/call)
```

## repl and lsp

```bash
godcode repl    # the interactive sanctuary
godcode lsp     # language server over stdio (hover, completion, live diagnostics)
```

## Golden rules

- Validate first, always. `check --json` before `run`.
- `--sandbox` for anything you did not write yourself.
- Read the hint. Every diagnostic teaches the fix.
