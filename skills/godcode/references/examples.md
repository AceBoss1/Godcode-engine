# Three runnable scrolls

Each one passes `godcode check --json` and runs under `godcode run --sandbox --json`. Copy one, change the words, make it yours.

## 1. A first blessing

The smallest complete scroll. Assignment, interpolation, output.

```godcode
BEGIN CREATION
  DECLARE name AS "world"
  REVEAL("Hello, {name}.")
  REVEAL("Grace upon grace, and peace upon this house.")
END CREATION
```

Run it:

```bash
godcode check --json hello.god
godcode run --sandbox --json hello.god
```

Expect `output` to hold:

```
Hello, world.
Grace upon grace, and peace upon this house.
```

## 2. A rite with declared intent, sealed

A rite that carries its purpose, invokes it, and seals the work. Watch `intents` in the JSON run output: the Spirit discerns whether the rite walked in its declared intent. Here it aligns, and the run carries the blessing.

```godcode
BEGIN CREATION
  DECLARE INTENT "bring peace to the household" ON morning_blessing

  DEFINE RITE morning_blessing()
    REVEAL("peace upon this house")
    REVEAL("peace upon the bread and the hands that made it")
    DECLARE loaves AS 2 * 5
    REVEAL("the oven holds {loaves} loaves")
  END RITE

  INVOKE morning_blessing()
  SEAL("the morning work is blessed")
END CREATION
```

Run it:

```bash
godcode check --json morning_blessing.god
godcode run --sandbox --json morning_blessing.god
```

Expect `output` to hold:

```
peace upon this house
peace upon the bread and the hands that made it
the oven holds 10 loaves
```

And `intents` to carry one entry for `morning_blessing` with its declared intent, the discerned intent ("Blessing of peace"), a confidence score, and `aligned: true`. If a rite ever drifts from its declared intent, the engine counsels gently. Drift can never fail a run.

## 3. A scroll that declares its permissions

The manifest sits at the top inside `BEGIN CREATION`. This scroll reads from `data/` and may ask the oracle. Anything else it reaches for is stopped.

```godcode
BEGIN CREATION
  DECLARE PERMISSION TO READ "data/"
  DECLARE PERMISSION TO ASK THE WORLD

  REVEAL("I read only what I declared, and nothing more.")
  DECLARE word AS CONSULT("what does a faithful steward do first?")
  REVEAL(word)
END CREATION
```

Run it:

```bash
godcode check --json faithful_steward.god
godcode run --sandbox --json faithful_steward.god
godcode permissions --json faithful_steward.god
```

The last command reads the manifest without running anything. Expect a manifest shaped like:

```json
{"read": ["<your-scroll-dir>/data"], "write": [], "network": [], "stdin": true, "summon": []}
```

(The `read` path is resolved against the scroll's own directory.)
