# God Code

God Code is a programming language that reads like scripture. Write real software in words of faith, in your own language, and watch it run. Human-readable, safe, and built for humans and AI creating together. Created in Botswana, open to the world.

When working with God Code scrolls (`.god` files), follow this workflow every time:

1. **Generate** the scroll. Everything must live between `BEGIN CREATION` and `END CREATION`.
2. **Check** it: `godcode check --json <file>`. Exit 0 is pure, 1 is diagnostics, 2 is a usage error. Fix every diagnostic using its `hint`.
3. **Run safely**: `godcode run --sandbox --json <file>`. Inspect `output`, `error`, `intents`, and `permissions`. Iterate until clean.

Never run a scroll you did not write without `--sandbox`.

Language essentials: `DECLARE x AS ...` assigns; `IS` / `IS NOT` compare; `REVEAL(expr)` prints; strings interpolate like `"grace upon {name}"`; blocks close explicitly (`ENDIF`, `ENDFOR`, `ENDWHILE`, `END RITE`); `IF` takes `THEN`; `FOR` walks a list or `RANGE(1, 4)`; rites are `DEFINE RITE name()` ... `END RITE` invoked with `INVOKE name()`; `DECLARE INTENT "words" ON rite_name` names a rite's purpose (drift counsels, never fails); `SEAL` writes a covenant block; `ANCHOR` returns a receipt map; `CONSULT("question")` asks the local oracle; `ASCEND` ends a run peacefully; `SHA256`, `HMAC`, `BASE64_ENCODE`, `BASE64_DECODE`, `REPEAT(s, n)`, and the commons (`TRIM`, `SORT`, `SUM_OF`, `FIRST`, `LAST`, `UNIQUE`, `INDEX_OF`, `KEYS`, `VALUES`, `HAS_KEY`, `MERGE`, `ABS`, `ROUND`, `SQRT`, `POW`) are pure and need no import.

Permission manifests go at the top inside `BEGIN CREATION`: `DECLARE PERMISSION TO READ "data/"`, `TO WRITE "out/"`, `TO SPEAK WITH "host"`, `TO ASK THE WORLD`, `TO SUMMON "verb"`. A rite reaching for an undeclared power is stopped. Read a foreign scroll's manifest with `godcode permissions --json <file>` before running it.

Tongues: `# tongue: tn` for Setswana keywords, `# tongue: zu` for isiZulu. English keywords still work.

Install the CLI with `pip install godcode-engine`. Full reference lives in the godcode skill pack under `skills/godcode/references/`.
