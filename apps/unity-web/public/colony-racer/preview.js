(() => {
  "use strict";
  const $ = id => document.getElementById(id);
  const canvas = $("unity-canvas");
  const panel = $("start-panel");
  const start = $("start");
  const heldButtons = Array.from(document.querySelectorAll("[data-held]"));
  const pointers = new Map();
  const keys = new Set();
  const lookPointers = new Map();
  const steeringPad = $("steering-pad");
  const steeringKnob = $("steering-knob");
  let steeringPointer = null, steeringAxis = 0;
  const keyActions = new Map([
    ["KeyW", "throttle"], ["ArrowUp", "throttle"], ["KeyS", "brake"], ["ArrowDown", "brake"], ["Space", "brake"],
    ["KeyA", "left"], ["ArrowLeft", "left"], ["KeyD", "right"], ["ArrowRight", "right"],
    ["KeyQ", "look-left"], ["KeyE", "look-right"], ["PageUp", "look-up"], ["PageDown", "look-down"]
  ]);
  const commandKeys = new Set(["KeyR", "KeyP", "Escape", "F1", "F2", "F3"]);
  const touchLayout = window.matchMedia("(pointer: coarse)").matches;
  let unity = null, ready = false, paused = true, detailed = !touchLayout, lastControls = "", statusTimer = 0;
  let latestTelemetry = null, telemetryReceivedAt = 0, loadError = null;

  function send(method, payload) {
    if (!unity || !ready) return false;
    if (payload === undefined) unity.SendMessage("ColonyRacerWebPreviewBridge", method);
    else unity.SendMessage("ColonyRacerWebPreviewBridge", method, payload);
    return true;
  }

  function controls() {
    const actions = new Set([...pointers.values(), ...Array.from(keys, key => keyActions.get(key))]);
    let lookX = (actions.has("look-right") ? .85 : 0) - (actions.has("look-left") ? .85 : 0);
    let lookY = (actions.has("look-up") ? .65 : 0) - (actions.has("look-down") ? .65 : 0);
    for (const look of lookPointers.values()) {
      lookX += Math.max(-1, Math.min(1, (look.x - look.startX) / 90));
      lookY -= Math.max(-1, Math.min(1, (look.y - look.startY) / 90));
    }
    return {
      throttle: !paused && actions.has("throttle") && !actions.has("brake") ? 1 : 0,
      brake: paused || actions.has("brake") ? 1 : 0,
      // The existing Gamepad stick processor supplies the deadzone once, inside Unity.
      steer: paused ? 0 : Math.max(-1, Math.min(1, steeringAxis + (actions.has("right") ? 1 : 0) - (actions.has("left") ? 1 : 0))),
      lookX: paused ? 0 : Math.max(-1, Math.min(1, lookX)),
      lookY: paused ? 0 : Math.max(-1, Math.min(1, lookY))
    };
  }

  function flush(force = false) {
    const data = JSON.stringify(controls());
    if (force || data !== lastControls) {
      lastControls = data;
      send("SetControls", data);
    }
    const actions = new Set([...pointers.values(), ...Array.from(keys, key => keyActions.get(key))]);
    heldButtons.forEach(button => button.classList.toggle("held", !paused && actions.has(button.dataset.held)));
  }

  function releaseAll() {
    pointers.clear(); keys.clear(); lookPointers.clear();
    releaseSteering();
    // Clearing maps first makes subsequent lostpointercapture events harmless.
    heldButtons.forEach(button => button.classList.remove("held"));
    send("ReleaseControls");
    flush(true);
  }

  function releaseSteering(pointerId) {
    if (pointerId !== undefined && pointerId !== steeringPointer) return;
    steeringPointer = null;
    steeringAxis = 0;
    steeringKnob.style.transform = "translate3d(0,0,0)";
    steeringPad.classList.remove("held");
    steeringPad.setAttribute("aria-valuenow", "0");
  }

  function updateSteering(event) {
    const bounds = steeringPad.getBoundingClientRect();
    const radius = Math.min(bounds.width, bounds.height) * .32;
    const x = event.clientX - (bounds.left + bounds.width * .5);
    const y = event.clientY - (bounds.top + bounds.height * .5);
    const length = Math.hypot(x, y);
    const factor = length > radius ? radius / length : 1;
    const clampedX = x * factor, clampedY = y * factor;
    steeringAxis = radius > 0 ? clampedX / radius : 0;
    steeringKnob.style.transform = `translate3d(${clampedX.toFixed(2)}px,${clampedY.toFixed(2)}px,0)`;
    steeringPad.setAttribute("aria-valuenow", String(Math.round(steeringAxis * 100)));
    flush();
  }

  steeringPad.addEventListener("pointerdown", event => {
    event.preventDefault();
    if (paused || !ready || steeringPointer !== null) return;
    steeringPointer = event.pointerId;
    steeringPad.setPointerCapture(event.pointerId);
    steeringPad.classList.add("held");
    updateSteering(event);
  });
  steeringPad.addEventListener("pointermove", event => {
    if (event.pointerId !== steeringPointer) return;
    event.preventDefault();
    updateSteering(event);
  });
  const endSteering = event => { releaseSteering(event.pointerId); flush(); };
  steeringPad.addEventListener("pointerup", endSteering);
  steeringPad.addEventListener("pointercancel", endSteering);
  steeringPad.addEventListener("lostpointercapture", endSteering);
  steeringPad.addEventListener("contextmenu", event => event.preventDefault());

  function setPaused(value, reason = "") {
    paused = value;
    releaseAll();
    send(value ? "PausePreview" : "ResumePreview");
    panel.hidden = !value;
    document.body.classList.toggle("paused", value);
    document.body.classList.toggle("running", !value);
    $("pause").textContent = value ? "再開" : "停止";
    if (ready) {
      $("start-title").textContent = value ? "試走を再開しよう" : "コロニー内壁を走ろう";
      start.textContent = "試走を始める";
      $("loading-text").textContent = reason || "準備できました。加速を操作すると進みます。";
    }
    flush(true);
  }

  heldButtons.forEach(button => {
    button.addEventListener("pointerdown", event => {
      event.preventDefault();
      if (paused || !ready) return;
      pointers.set(event.pointerId, button.dataset.held);
      button.setPointerCapture(event.pointerId);
      flush();
    });
    const release = event => { pointers.delete(event.pointerId); flush(); };
    button.addEventListener("pointerup", release);
    button.addEventListener("pointercancel", release);
    button.addEventListener("lostpointercapture", release);
    button.addEventListener("contextmenu", event => event.preventDefault());
  });
  // Independent IDs retain acceleration while a second thumb steers or cancels.
  window.addEventListener("pointerup", event => { pointers.delete(event.pointerId); lookPointers.delete(event.pointerId); releaseSteering(event.pointerId); flush(); });
  window.addEventListener("pointercancel", event => { pointers.delete(event.pointerId); lookPointers.delete(event.pointerId); releaseSteering(event.pointerId); flush(); });

  const lookZone = $("look-zone");
  lookZone.addEventListener("pointerdown", event => {
    event.preventDefault();
    if (paused || !ready) return;
    lookPointers.set(event.pointerId, {startX:event.clientX, startY:event.clientY, x:event.clientX, y:event.clientY});
    lookZone.setPointerCapture(event.pointerId);
  });
  lookZone.addEventListener("pointermove", event => {
    const look = lookPointers.get(event.pointerId);
    if (!look) return;
    event.preventDefault(); look.x = event.clientX; look.y = event.clientY; flush();
  });
  lookZone.addEventListener("lostpointercapture", event => { lookPointers.delete(event.pointerId); flush(); });
  lookZone.addEventListener("contextmenu", event => event.preventDefault());

  window.addEventListener("keydown", event => {
    if (!keyActions.has(event.code) && !commandKeys.has(event.code)) return;
    event.preventDefault(); event.stopImmediatePropagation();
    if (event.repeat) return;
    if (event.code === "KeyP" || event.code === "Escape") { if (ready) setPaused(!paused); return; }
    if (paused || !ready) return;
    if (keyActions.has(event.code)) { keys.add(event.code); flush(); }
    else if (event.code === "KeyR") { releaseAll(); send("ResetPreview"); }
    else { releaseAll(); send("VisitDistrict", {F1:"Core", F2:"East", F3:"West"}[event.code]); }
  }, true);
  window.addEventListener("keyup", event => {
    if (!keyActions.has(event.code) && !commandKeys.has(event.code)) return;
    event.preventDefault(); event.stopImmediatePropagation(); keys.delete(event.code); flush();
  }, true);
  window.addEventListener("blur", () => { if (ready) setPaused(true, "画面を離れたので停止したよ。"); else releaseAll(); });
  window.addEventListener("pagehide", () => { if (ready) setPaused(true); else releaseAll(); });
  document.addEventListener("visibilitychange", () => { if (document.hidden) { if (ready) setPaused(true, "画面を離れたので停止したよ。"); else releaseAll(); } });
  start.addEventListener("click", () => { if (ready) setPaused(false); });
  $("pause").addEventListener("click", () => { if (ready) setPaused(!paused); });
  $("reset").addEventListener("click", () => { releaseAll(); send("ResetPreview"); });
  document.querySelectorAll("[data-district]").forEach(button => button.addEventListener("click", () => { releaseAll(); send("VisitDistrict", button.dataset.district); }));
  $("quality").addEventListener("click", () => {
    detailed = !detailed;
    $("quality").textContent = detailed ? "詳細" : "軽量";
    $("quality").setAttribute("aria-pressed", String(detailed));
    send("SetQuality", detailed ? "detail" : "light");
    resizeCanvas();
  });

  function resizeCanvas() {
    const bounds = canvas.getBoundingClientRect();
    // Keep CSS full screen, cap actual framebuffer by long edge and total pixels.
    const maxEdge = detailed ? 1600 : 960;
    const maxPixels = detailed ? 1400000 : 960 * 540;
    const scale = Math.min(1, maxEdge / Math.max(bounds.width, bounds.height), Math.sqrt(maxPixels / Math.max(1, bounds.width * bounds.height)));
    const width = Math.max(1, Math.round(bounds.width * scale));
    const height = Math.max(1, Math.round(bounds.height * scale));
    if (canvas.width !== width || canvas.height !== height) { canvas.width = width; canvas.height = height; }
  }
  window.addEventListener("resize", () => { releaseAll(); resizeCanvas(); });
  if (window.visualViewport) window.visualViewport.addEventListener("resize", resizeCanvas);
  resizeCanvas();

  function fail(message) {
    loadError = String(message);
    paused = true; releaseAll(); panel.hidden = false;
    $("start-title").textContent = "読み込みを確認してね";
    $("loading-text").textContent = loadError;
    start.disabled = true; start.textContent = "ページを再読み込み";
    $("status").textContent = "Unity の読み込みに失敗しました";
  }

  window.ColonyRacerWebPreview = {
    receiveTelemetry(json) {
      let value;
      try { value = JSON.parse(json); } catch { return; }
      latestTelemetry = Object.freeze(value);
      telemetryReceivedAt = performance.now();
      if (value.ready && !ready) {
        ready = true;
        start.disabled = false; start.textContent = "試走を始める";
        $("pause").disabled = false;
        $("loading").hidden = true;
        $("loading-text").textContent = "準備できました。加速を操作すると進みます。";
        send("SetQuality", detailed ? "detail" : "light");
        send("PausePreview");
      }
      if (value.paused && !paused && ready) setPaused(true, "ゲームは停止中です。");
      $("speed").textContent = Number(value.speedKmh || 0).toFixed(1);
      $("contact").textContent = value.paused ? "停止中" : value.grounded ? "接地" : "浮上";
      $("contact").style.color = value.grounded || value.paused ? "#a6e9c4" : "#ffcb9e";
      $("district-name").textContent = value.district || "Core";
      if (performance.now() - statusTimer > 500) {
        statusTimer = performance.now();
        $("status").textContent = `${value.district || "Core"} · ${Number(value.fps || 0).toFixed(0)} fps · ${detailed ? "詳細" : "軽量"} · 上限120km/h`;
      }
      window.dispatchEvent(new CustomEvent("colony-telemetry", {detail:latestTelemetry}));
    },
    pause() { if (ready) setPaused(true); },
    resume() { if (ready) setPaused(false); },
    snapshot() { return {ready, paused, detailed, touchLayout, steeringAxis, controls:controls(), telemetry:latestTelemetry, telemetryAgeMs:performance.now()-telemetryReceivedAt, loadError, canvas:{width:canvas.width,height:canvas.height}}; }
  };
  document.body.classList.add("paused");
  document.body.classList.add(touchLayout ? "touch-layout" : "desktop-layout");
  $("quality").textContent = detailed ? "詳細" : "軽量";
  $("quality").setAttribute("aria-pressed", String(detailed));
  // Renew held state so a stalled/lost browser controller cannot leave the car accelerating.
  window.setInterval(() => { if (ready && !paused) flush(true); }, 100);
  const config = {...window.COLONY_UNITY_CONFIG};
  const loaderUrl = config.loaderUrl;
  delete config.loaderUrl;
  config.showBanner = (message, type) => { if (type === "error") fail(message); else console.warn(message); };
  const loader = document.createElement("script");
  loader.src = loaderUrl;
  loader.onerror = () => fail("ゲームのファイルを取得できませんでした。通信を確認して再読み込みしてね。");
  loader.onload = () => {
    createUnityInstance(canvas, config, progress => {
      $("loading").value = progress;
      $("loading-text").textContent = `Unity を読み込み中… ${Math.round(progress * 100)}%`;
    }).then(instance => {
      unity = instance;
      resizeCanvas();
      // A telemetry packet may arrive before createUnityInstance resolves.
      if (ready) { send("SetQuality", detailed ? "detail" : "light"); send("PausePreview"); }
    }).catch(fail);
  };
  document.body.appendChild(loader);
})();
