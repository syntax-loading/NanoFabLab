// rec.mjs — deterministic clip recorder for lab3_process_flow.html
//
//   node rec.mjs --hash 13 --adv 13 --pre 2000 --dur 30000 --out D:/tmp/p0
//
// loads the deck at #<hash>, lets it settle for --pre ms, then starts a CDP
// screencast and immediately drives go(<adv>) once (adv=-1 to only watch).
// every screencast frame is written to <out>/f_00000.<fmt> and logged to
// <out>/capture.json with its real timestamp, so the assembly step can place
// frames on a CFR grid afterwards instead of hoping capture was exactly 30 fps.
//
// no npm dependencies: node 22+ has a global WebSocket, and fetch is built in.

import { spawn, spawnSync } from "node:child_process";
import { mkdirSync, writeFileSync, existsSync, rmSync } from "node:fs";
import { resolve, join } from "node:path";

const CHROME =
  process.env.CHROME ||
  "C:/Users/16329/AppData/Local/ms-playwright/chromium-1243/chrome-win64/chrome.exe";

function arg(name, def) {
  const i = process.argv.indexOf("--" + name);
  return i > 0 && i + 1 < process.argv.length ? process.argv[i + 1] : def;
}
const HASH = parseInt(arg("hash", "1"), 10);
const ADV = parseInt(arg("adv", "-1"), 10); // 1-based; -1 = don't advance
const PRE = parseInt(arg("pre", "2000"), 10);
const DUR = parseInt(arg("dur", "30000"), 10);
const OUT = resolve(arg("out", "clip"));
const FMT = arg("fmt", "png");
const W = parseInt(arg("w", "1600"), 10);
const H = parseInt(arg("h", "900"), 10);
const DSF = arg("dsf", "1.2");
const NODPR = process.argv.includes("--nodpr");
const PIN = process.argv.includes("--pin");
const APROBE = arg("aprobe", "");
const WIN = arg("win", W + "x" + H);
const DECK = resolve(arg("deck", "lab3_process_flow.html"));
const EXTRA = arg("q", ""); // extra query string, e.g. "notr=1"

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

if (existsSync(OUT)) rmSync(OUT, { recursive: true, force: true });
mkdirSync(OUT, { recursive: true });

const profile = join(OUT, "_profile");
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
    "--autoplay-policy=no-user-gesture-required",
    "--hide-scrollbars",
    "--mute-audio",
    "--window-size=" + WIN.replace("x", ","),
    ...(NODPR ? [] : ["--force-device-scale-factor=" + DSF]),
    "about:blank",
  ],
  { stdio: ["ignore", "pipe", "pipe"] }
);

let chromeErr = "";
chrome.stderr.on("data", (d) => {
  chromeErr += d.toString();
  const m = /DevTools listening on (ws:\/\/\S+)/.exec(chromeErr);
  if (m && !browserWs) start(m[1]);
});
chrome.stdout.on("data", () => {});

let browserWs = null;
let stage = "start";
const t_start = Date.now();
function T(s) {
  stage = s;
  console.error("[%5.1fs] %s", (Date.now() - t_start) / 1000, s);
}
// chrome.kill() only terminates the browser process on windows; renderers and
// utility children stay behind and keep the profile locked, so ask taskkill for
// the whole tree.
function killTree() {
  if (process.platform === "win32" && chrome && chrome.pid) {
    try {
      spawnSync("taskkill", ["/PID", String(chrome.pid), "/T", "/F"],
                { stdio: "ignore" });
    } catch (e) {}
  }
  try { chrome.kill(); } catch (e) {}
}
const WATCHDOG_S = parseInt(arg("watchdog", "240"), 10);
const WD = setTimeout(() => {
  T("WATCHDOG, stuck at: " + stage);
  killTree();
  process.exit(3);
}, WATCHDOG_S * 1000);

async function start(wsUrl) {
  browserWs = wsUrl;
  const port = new URL(wsUrl).port;
  try {
    await run(port);
  } catch (e) {
    console.error("FAIL", e);
    process.exit(1);
  }
}

function cdp(url) {
  const ws = new WebSocket(url);
  let id = 0;
  const pending = new Map();
  const handlers = new Map();
  const ready = new Promise((res, rej) => {
    ws.onopen = () => res();
    ws.onerror = (e) => rej(new Error("ws error"));
  });
  ws.onmessage = (ev) => {
    const m = JSON.parse(ev.data);
    if (m.id != null) {
      const p = pending.get(m.id);
      if (p) {
        pending.delete(m.id);
        m.error ? p.rej(new Error(m.method + " " + JSON.stringify(m.error))) : p.res(m.result);
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

async function run(port) {
  // find the page target
  T("chrome pid " + chrome.pid + ", polling /json/list");
  let list = [];
  for (let i = 0; i < 50; i++) {
    try {
      list = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
      if (list.some((t) => t.type === "page")) break;
    } catch (e) {}
    await sleep(100);
  }
  const page = list.find((t) => t.type === "page");
  if (!page) throw new Error("no page target");
  T("page target " + page.id.slice(0, 8) + " url=" + page.url);

  const c = cdp(page.webSocketDebuggerUrl);
  await c.ready;
  T("cdp ws open");
  await c.send("Page.enable");
  await c.send("Runtime.enable");
  T("domains enabled");
  // the window is not exactly --window-size in headless=new (it loses ~17 px to a
  // phantom scrollbar and some inset), so pin the CSS viewport by hand: the deck's
  // fit() then computes scale 1.0 and the backing store is exactly W*dsf by H*dsf.
  await c.send("Emulation.setDeviceMetricsOverride", {
    width: W,
    height: H,
    deviceScaleFactor: parseFloat(DSF),
    mobile: false,
  });

  const q = [];
  if (EXTRA) q.push(EXTRA);
  const url = "file:///" + DECK.replace(/\\/g, "/") + (q.length ? "?" + q.join("&") : "") + "#" + HASH;
  const loaded = new Promise((r) => c.on("Page.loadEventFired", r));
  T("navigating " + url);
  await c.send("Page.navigate", { url });
  await loaded;
  T("load event");
  if (PIN) {
    // the deck centres #stage with left:50% margin:-800px. at a fractional device
    // scale that lands on a half pixel and every glyph gets resampled, so pin the
    // stage to the viewport origin instead: with a 1600-wide viewport that is
    // device pixel 0 exactly. one leftover column is cropped at encode time.
    await c.send("Runtime.evaluate", {
      expression: `(function(){var s=document.getElementById("stage");
        s.style.left="0px";s.style.top="0px";s.style.margin="0";
        s.style.transform="none";return s.getBoundingClientRect().left+"x"+s.getBoundingClientRect().top;})()`,
      returnByValue: true,
    }).then((r) => console.log("pinned at", r.result.value));
  }
  await sleep(PRE);
  T("settled " + PRE + "ms");

  const probe = await c.send("Runtime.evaluate", {
    expression: `JSON.stringify({w:innerWidth,h:innerHeight,dpr:devicePixelRatio,
      scale:document.getElementById("stage").style.transform,
      cur:document.getElementById("cur")?document.getElementById("cur").textContent:"?"})`,
    returnByValue: true,
  });
  const info = JSON.parse(probe.result.value);
  console.log("probe", JSON.stringify(info));

  T("probe done: " + JSON.stringify(info));
  await c.send("Runtime.evaluate", {
    expression: `(function(){
      if (document.getElementById("__tick")) return;
      var st = document.createElement("style");
      st.textContent = "@keyframes __tickK{from{opacity:0.002}to{opacity:0.004}}" +
        "#__tick{position:fixed;left:0;top:0;width:1px;height:1px;background:#000;" +
        "opacity:.002;pointer-events:none;z-index:0;animation:__tickK .5s linear infinite alternate}";
      document.head.appendChild(st);
      var d = document.createElement("div"); d.id = "__tick";
      document.body.appendChild(d);})()`,
    returnByValue: true,
  });

  const frames = [];
  let idx = 0;
  c.on("Page.screencastFrame", (p) => {
    // keep the frames while the loop is running; ack immediately
    const t = p.metadata.timestamp * 1000; // s -> ms, epoch
    const name = "f_" + String(idx++).padStart(5, "0") + "." + FMT;
    writeFileSync(join(OUT, name), Buffer.from(p.data, "base64"));
    frames.push({
      file: name,
      t: t,
      w: p.metadata.deviceWidth,
      h: p.metadata.deviceHeight,
    });
    c.send("Page.screencastFrameAck", { sessionId: p.sessionId }).catch(() => {});
  });

  if (APROBE) {
    // does a file:// <audio> advance its own clock in headless, with no sound device?
    // the whole narration timing depends on the answer.
    const url = "file:///" + resolve(APROBE).replace(/\\/g, "/");
    const r = await c.send("Runtime.evaluate", {
      expression: `(function(){window.__au=new Audio(${JSON.stringify(url)});
        window.__au.currentTime=0; var p=window.__au.play();
        return "created"+(p?"":"")+"/"+(window.__au.readyState);})()`,
      returnByValue: true, awaitPromise: false,
    });
    console.log("audio", r.result.value, r.exceptionDetails ? r.exceptionDetails.text : "");
    for (let k = 1; k <= 6; k++) {
      await sleep(500);
      const q = await c.send("Runtime.evaluate", {
        expression: `JSON.stringify({ct:+(window.__au.currentTime||0).toFixed(3),dur:+(window.__au.duration||0).toFixed(2),rs:window.__au.readyState,paused:window.__au.paused})`,
        returnByValue: true,
      });
      console.log("audio sample", k * 500, q.result.value);
    }
  }

  const t0 = Date.now();
  T("starting screencast");
  await c.send("Page.startScreencast", {
    format: FMT,
    quality: FMT === "jpeg" ? 95 : 0,
    everyNthFrame: 1,
  });
  const capStart = Date.now();
  T("screencast on");
  // the deck's go()/next() live inside an IIFE, so there is no global handle to
  // call. its own keyboard bindings are the public interface: press ArrowRight.
  if (ADV > 0) {
    const cur = parseInt(
      (await c.send("Runtime.evaluate", {
        expression: `document.getElementById("cur").textContent`,
        returnByValue: true,
      })).result.value,
      10
    );
    for (let k = cur; k < ADV; k++) {
      await c.send("Runtime.evaluate", {
        expression: `document.dispatchEvent(new KeyboardEvent("keydown",
          {key:"ArrowRight",bubbles:true,cancelable:true}));`,
        returnByValue: true,
      });
      await sleep(40);
    }
    const now = (await c.send("Runtime.evaluate", {
      expression: `document.getElementById("cur").textContent`,
      returnByValue: true,
    })).result.value;
    console.log("advanced", cur, "->", now, "(wanted", ADV + ")");
    if (parseInt(now, 10) !== ADV) console.log("WARN advance failed");
  }
  await sleep(DUR);
  T("capture window over, " + frames.length + " frames");
  await c.send("Page.stopScreencast");
  T("stopped");

  // relative timing, and a short report
  const base = frames.length ? frames[0].t : 0;
  frames.forEach((f) => (f.ms = Math.round(f.t - base)));
  const span = frames.length ? frames[frames.length - 1].ms : 0;
  const fps = frames.length > 1 ? ((frames.length - 1) * 1000) / Math.max(1, span) : 0;
  const gaps = [];
  for (let i = 1; i < frames.length; i++) {
    const d = frames[i].ms - frames[i - 1].ms;
    if (d > 60) gaps.push({ at: frames[i].ms, dt: d });
  }
  const report = {
    deck: DECK,
    hash: HASH,
    adv: ADV,
    pre: PRE,
    dur: DUR,
    probe: info,
    frames: frames.length,
    spanMs: span,
    meanFps: +fps.toFixed(2),
    maxFramePx: frames.length ? [frames[0].w, frames[0].h] : null,
    bigGaps: gaps.slice(0, 20),
    bigGapCount: gaps.length,
    chromeMs: Date.now() - t_start,
    capStartDeltaMs: capStart - t0,
  };
  writeFileSync(join(OUT, "capture.json"), JSON.stringify({ report, frames }, null, 1));
  console.log(JSON.stringify(report, null, 1));

  c.close();
  clearTimeout(WD);
  killTree();
  process.exit(0);
}

setTimeout(() => {
  if (!browserWs) {
    console.error("no devtools url; stderr tail:\n" + chromeErr.slice(-2000));
    chrome.kill();
    process.exit(2);
  }
}, 15000);
