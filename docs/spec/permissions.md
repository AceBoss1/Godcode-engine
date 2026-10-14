# Permission manifests — the spec

*God Code spec layer: permissions. Companion to `sandbox.md`.*

## The rule

A scroll may declare what it is allowed to touch, at the top of the
scroll:

```
DECLARE PERMISSION TO READ "data/"
DECLARE PERMISSION TO WRITE "out/"
DECLARE PERMISSION TO SPEAK WITH "api.example.com"
DECLARE PERMISSION TO ASK THE WORLD
DECLARE PERMISSION TO SUMMON "reports.weekly"
```

The declaration is a promise and a boundary. Any rite that reaches for
a power the scroll did not declare is counselled and stopped. The
manifest never widens what the host allows: the effective grant is
always **host policy intersect manifest**. Deny by default; the host
may approve more, never less.

## The five powers

| Declaration | Grants | Policed rites |
|---|---|---|
| `READ "dir/"` | Read files under the directory (or the one file, if the path names a file) | `READ_FILE`, `LIST_DIR`, `FILE_EXISTS` |
| `WRITE "dir/"` | Write files under the directory | `WRITE_FILE` |
| `SPEAK WITH "host"` | Reach the host over the web (the host and its subdomains) | `HTTP_GET` |
| `ASK THE WORLD` | Speak with the outer world | `ASK` |
| `SUMMON "verb"` | Call upon the named plugin verb (and its namespaced children) | `SUMMON` |

## Static meaning

- `DECLARE PERMISSION TO` is a top-level decree. It is also gathered
  from inside top-level creation blocks. A decree anywhere else is
  ignored: manifests live at the top of the scroll.
- `PERMISSION`, `TO`, `READ`, `WRITE`, `SPEAK`, `WITH`, `ASK`, `THE`,
  `WORLD`, `SUMMON` are soft words: `DECLARE permission AS x` still
  declares an ordinary name.
- An unknown power is a parse-time counsel naming the five legal forms.

## Dynamic meaning

1. Before the run begins, the engine gathers every permission decree
   into the scroll's manifest. Relative path patterns resolve against
   the scroll's own directory.
2. If the scroll declared any permission, the guard is bound for the
   run — even under a plain `godcode run`, which otherwise runs
   unbound. The host policy for such a run is permissive; the manifest
   does the narrowing.
3. Every side-effecting rite is checked against the manifest before it
   runs. Path targets are resolved exactly the way the rite will open
   them (relative to the invocation directory), so the check can never
   bless a different file than the rite will touch.
4. Imported scrolls contribute their own manifests; grants compose by
   union. A library scroll that reads its data declares that read, and
   the run honors it.
5. A violation raises `SandboxViolation` with counsel naming the
   withheld power and the decree that would grant it.

## Machine interfaces

- `godcode permissions scroll.god [--json]` reads the manifest without
  running any code. Safe to call on untrusted scrolls.
- `godcode run --json` reports the run's manifest under `permissions`.
- The agent bridge offers a `permissions` tool with the same reading,
  and every `run` result carries the manifest.

## Honest limits

- The manifest polices the *invocation* of powers, not what trusted
  host code does after invocation: plugin verbs are host code and run
  outside the guard. Grant `SUMMON` only to verbs you trust.
- There is no approval hook yet: a denied power fails the run rather
  than asking the human. Interactive approval is the road ahead.
- The manifest does not police `IMPORT` paths; the host sandbox policy
  does (`--sandbox` confines imports to the stdlib and the scroll's
  own directory).
