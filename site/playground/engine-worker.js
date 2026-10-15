/* ============================================================
   GOD CODE ENGINE WORKER. The real engine, in the browser.

   Loads Pyodide (Python compiled to WebAssembly), lays this repo's own
   `godcode` package into its filesystem from engine.json, and answers
   the playground page with godcode.webrun:

     page → worker  {id, kind:"run"|"check", source}
     worker → page  {type:"ready", version, samples}
                    {type:"result", id, kind, payload}   (the webrun dict)
                    {type:"failed", message}             (engine could not wake)

   Every run is sandboxed by the engine itself (strict policy: no files,
   no network, a wall-clock grant and a step budget). The page also
   holds a hard deadline and terminates this worker if a run outlives it.
   Rebuild engine.json with `python3 site/playground/build_engine.py`.
   ============================================================ */
"use strict";

const PYODIDE_VERSION = "0.26.4";
const PYODIDE_URL = "https://cdn.jsdelivr.net/pyodide/v" + PYODIDE_VERSION + "/full/";
const ENGINE_ROOT = "/engine";                 // godcode/ and the dataset rest here
const LIBRARY_DIR = "/home/pyodide/library";   // registry scrolls, by bare name

let engine = null;   // {run, check}: Python callables that answer JSON text

function writeTree(FS, root, files){
  for(const [path, text] of Object.entries(files)){
    const full = root + "/" + path;
    FS.mkdirTree(full.slice(0, full.lastIndexOf("/")));
    FS.writeFile(full, text, {encoding: "utf8"});
  }
}

// The Python side of the bridge: plain godcode.webrun, answered as JSON text.
const BRIDGE = `
import json, os, sys
sys.path.insert(0, ${JSON.stringify(ENGINE_ROOT)})
os.environ["GODCODE_NO_PLUGINS"] = "1"
from godcode import webrun

def _gc_run(source):
    return json.dumps(webrun.run_creation(source, library_dir=${JSON.stringify(LIBRARY_DIR)}),
                      ensure_ascii=False)

def _gc_check(source):
    return json.dumps(webrun.check_creation(source), ensure_ascii=False)
`;

const ready = (async () => {
  importScripts(PYODIDE_URL + "pyodide.js");
  const [pyodide, bundle] = await Promise.all([
    loadPyodide({indexURL: PYODIDE_URL}),
    fetch(new URL("engine.json", self.location.href)).then((r) => {
      if(!r.ok) throw new Error("engine.json answered " + r.status);
      return r.json();
    }),
  ]);
  writeTree(pyodide.FS, ENGINE_ROOT, bundle.files);
  writeTree(pyodide.FS, LIBRARY_DIR, bundle.library);
  pyodide.runPython(BRIDGE);
  engine = {run: pyodide.globals.get("_gc_run"), check: pyodide.globals.get("_gc_check")};
  return bundle;
})();

ready.then(
  (bundle) => postMessage({type: "ready", version: bundle.version, samples: bundle.samples}),
  (err) => postMessage({type: "failed", message: String((err && err.message) || err)})
);

self.onmessage = async (event) => {
  const {id, kind, source} = event.data || {};
  try{ await ready; }catch(_){ return; }      // "failed" was already posted
  let payload;
  try{
    payload = JSON.parse(kind === "check" ? engine.check(source) : engine.run(source));
  }catch(err){
    payload = {ok: false, output: [], diagnostics: [],
               error: {line: null, col: null, code: "HOST_ERROR",
                       message: "the engine faltered: " + String((err && err.message) || err),
                       hint: null, trace: []}};
  }
  postMessage({type: "result", id, kind, payload});
};
