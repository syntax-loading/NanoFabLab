// mk_pdf.mjs — print every beat of lab3_process_flow.html as one 16:9 PDF page.
//
//   node mk_pdf.mjs                                  # all 19 -> lab3_process_flow.pdf
//   node mk_pdf.mjs --pages 1,16 --out /tmp/t.pdf     # a subset, for checking
//
// Why this is not `--print-to-pdf`: the deck animates. ?instant=1 snaps CSS
// keyframes to their 0 % state (the keyframes do the "before -> after" work, so
// no animation = the before state), and headless virtual time does not advance
// the compositor clock, so --virtual-time-budget leaves a half-revealed page.
// The only honest way to a finished page is to let the beat run for its own
// dwell time and then print. 19 pages x dwell = about 4.5 minutes.
//
// no npm dependencies: node 22+ has a global WebSocket and fetch.

import { spawn, spawnSync } from "node:child_process";
import { mkdirSync, readFileSync, writeFileSync, existsSync, rmSync } from "node:fs";
import { resolve, join } from "node:path";

const CHROME =
  process.env.CHROME ||
  "C:/Users/16329/AppData/Local/ms-playwright/chromium-1243/chrome-win64/chrome.exe";
const PDFUNITE =
  process.env.PDFUNITE || "C:/texlive/2024/bin/windows/pdfunite.exe";

const W = 1600;
const H = 900;

function arg(name, def) {
  const i = process.argv.indexOf("--" + name);
  return i > 0 && i + 1 < process.argv.length ? process.argv[i + 1] : def;
}
const DECK = resolve(arg("deck", "lab3_process_flow.html"));
const OUT = resolve(arg("out", "lab3_process_flow.pdf"));
const PARTS = resolve(arg("parts", "_shot/pdf"));
const SLACK = parseInt(arg("slack", "2500"), 10);
const ONLY = arg("pages", "")
  .split(",")
  .filter(Boolean)
  .map(Number);

// dwell per beat in seconds — CAM[].d in the deck. A beat is "finished" when its
// own dwell has run out, which is exactly the moment the presenter presses ->.
const DWELL = [5, 9, 30, 30, 50, 15.4, 15.4, 9, 8, 9, 8, 9, 10, 6, 10, 11, 9, 10, 10];
if (DWELL.length !== 19) throw new Error("dwell table does not match the 19 beats");

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

mkdirSync(PARTS, { recursive: true });

const profile = join(PARTS, "_profile");
if (existsSync(profile)) rmSync(profile, { recursive: true, force: true });

const t_start = Date.now();
const T = (s) => console.error("[%5.1fs] %s", (Date.now() - t_start) / 1000, s);

const chrome = spawn(
  CHROME,
  [
    "--headless=new",
    "--remote-debugging-port=0",
    "--user-data-dir=" + profile,
    "--no-first-run",
    "--no-default-browser-check",
    "--disable-extensions",
    "--disable-background-timer-throttling",
    "--disable-backgrounding-occluded-windows",
    "--disable-renderer-backgrounding",
    "--disable-features=CalculateNativeWinOcclusion",
    "--hide-scrollbars",
    "--mute-audio",
    "--window-size=" + W + "," + H,
    "--force-device-scale-factor=1",
    "about:blank",
  ],
  { stdio: ["ignore", "pipe", "pipe"] }
);

let chromeErr = "";
chrome.stdout.on("data", () => {});
chrome.stderr.on("data", (d) => {
  chromeErr += d.toString();
  const m = /DevTools listening on (ws:\/\/\S+)/.exec(chromeErr);
  if (m && !browserWs) start(m[1]);
});

let browserWs = null;
function killTree() {
  if (process.platform === "win32" && chrome.pid) {
    try {
      spawnSync("taskkill", ["/PID", String(chrome.pid), "/T", "/F"], { stdio: "ignore" });
    } catch (e) {}
  }
  try { chrome.kill(); } catch (e) {}
}
const WD = setTimeout(() => {
  console.error("WATCHDOG");
  killTree();
  process.exit(3);
}, 15 * 60 * 1000);

function cdp(url) {
  const ws = new WebSocket(url);
  let id = 0;
  const pending = new Map();
  const handlers = new Map();
  const ready = new Promise((res, rej) => {
    ws.onopen = () => res();
    ws.onerror = () => rej(new Error("ws error"));
  });
  ws.onmessage = (ev) => {
    const m = JSON.parse(ev.data);
    if (m.id != null) {
      const p = pending.get(m.id);
      if (p) {
        pending.delete(m.id);
        m.error ? p.rej(new Error(JSON.stringify(m.error))) : p.res(m.result);
      }
    } else {
      (handlers.get(m.method) || []).forEach((f) => f(m.params));
    }
  };
  return {
    ready,
    send(method, params = {}) {
      const i = ++id;
      return new Promise((res, rej) => {
        pending.set(i, { res, rej });
        ws.send(JSON.stringify({ id: i, method, params }));
      });
    },
    on(method, fn) {
      if (!handlers.has(method)) handlers.set(method, []);
      handlers.get(method).push(fn);
    },
    close: () => ws.close(),
  };
}

async function start(wsUrl) {
  browserWs = wsUrl;
  try {
    await run(new URL(wsUrl).port);
  } catch (e) {
    console.error("FAIL", e);
    killTree();
    process.exit(1);
  }
}

async function run(port) {
  let list = [];
  for (let i = 0; i < 60; i++) {
    try {
      list = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
      if (list.some((t) => t.type === "page")) break;
    } catch (e) {}
    await sleep(100);
  }
  const page = list.find((t) => t.type === "page");
  if (!page) throw new Error("no page target");

  const c = cdp(page.webSocketDebuggerUrl);
  await c.ready;
  await c.send("Page.enable");
  await c.send("Runtime.enable");
  // pin the CSS viewport: the deck's fit() then computes scale 1 and nothing in
  // the rendered page depends on the real window size
  await c.send("Emulation.setDeviceMetricsOverride", {
    width: W,
    height: H,
    deviceScaleFactor: 1,
    mobile: false,
  });

  const pages = ONLY.length ? ONLY : Array.from({ length: DWELL.length }, (_, i) => i + 1);
  const files = [];

  for (const n of pages) {
    // the query is only there to bust the URL: navigating #1 -> #16 alone is a
    // same-document hash change, so no load event fires and the page is never
    // rebuilt. the deck ignores unknown search keys.
    const url =
      "file:///" + encodeURI(DECK.replace(/\\/g, "/")) + "?shot=" + n + "#" + n;
    const loaded = new Promise((r) => c.on("Page.loadEventFired", r));
    T(`page ${n}: navigate`);
    await c.send("Page.navigate", { url });
    await Promise.race([loaded, sleep(15000)]);
    // left:50%/margin:-800px lands on a half pixel in print layout; pin the stage
    // to the page origin so one CSS pixel is one page pixel
    await c.send("Runtime.evaluate", {
      expression: `(function(){var s=document.getElementById("stage");
        s.style.left="0px";s.style.top="0px";s.style.margin="0";s.style.transform="none";
        return 1;})()`,
      returnByValue: true,
    });

    const wait = Math.round(DWELL[n - 1] * 1000) + SLACK;
    await sleep(wait);

    const probe = await c.send("Runtime.evaluate", {
      expression: `JSON.stringify({cur:(document.getElementById("cur")||{}).textContent,
        t1:getComputedStyle(document.getElementById("t1")).opacity,
        note:getComputedStyle(document.getElementById("note")).opacity,
        beat:document.getElementById("stage").getAttribute("data-beat")})`,
      returnByValue: true,
    });
    const info = JSON.parse(probe.result.value);
    T(`page ${n}: settled ${wait}ms  cur=${info.cur} beat=${info.beat} t1=${info.t1} note=${info.note}`);
    if (parseInt(info.cur, 10) !== n) console.error(`  WARN wanted page ${n}, deck is on ${info.cur}`);
    if (info.t1 !== "1") console.error(`  WARN title opacity is ${info.t1}, not 1`);

    const pdf = await c.send("Page.printToPDF", {
      printBackground: true,
      paperWidth: W / 96,
      paperHeight: H / 96,
      marginTop: 0,
      marginBottom: 0,
      marginLeft: 0,
      marginRight: 0,
      preferCSSPageSize: true,
      scale: 1,
      displayHeaderFooter: false,
      transferMode: "ReturnAsBase64",
    });
    const file = join(PARTS, "p" + String(n).padStart(2, "0") + ".pdf");
    writeFileSync(file, Buffer.from(pdf.data, "base64"));
    files.push(file);
    T(`page ${n}: wrote ${file}`);
  }

  c.close();
  clearTimeout(WD);
  killTree();

  if (files.length === 1) {
    writeFileSync(OUT, readFileSync(files[0]));
    T("one page: copied to " + OUT);
  } else {
    const r = spawnSync(PDFUNITE, [...files, OUT], { encoding: "utf8" });
    if (r.status !== 0) throw new Error("pdfunite failed: " + (r.stderr || r.error));
    T("joined " + files.length + " pages -> " + OUT);
  }
  fixPageBox(OUT, files.length);
  process.exit(0);
}

// Chrome answers "one 900 px page" with a 675.12 pt box while its canvas is only
// 900.00 px tall, so every page rasterises with a white hairline along the bottom
// edge. Rewrite the page boxes to the exact 675.00 pt AFTER the join: the new
// string has the same byte length, so the xref offsets stay valid and no PDF
// library is needed.
function fixPageBox(file, pages) {
  const heightPt = (H * 72) / 96;
  const s = readFileSync(file).toString("latin1");
  let n = 0;
  const out = s.replace(
    /\/(MediaBox|TrimBox) \[0 0 (\d+(?:\.\d+)?) (\d+(?:\.\d+)?)( ?)\]/g,
    (m, kind, w, h, sep) => {
      const dec = h.includes(".") ? h.length - h.indexOf(".") - 1 : 0;
      const want = heightPt.toFixed(dec);
      if (want.length !== h.length) return m; // cannot patch without moving bytes
      if (want === h) return m;
      n++;
      return `/${kind} [0 0 ${w} ${want}${sep}]`;
    }
  );
  if (!n) {
    console.error("WARN no page box needed patching in " + file);
    return;
  }
  if (n < pages) console.error(`WARN patched ${n} page boxes for ${pages} pages`);
  writeFileSync(file, out, "latin1");
  T(`page boxes: ${n} patched to ${heightPt} pt`);
}

setTimeout(() => {
  if (!browserWs) {
    console.error("no devtools url; stderr tail:\n" + chromeErr.slice(-2000));
    killTree();
    process.exit(2);
  }
}, 20000);
