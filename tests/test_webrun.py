"""The web door: the real engine, as the browser playground runs it.

The playground at site/playground/ loads this repository's own engine
into the browser through Pyodide, from site/playground/engine.json, and
calls godcode.webrun. These tests keep that path honest: the bundle is
current with the engine, it boots on its own with nothing but its own
files, every bundled sample runs clean under the sandbox, and the
payloads the page reads keep their shape.
"""
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from godcode.webrun import CREATION_NAME, check_creation, run_creation

REPO = Path(__file__).resolve().parent.parent
PLAYGROUND = REPO / "site" / "playground"
BUNDLE = PLAYGROUND / "engine.json"


def _load_builder():
    spec = importlib.util.spec_from_file_location(
        "build_engine", PLAYGROUND / "build_engine.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def bundle():
    return json.loads(BUNDLE.read_text(encoding="utf-8"))


@pytest.fixture()
def library(tmp_path, bundle):
    """Lay the bundled registry scrolls out as the worker does."""
    lib = tmp_path / "library"
    lib.mkdir()
    for name, text in bundle["library"].items():
        (lib / name).write_text(text, encoding="utf-8")
    return lib


def _creation(*lines):
    return "BEGIN CREATION\n" + "".join(f"  {line}\n" for line in lines) + "END CREATION\n"


# ---------------------------------------------------------------- the bundle

def test_bundle_is_current_with_the_engine():
    """Change the engine, rebuild the bundle: the playground never drifts."""
    assert BUNDLE.read_text(encoding="utf-8") == _load_builder().build(), (
        "site/playground/engine.json is stale: run "
        "python3 site/playground/build_engine.py")


def test_bundle_carries_every_engine_module(bundle):
    package = REPO / "godcode"
    wanted = {p.relative_to(REPO).as_posix() for p in package.glob("*.py")}
    wanted |= {p.relative_to(REPO).as_posix() for p in (package / "scrolls").iterdir()
               if p.suffix in (".god", ".toml")}
    wanted.add("god_code_training_dataset.csv")
    assert set(bundle["files"]) == wanted


def test_bundle_version_matches_the_package(bundle):
    from godcode import __version__
    assert bundle["version"] == __version__


def test_bundle_boots_alone(tmp_path, bundle):
    """With only the bundled files on the path, the engine wakes and runs.

    This is the browser's situation: Pyodide has the standard library and
    whatever the worker writes from engine.json, nothing else. The run is
    isolated (-I) so the repository itself is never imported.
    """
    root = tmp_path / "engine"
    for path, text in bundle["files"].items():
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    lib = tmp_path / "library"
    lib.mkdir()
    for name, text in bundle["library"].items():
        (lib / name).write_text(text, encoding="utf-8")
    source = _creation(
        'IMPORT "blessings"',
        "REVEAL(BLESSING_COUNT() > 0)",
        'REVEAL(LEN(CONSULT("what next?")) > 0)',
        'REVEAL(TRIM("  amen  "))',
    )
    script = (
        "import json, sys\n"
        f"sys.path.insert(0, {str(root)!r})\n"
        "import godcode.webrun as w\n"
        "assert w.__file__.startswith(sys.path[0]), w.__file__\n"
        f"print(json.dumps(w.run_creation({source!r}, library_dir={str(lib)!r})))\n"
    )
    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    env["GODCODE_NO_PLUGINS"] = "1"
    done = subprocess.run([sys.executable, "-I", "-c", script], cwd=str(tmp_path),
                          env=env, capture_output=True, text=True, timeout=120)
    assert done.returncode == 0, done.stderr
    payload = json.loads(done.stdout.strip().splitlines()[-1])
    assert payload["ok"], payload["error"]
    assert payload["output"] == ["true", "true", "amen"]


def test_every_bundled_sample_runs_clean(bundle, library):
    assert bundle["samples"], "the playground offers no engine samples"
    for sample in bundle["samples"]:
        assert (REPO / "examples" / sample["file"]).is_file()
        payload = run_creation(sample["code"], library_dir=library)
        assert payload["ok"], (sample["file"], payload["error"])
        assert payload["output"], sample["file"]


# ---------------------------------------------------------------- run

def test_run_payload_shape():
    payload = run_creation(_creation('REVEAL("grace upon {1 + 2}")', "ASCEND"))
    assert payload["tool"] == "godcode"
    assert payload["command"] == "run"
    assert payload["file"] == CREATION_NAME
    assert payload["ok"] is True
    assert payload["error"] is None
    assert payload["output"] == ["grace upon 3", "🕊 Creation ascended in peace."]
    assert isinstance(payload["stats"]["ms"], int)
    json.dumps(payload)  # the page receives it as JSON


def test_run_error_keeps_earlier_output_and_trace():
    payload = run_creation(_creation(
        "DEFINE RITE HALVE(n)",
        "  RETURN n / 0",
        "END RITE",
        'REVEAL("before")',
        "REVEAL(HALVE(4))",
    ))
    assert payload["ok"] is False
    assert payload["output"] == ["before"]
    error = payload["error"]
    assert error["code"] == "RUNTIME_ERROR"
    assert error["line"] == 3
    assert error["hint"]
    assert error["trace"] == [{"rite": "HALVE", "line": 6}]


def test_run_is_sandboxed():
    payload = run_creation(_creation('REVEAL(FILE_EXISTS("/etc/passwd"))'))
    assert payload["ok"] is False
    assert "sandbox withholds" in payload["error"]["message"]


def test_run_step_budget_releases_an_endless_cycle():
    payload = run_creation(_creation("WHILE TRUE DO", "  DECLARE a AS 1", "ENDWHILE"),
                           max_steps=5_000)
    assert payload["ok"] is False
    assert "step budget is spent" in payload["error"]["message"]


def test_run_imports_registry_scrolls_from_the_library(library):
    payload = run_creation(_creation('IMPORT "blessings"', "REVEAL(BLESSING_COUNT() > 0)"),
                           library_dir=library)
    assert payload["ok"], payload["error"]
    assert payload["output"] == ["true"]


def test_run_refuses_imports_beyond_the_library(library, tmp_path):
    outside = tmp_path / "outside.god"
    outside.write_text(_creation('REVEAL("escaped")'), encoding="utf-8")
    payload = run_creation(_creation(f'IMPORT "{outside.as_posix()}"'), library_dir=library)
    assert payload["ok"] is False
    assert "outside the consecrated paths" in payload["error"]["message"]


def test_run_speaks_the_tongues():
    source = (REPO / "examples" / "first_blessing_zu.god").read_text(encoding="utf-8")
    payload = run_creation(source)
    assert payload["ok"], payload["error"]
    assert payload["output"][0] == "Sawubona, mngane wami."


# ---------------------------------------------------------------- check

def test_check_pure_creation():
    payload = check_creation(_creation("DECLARE x AS 1", "REVEAL(x)"))
    assert payload["command"] == "check"
    assert payload["ok"] is True
    assert payload["diagnostics"] == []


def test_check_parse_error_is_impure():
    payload = check_creation(_creation('REVEAL("hi"'))
    assert payload["ok"] is False
    [diag] = payload["diagnostics"]
    assert diag["severity"] == "error"
    assert diag["code"] == "PARSE_ERROR"
    assert diag["line"] == 2


def test_check_lint_counsel_is_a_warning():
    payload = check_creation(_creation("DECLARE unused AS 1", "REVEAL(ghost)"))
    assert payload["ok"] is True  # counsel never makes a creation impure
    codes = {(d["code"], d["severity"], d["line"]) for d in payload["diagnostics"]}
    assert codes == {("GC001", "warning", 2), ("GC002", "warning", 3)}


# ---------------------------------------------------------------- the page

def test_page_and_worker_are_wired():
    page = (PLAYGROUND / "index.html").read_text(encoding="utf-8")
    worker = (PLAYGROUND / "engine-worker.js").read_text(encoding="utf-8")
    assert 'new Worker("engine-worker.js")' in page
    assert 'id="engineBadge"' in page and 'id="diag"' in page
    assert '"engine.json"' in worker
    assert "webrun.run_creation" in worker and "webrun.check_creation" in worker
    # Pyodide is pinned to an exact version, never a floating tag.
    assert 'const PYODIDE_VERSION = "0.26.4";' in worker
    assert "cdn.jsdelivr.net/pyodide/v" in worker


def test_page_keeps_old_share_links_working():
    """Links already shared (and the demos page) use #c=<base64url>."""
    page = (PLAYGROUND / "index.html").read_text(encoding="utf-8")
    assert 'location.hash.indexOf("#c=")===0' in page
    assert '"#c="+b64urlEncode(editor.value)' in page


def test_page_keeps_the_lite_engine_for_offline_use():
    page = (PLAYGROUND / "index.html").read_text(encoding="utf-8")
    assert "class Interpreter{" in page
    assert "function runLite(source)" in page
