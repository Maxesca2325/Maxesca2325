// 3D world for the 15 s "protocole" prototype. Everything is a pure function of time t (seconds):
// window.__render3d(t) draws the frame for t. Loaded as a module from index.html.
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/RoundedBoxGeometry.js";

const W = 1080, H = 1920;
const canvas = document.getElementById("w3d-canvas");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true, powerPreference: "high-performance" });
renderer.setPixelRatio(1);
renderer.setSize(W, H, false);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;
renderer.outputColorSpace = THREE.SRGBColorSpace;

const scene = new THREE.Scene();
scene.background = new THREE.Color("#0b0a18");
scene.fog = new THREE.Fog("#0b0a18", 6, 13);
const camera = new THREE.PerspectiveCamera(35, W / H, 0.05, 40);

// ---------- helpers ----------
const clamp01 = (x) => Math.min(1, Math.max(0, x));
const lerp = (a, b, k) => a + (b - a) * k;
const smooth = (x) => { x = clamp01(x); return x * x * (3 - 2 * x); };
const ease = {
  inOut2: (x) => (x < 0.5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2),
  inOut3: (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2),
  out3: (x) => 1 - Math.pow(1 - x, 3),
  in3: (x) => x * x * x,
  sine: (x) => -(Math.cos(Math.PI * x) - 1) / 2,
};
const seg = (t, a, b, e = ease.inOut2) => e(clamp01((t - a) / (b - a)));
const pulse = (t, at, up, down) => (t < at ? 0 : t < at + up ? (t - at) / up : Math.max(0, 1 - (t - at - up) / down));
const std = (color, o = {}) => new THREE.MeshStandardMaterial({ color, roughness: 0.75, metalness: 0, ...o });
function mesh(geo, mat, x = 0, y = 0, z = 0, parent = scene, shadow = true) {
  const m = new THREE.Mesh(geo, mat);
  m.position.set(x, y, z);
  m.castShadow = shadow; m.receiveShadow = true;
  parent.add(m);
  return m;
}
const texs = [];
function canvasTex(w, h, draw) {
  const c = document.createElement("canvas"); c.width = w; c.height = h;
  const g = c.getContext("2d");
  draw(g, w, h);
  const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 8;
  tx.userData.redraw = () => { g.clearRect(0, 0, w, h); draw(g, w, h); tx.needsUpdate = true; };
  texs.push(tx);
  return tx;
}
// deterministic hash for "random" details
const hash = (i) => { let x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };

// ---------- room (x: -4..4, z: -4..4, y: 0..3) ----------
const wallMat = std("#2a2650", { roughness: 0.95 });
const floorTex = canvasTex(1024, 1024, (g, w, h) => {
  for (let i = 0; i < 16; i++) {
    const v = 52 + Math.floor(hash(i) * 22);
    g.fillStyle = `rgb(${v + 26},${v + 8},${v + 30})`; g.fillRect(0, i * 64, w, 64);
    g.fillStyle = "rgba(10,6,20,.55)"; g.fillRect(0, i * 64, w, 3);
    g.fillRect(Math.floor(hash(i + 50) * w), i * 64, 3, 64);
  }
});
floorTex.wrapS = floorTex.wrapT = THREE.RepeatWrapping; floorTex.repeat.set(3, 3);
mesh(new THREE.PlaneGeometry(8, 8), std("#ffffff", { map: floorTex, roughness: 0.6 }), 0, 0, 0, scene, false).rotation.x = -Math.PI / 2;
mesh(new THREE.PlaneGeometry(8, 3.2), wallMat, 0, 1.6, -4, scene, false); // back wall
const leftWall = mesh(new THREE.PlaneGeometry(8, 3.2), wallMat, -4, 1.6, 0, scene, false); leftWall.rotation.y = Math.PI / 2;
const rightWallMat = std("#2e2954", { roughness: 0.95 });
// right wall with a door hole (door centred at z=-0.5, 0.95 wide, 2.1 high)
[[-4, -0.975], [-0.025, 4]].forEach(([a, b]) => { const p = mesh(new THREE.PlaneGeometry(b - a, 3.2), rightWallMat, 4, 1.6, (a + b) / 2, scene, false); p.rotation.y = -Math.PI / 2; });
const lintel = mesh(new THREE.PlaneGeometry(0.95, 1.1), rightWallMat, 4, 2.65, -0.5, scene, false); lintel.rotation.y = -Math.PI / 2;
mesh(new THREE.PlaneGeometry(8, 8), std("#1c1934"), 0, 3.2, 0, scene, false).rotation.x = Math.PI / 2; // ceiling
// skirting boards
const skirt = std("#3b3566");
mesh(new THREE.BoxGeometry(8, 0.12, 0.03), skirt, 0, 0.06, -3.98);

// window on the back wall, moon outside
const winX = -2.0, winY = 1.95;
const glass = mesh(new THREE.PlaneGeometry(1.3, 1.5), new THREE.MeshBasicMaterial({ color: "#2c3d7a" }), winX, winY, -3.99, scene, false);
const moon = mesh(new THREE.CircleGeometry(0.17, 48), new THREE.MeshBasicMaterial({ color: "#eef2ff" }), winX + 0.32, winY + 0.4, -3.985, scene, false);
const moonHalo = mesh(new THREE.CircleGeometry(0.42, 48), new THREE.MeshBasicMaterial({ color: "#9fb2ff", transparent: true, opacity: 0.25 }), winX + 0.32, winY + 0.4, -3.988, scene, false);
const frameMat = std("#3d3768", { roughness: 0.6 });
[[0, 0.78, 1.42, 0.08], [0, -0.78, 1.42, 0.08], [-0.69, 0, 0.08, 1.64], [0.69, 0, 0.08, 1.64], [0, 0, 0.06, 1.5], [0, 0.05, 1.3, 0.06]].forEach(([x, y, w, h]) =>
  mesh(new THREE.BoxGeometry(w, h, 0.08), frameMat, winX + x, winY + y, -3.95));
mesh(new THREE.BoxGeometry(1.6, 0.06, 0.25), frameMat, winX, winY - 0.85, -3.86); // sill
// curtain (folds), sways a little
const curtainGeo = new THREE.PlaneGeometry(0.55, 1.9, 24, 1);
const cpos = curtainGeo.attributes.position;
for (let i = 0; i < cpos.count; i++) cpos.setZ(i, Math.sin(cpos.getX(i) * 26) * 0.035);
curtainGeo.computeVertexNormals();
const curtain = mesh(curtainGeo, std("#4a3870", { side: THREE.DoubleSide, roughness: 0.9 }), winX - 0.95, winY - 0.1, -3.9);

// ---------- bed + character ----------
const bed = new THREE.Group(); bed.position.set(-1.7, 0, -2.75); scene.add(bed);
mesh(new RoundedBoxGeometry(1.7, 0.42, 2.3, 4, 0.06), std("#3f3366"), 0, 0.25, 0, bed);
mesh(new RoundedBoxGeometry(1.8, 1.1, 0.12, 4, 0.05), std("#3f3366"), 0, 0.6, -1.17, bed); // headboard
mesh(new RoundedBoxGeometry(1.6, 0.2, 2.15, 4, 0.08), std("#d7d2ea"), 0, 0.55, 0.02, bed); // mattress
const pillow = mesh(new RoundedBoxGeometry(0.95, 0.2, 0.5, 6, 0.09), std("#e9e5f6", { roughness: 0.9 }), 0, 0.72, -0.78, bed);
pillow.scale.set(1, 1, 1);

// the hero: a round toy-like head on the pillow, body under the blanket
const skin = std("#f3e5d8", { roughness: 0.55 });
const hero = new THREE.Group(); hero.position.set(0, 0.95, -0.66); bed.add(hero);
const head = mesh(new THREE.SphereGeometry(0.27, 64, 48), skin, 0, 0, 0, hero);
head.scale.set(1, 0.97, 0.93);
const hair = mesh(new THREE.SphereGeometry(0.285, 64, 32, 0, Math.PI * 2, 0, Math.PI * 0.42), std("#3b2622", { roughness: 0.65 }), 0, 0.01, -0.03, hero);
hair.rotation.x = -0.95;
const eyeWhite = std("#ffffff", { roughness: 0.3 });
const pupilMat = std("#120d1c", { roughness: 0.2 });
const eyes = [], pupils = [], lids = [], brows = [];
[-1, 1].forEach((s) => {
  const e = mesh(new THREE.SphereGeometry(0.058, 32, 24), eyeWhite, s * 0.095, 0.02, 0.215, hero, false); eyes.push(e);
  const p = mesh(new THREE.SphereGeometry(0.03, 24, 16), pupilMat, s * 0.095, 0.02, 0.262, hero, false); pupils.push(p);
  const l = mesh(new THREE.SphereGeometry(0.062, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2), skin, s * 0.095, 0.02, 0.215, hero, false); lids.push(l);
  const b = mesh(new THREE.CapsuleGeometry(0.012, 0.07, 6, 12), std("#3b2622"), s * 0.1, 0.11, 0.24, hero, false);
  b.rotation.z = Math.PI / 2; brows.push(b);
});
const mouth = mesh(new THREE.TorusGeometry(0.035, 0.009, 10, 32, Math.PI), pupilMat, 0, -0.1, 0.245, hero, false);
// blanket: a cloth sheet draped over a body-shaped bump
const blanketGeo = new THREE.PlaneGeometry(1.75, 1.75, 90, 90);
const bpos = blanketGeo.attributes.position;
for (let i = 0; i < bpos.count; i++) {
  const x = bpos.getX(i), y = bpos.getY(i);
  const body = Math.exp(-(x * x) / 0.09) * Math.exp(-Math.pow(Math.max(0, y - 0.1), 2) / 0.9) * 0.22; // torso + legs
  const folds = Math.sin(x * 9 + y * 3) * 0.012 + Math.sin(y * 7 - x * 2) * 0.01;
  const drape = -Math.pow(Math.max(0, Math.abs(x) - 0.78), 1.4) * 2.2;
  bpos.setZ(i, body + folds + drape);
}
blanketGeo.computeVertexNormals();
const blanket = mesh(blanketGeo, std("#5b4a9a", { roughness: 0.92, side: THREE.DoubleSide }), 0, 0.67, 0.25, bed);
blanket.rotation.x = -Math.PI / 2;

// nightstand + alarm clock
const stand = new THREE.Group(); stand.position.set(-0.45, 0, -3.5); scene.add(stand);
mesh(new RoundedBoxGeometry(0.6, 0.6, 0.5, 4, 0.04), std("#3a2f5c"), 0, 0.3, 0, stand);
mesh(new RoundedBoxGeometry(0.34, 0.16, 0.14, 4, 0.03), std("#141024"), 0, 0.68, 0.05, stand);
const clockFace = canvasTex(256, 112, (g, w, h) => {
  g.fillStyle = "#0b0812"; g.fillRect(0, 0, w, h);
  g.font = "bold 84px 'JetBrains Mono', monospace"; g.textAlign = "center"; g.textBaseline = "middle";
  g.shadowColor = "#ff3040"; g.shadowBlur = 18; g.fillStyle = "#ff3a46"; g.fillText("2:41", w / 2, h / 2 + 4);
});
mesh(new THREE.PlaneGeometry(0.29, 0.125), new THREE.MeshBasicMaterial({ map: clockFace }), 0, 0.68, 0.122, stand, false);
const clockLight = new THREE.PointLight("#ff2a3a", 0.35, 1.4, 2); clockLight.position.set(-0.45, 0.75, -3.25); scene.add(clockLight);

// ---------- door (right wall x=4, centred z=-0.5) ----------
const doorPivot = new THREE.Group(); doorPivot.position.set(3.97, 0, -0.975); scene.add(doorPivot); // hinge
const doorMat = std("#4b3b70", { roughness: 0.7 });
const door = mesh(new RoundedBoxGeometry(0.06, 2.06, 0.93, 3, 0.012), doorMat, 0, 1.06, 0.475, doorPivot);
const panelMat = std("#43356a", { roughness: 0.7 });
[[1.52, 0.7], [0.55, 0.85]].forEach(([y, h]) => mesh(new RoundedBoxGeometry(0.02, h, 0.66, 2, 0.008), panelMat, -0.035, y, 0.475, doorPivot));
const knob = mesh(new THREE.SphereGeometry(0.035, 24, 16), std("#c9b27a", { metalness: 0.6, roughness: 0.35 }), -0.07, 1.0, 0.82, doorPivot);
const jambMat = std("#2b2448");
[[-0.5 - 0.5, 0.06], [0.0, 0.06]].forEach(([z]) => mesh(new THREE.BoxGeometry(0.12, 2.18, 0.06), jambMat, 3.95, 1.09, z + 0.0));
mesh(new THREE.BoxGeometry(0.12, 0.08, 1.07), jambMat, 3.95, 2.16, -0.5);
// light under the door: a thin bright strip + warm spill on the floor with the feet shadows (canvas, animated by offset)
const gapMat = new THREE.MeshBasicMaterial({ color: "#ffd9a0" });
const gap = mesh(new THREE.PlaneGeometry(0.93, 0.022), gapMat, 3.995, 0.011, -0.5, scene, false); gap.rotation.y = -Math.PI / 2;
const spillTex = canvasTex(512, 512, (g, w, h) => {
  const gr = g.createRadialGradient(w / 2, 0, 10, w / 2, 0, h * 0.95);
  gr.addColorStop(0, "rgba(255,200,130,0.95)"); gr.addColorStop(0.35, "rgba(242,170,90,0.45)"); gr.addColorStop(1, "rgba(242,170,90,0)");
  g.fillStyle = gr; g.fillRect(0, 0, w, h);
});
const spill = mesh(new THREE.PlaneGeometry(1.6, 1.4), new THREE.MeshBasicMaterial({ map: spillTex, transparent: true, opacity: 0.55, depthWrite: false, blending: THREE.AdditiveBlending }), 3.3, 0.004, -0.5, scene, false);
spill.rotation.x = -Math.PI / 2; spill.rotation.z = -Math.PI / 2;
// feet blocking the gap (outside the room, visible through the gap as dark notches)
const feet = new THREE.Group(); feet.position.set(4.06, 0.011, -0.5); scene.add(feet);
const footMat = new THREE.MeshBasicMaterial({ color: "#120d1c" });
[-0.17, 0.17].forEach((z) => { const f = mesh(new THREE.PlaneGeometry(0.16, 0.03), footMat, -0.06, 0, z, feet, false); f.rotation.y = -Math.PI / 2; });
const footShadows = [];
[-0.17, 0.17].forEach((z) => {
  const s = mesh(new THREE.PlaneGeometry(0.62, 0.15), new THREE.MeshBasicMaterial({ color: "#000000", transparent: true, opacity: 0.55, depthWrite: false }), 3.65, 0.006, -0.5 + z, scene, false);
  s.rotation.x = -Math.PI / 2; footShadows.push(s);
});
const doorWarm = new THREE.PointLight("#ffb46a", 0.9, 2.4, 2); doorWarm.position.set(3.75, 0.06, -0.5); scene.add(doorWarm);

// the paper that slides under the door
const paperTex = (withLine) => canvasTex(900, 1200, (g, w, h) => {
  g.fillStyle = "#efe6d2"; g.fillRect(0, 0, w, h);
  for (let i = 0; i < 1400; i++) { g.fillStyle = `rgba(120,100,70,${0.04 * hash(i)})`; g.fillRect(hash(i + 9) * w, hash(i + 77) * h, 2, 2); }
  g.textAlign = "center"; g.fillStyle = "#1a1426";
  g.font = "700 128px Oswald, 'League Gothic', sans-serif"; g.fillText("RÈGLE N°1", w / 2, 430);
  g.fillStyle = "#1a1426"; g.fillRect(w / 2 - 170, 470, 340, 6);
  if (withLine) { g.fillStyle = "#8e1b22"; g.font = "italic 118px 'EB Garamond', Georgia, serif"; g.fillText("Ne réponds", w / 2, 690); g.fillText("pas.", w / 2, 820); }
});
const paperA = paperTex(false), paperB = paperTex(true);
const paperMat = new THREE.MeshStandardMaterial({ map: paperA, emissiveMap: paperA, emissive: new THREE.Color("#c9b9a0"), emissiveIntensity: 0.75, roughness: 0.85, side: THREE.DoubleSide });
const paper = mesh(new THREE.PlaneGeometry(0.21, 0.28), paperMat, 0, 0, 0, scene, true);

// ---------- light ----------
scene.add(new THREE.HemisphereLight("#6f78c8", "#1a1530", 0.55));
const moonLight = new THREE.DirectionalLight("#9fb2ff", 2.4);
moonLight.position.set(winX + 0.6, 3.6, -6.5); moonLight.target.position.set(-1.6, 0.6, -2.4);
moonLight.castShadow = true; moonLight.shadow.mapSize.set(2048, 2048); moonLight.shadow.bias = -0.0004; moonLight.shadow.normalBias = 0.02;
Object.assign(moonLight.shadow.camera, { left: -3, right: 3, top: 3, bottom: -3, near: 0.5, far: 14 });
scene.add(moonLight, moonLight.target);
const rim = new THREE.PointLight("#8a7dff", 0.6, 6, 2); rim.position.set(0.5, 2.2, -1.0); scene.add(rim);

// ---------- camera path ----------
const V = (x, y, z) => new THREE.Vector3(x, y, z);
const FACE = V(-1.7, 0.95, -3.41);      // hero's face (world)
const DOOR = V(3.95, 1.0, -0.5);
const GAPPT = V(3.95, 0.03, -0.5);
function cameraAt(t) {
  // shot A: close on the face, slow push (0 – 4.3)
  let pos = V(-1.3, 1.36, -1.35).lerp(V(-1.42, 1.31, -1.68), seg(t, 0, 4.3, ease.sine));
  let look = FACE.clone().add(V(0.12, -0.08, 0.2));
  let fov = lerp(40, 37, seg(t, 0, 4.3, ease.sine));
  // whip to the door (4.3 – 4.75)
  const w = seg(t, 4.3, 4.75, ease.inOut3);
  pos.lerp(V(-0.9, 1.3, -2.1), w); look.lerp(DOOR, w); fov = lerp(fov, 38, w);
  // door shot: slow push (4.75 – 7.3)
  pos.lerp(V(0.6, 1.15, -1.25), seg(t, 4.75, 7.3, ease.sine));
  // dive down to the gap (7.3 – 8.3), keep creeping (8.3 – 10.4)
  const d = seg(t, 7.3, 8.3, ease.inOut2);
  pos.lerp(V(2.75, 0.2, -0.5), d); look.lerp(GAPPT, d); fov = lerp(fov, 46, d);
  pos.lerp(V(3.05, 0.16, -0.5), seg(t, 8.3, 10.4, ease.sine));
  // knocks: camera punch (fov) on each
  fov -= 1.6 * (pulse(t, 4.9, 0.05, 0.18) + pulse(t, 5.25, 0.05, 0.18) + pulse(t, 5.6, 0.05, 0.18));
  // never fully still: tiny handheld drift
  pos.x += Math.sin(t * 0.9) * 0.008; pos.y += Math.sin(t * 1.3 + 1) * 0.006;
  return { pos, look, fov };
}

// ---------- the frame at time t ----------
function pose(t) {
  // camera
  const c = cameraAt(t);
  camera.position.copy(c.pos); camera.fov = c.fov; camera.updateProjectionMatrix(); camera.lookAt(c.look);
  camera.updateMatrixWorld();

  // curtain sway
  curtain.rotation.y = Math.sin(t * 0.8) * 0.06;
  // acting: blink at 1.0 and 3.7, eyes widen on "frappe", brows up, pupils to the door
  const blink = Math.max(pulse(t, 1.0, 0.07, 0.09), pulse(t, 3.7, 0.07, 0.09));
  const scared = seg(t, 2.55, 2.8, ease.out3);
  lids.forEach((l) => { l.visible = blink > 0.02; l.rotation.x = lerp(-1.75, -0.2, blink); l.scale.setScalar(1.0 + 0.18 * scared); });
  eyes.forEach((e) => e.scale.setScalar(1 + 0.18 * scared));
  const look = seg(t, 3.9, 4.2, ease.out3);
  pupils.forEach((p, i) => { p.position.x = (i ? 1 : -1) * 0.095 + 0.028 * look - 0.006 * pulse(t, 3.82, 0.06, 0.06); p.position.y = 0.02 + 0.006 * scared; p.scale.setScalar(1 - 0.25 * scared); });
  brows.forEach((b, i) => { b.position.y = 0.11 + 0.035 * scared; b.rotation.z = Math.PI / 2 + (i ? -1 : 1) * 0.25 * scared; });
  mouth.rotation.z = 0; mouth.scale.set(lerp(0.9, 1.05, scared), lerp(0.22, 1.0, scared), 1);
  hero.rotation.y = 0.35 * seg(t, 3.95, 4.4, ease.inOut2); // head turns towards the door
  hero.position.y = 0.95 + Math.sin(t * 1.6) * 0.004;      // breathing
  blanket.position.y = 0.67 + Math.sin(t * 1.6) * 0.006;

  // knocks: the door jumps on its hinge
  const k = pulse(t, 4.9, 0.03, 0.12) - pulse(t, 5.25, 0.03, 0.12) + pulse(t, 5.6, 0.03, 0.12);
  doorPivot.rotation.y = 0.012 * k;
  // far knocks during "frappe" make the room tremble very slightly (handled by the camera drift) – feet shift on "seul"
  const fs = seg(t, 6.6, 7.1, ease.inOut2);
  feet.position.z = -0.5 + 0.05 * fs; footShadows.forEach((s, i) => (s.position.z = -0.5 + (i ? 0.17 : -0.17) + 0.05 * fs));

  // the paper: slides out from under the door (9.15 – 9.9), then rises to fill the frame (10.4 – 11.2)
  const slide = seg(t, 9.15, 9.9, ease.out3);
  const floorPose = { p: V(lerp(4.1, 3.58, slide), 0.004, -0.5), q: new THREE.Quaternion().setFromEuler(new THREE.Euler(-Math.PI / 2, 0, -Math.PI / 2 + 0.12 * slide)) };
  const r = seg(t, 10.35, 11.2, ease.inOut3);
  const camQ = camera.quaternion.clone();
  const front = V(0, 0, -0.31).applyQuaternion(camQ).add(camera.position);
  const tilt = new THREE.Quaternion().setFromEuler(new THREE.Euler(0, 0, -0.03 + 0.02 * Math.sin(t * 0.7)));
  paper.position.copy(floorPose.p).lerp(front, r);
  paper.quaternion.copy(floorPose.q).slerp(camQ.clone().multiply(tilt), r);
  paper.position.y += Math.sin(Math.PI * r) * 0.12; // a little arc on the way up
  paper.visible = t > 9.1;
  paperMat.map = paperMat.emissiveMap = t >= 12.6 ? paperB : paperA;
  paperMat.emissiveIntensity = t < 14.0 ? 0.75 : 0.28;

  // the light behind the door goes out at 14.0
  const on = t < 14.0 ? 1 : 0;
  gapMat.color.set(on ? "#ffd9a0" : "#1a1426"); spill.visible = !!on; doorWarm.intensity = 0.9 * on + 0.15 * pulse(t, 4.9, 0.02, 0.1);
  feet.visible = !!on; footShadows.forEach((s) => (s.visible = !!on));
  moonLight.intensity = on ? 2.4 : 1.2; clockLight.intensity = on ? 0.35 : 0.2;
}

// motion blur by accumulating sub-frames during the whip (deterministic)
const rt = new THREE.WebGLRenderTarget(W, H, { type: THREE.HalfFloatType, samples: 4 });
const accScene = new THREE.Scene();
const accCam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
const accMat = new THREE.MeshBasicMaterial({ map: rt.texture, transparent: true, blending: THREE.AdditiveBlending, depthTest: false, depthWrite: false, toneMapped: true });
accScene.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), accMat));
const FRAME = 1 / 60;
function render(t) {
  const blur = (t > 4.3 && t < 4.8) || (t > 7.35 && t < 8.25) || (t > 10.4 && t < 11.15);
  if (!blur) { pose(t); renderer.setRenderTarget(null); renderer.render(scene, camera); return; }
  const N = 6;
  renderer.setRenderTarget(null); renderer.setClearColor("#000000", 1); renderer.clear();
  accMat.opacity = 1 / N;
  for (let i = 0; i < N; i++) {
    pose(t - (FRAME * 0.9 * i) / N);
    renderer.setRenderTarget(rt); renderer.render(scene, camera);
    renderer.setRenderTarget(null); renderer.autoClear = false; renderer.render(accScene, accCam); renderer.autoClear = true;
  }
}

window.__render3d = render;
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["w3d"] = (async () => {
  await Promise.all(["700 128px Oswald", "italic 118px 'EB Garamond'", "bold 84px 'JetBrains Mono'"].map((f) => document.fonts.load(f)));
  await document.fonts.ready;
  texs.forEach((tx) => tx.userData.redraw());
  await renderer.compileAsync(scene, camera);
  render(window.__w3dTime || 0);
})();
