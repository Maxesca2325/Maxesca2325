// Episode 2 sets: Saint-Pierre (Martinique, 1902) under the montagne Pelée, the prison and its cachot, the cloud, the circus.
// Layout (shared by every set): the volcano is far to -z (crater at [0, 50, -110]); the sea is to +z.
import React, { useMemo } from "react";
import * as THREE from "three";
import { useCurrentFrame, useVideoConfig } from "remotion";
import { Box, Cyl, Ground, Roof, Window, Snow, Sign, Fire } from "../engine/kit";
import { bricks, cobbles, painted, planks, roofSlate, sky, water, rng, shade } from "../engine/tex";
import { LAYER_FX } from "../engine/Stage";
import type { Look, V3 } from "../engine/Stage";

const useT = () => { const f = useCurrentFrame(); const { fps } = useVideoConfig(); return f / fps; };
const canvasTex = (w: number, h: number, draw: (g: CanvasRenderingContext2D) => void) => {
  const c = document.createElement("canvas"); c.width = w; c.height = h; draw(c.getContext("2d")!);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t;
};

// ---------- looks ----------
export const tropLook = (): Look => ({
  sky: sky("#2a7ae0", "#7ab8f5", "#e2f0ff", "#ffffff"),
  fog: "#cfe0f2", fogNear: 60, fogFar: 320,
  sun: { pos: [20, 26, 14], color: "#ffe0b0", intensity: 3.3, shadow: 34 },
  hemi: { sky: "#a8d0ff", ground: "#7a4a8a", intensity: 1.05 },
  ambient: 0.1, exposure: 1.05, aperture: 0.38, warm: "#ffb070", cool: "#5a3fc8", vignette: 0.45, saturation: 1.28,
});
export const ashLook = (): Look => ({
  sky: sky("#7a7a86", "#b0a490", "#d8c8a8", "#9a9088"),
  fog: "#b8ab96", fogNear: 40, fogFar: 260,
  sun: { pos: [20, 26, 14], color: "#ffd6a0", intensity: 2.4, shadow: 34 },
  hemi: { sky: "#c8c0b0", ground: "#6a4a7a", intensity: 0.95 },
  ambient: 0.12, exposure: 1.05, aperture: 0.4, warm: "#ffb070", cool: "#5a3fc8", vignette: 0.55, saturation: 1.05,
});
export const eruptLook = (): Look => ({
  sky: sky("#3a2a2a", "#8a4a2a", "#e08a4a", "#6a4a3a"),
  fog: "#8a5a40", fogNear: 50, fogFar: 300,
  sun: { pos: [-10, 30, 20], color: "#ffb070", intensity: 2.4, shadow: 40 },
  hemi: { sky: "#ffb080", ground: "#4a2a5a", intensity: 0.9 },
  ambient: 0.12, exposure: 1.1, aperture: 0.38, warm: "#ff8a40", cool: "#5a2fa8", vignette: 0.6, saturation: 1.2,
});
export const burnLook = (): Look => ({
  fog: "#3a1a10", fogNear: 10, fogFar: 70,
  sun: { pos: [-10, 20, -20], color: "#ff7a3a", intensity: 2.2, shadow: 30 },
  hemi: { sky: "#ff8a4a", ground: "#2a1030", intensity: 0.7 },
  ambient: 0.12, exposure: 1.2, aperture: 0.45, warm: "#ff7a30", cool: "#4a1a8a", vignette: 0.75, saturation: 1.2,
});
export const nightLook = (): Look => ({
  sky: sky("#0d1640", "#2a3f8f", "#6a7fc9", "#3a4c96", true),
  fog: "#2b3f7f", fogNear: 25, fogFar: 140,
  sun: { pos: [-14, 22, 18], color: "#a9bcff", intensity: 1.4, shadow: 26 },
  hemi: { sky: "#7f97ff", ground: "#4a2f6a", intensity: 0.75 },
  ambient: 0.12, exposure: 1.3, aperture: 0.45, warm: "#ffae5a", cool: "#4b46d8", vignette: 0.6, saturation: 1.2,
});
export const ruinLook = (): Look => ({
  sky: sky("#8a8a92", "#b8b0a4", "#d8d0c4", "#a8a29a"),
  fog: "#b8b0a4", fogNear: 30, fogFar: 220,
  sun: { pos: [18, 24, 12], color: "#fff0d8", intensity: 2.6, shadow: 34 },
  hemi: { sky: "#c8ccd8", ground: "#5a4a7a", intensity: 1.0 },
  ambient: 0.12, exposure: 1.05, aperture: 0.4, warm: "#ffc890", cool: "#5a4fd0", vignette: 0.55, saturation: 0.85,
});
export const cellLook = (glow: string): Look => ({
  fog: "#140c0a", fogNear: 4, fogFar: 22,
  sun: { pos: [2, 10, 6], color: glow, intensity: 0.25, shadow: 6 },
  hemi: { sky: "#6a5a7a", ground: "#2a1a2a", intensity: 0.45 },
  ambient: 0.1, exposure: 1.55, aperture: 0.5, warm: "#ffa040", cool: "#4a2a8a", vignette: 0.8, saturation: 1.15,
});

// ---------- the volcano ----------
const volcanoTex = () => canvasTex(1024, 1024, (g) => {
  const r = rng(5);
  const grd = g.createLinearGradient(0, 0, 0, 1024);
  grd.addColorStop(0, "#6a5a4a"); grd.addColorStop(0.35, "#5a6a3a"); grd.addColorStop(1, "#2f6a3a");
  g.fillStyle = grd; g.fillRect(0, 0, 1024, 1024);
  for (let i = 0; i < 1800; i++) { const y = r() * 1024; g.fillStyle = y > 360 ? `rgba(30,${80 + r() * 60},40,0.35)` : `rgba(80,60,50,0.3)`; g.beginPath(); g.ellipse(r() * 1024, y, 8 + r() * 30, 5 + r() * 12, 0, 0, 7); g.fill(); }
  g.strokeStyle = "rgba(40,30,25,0.35)"; g.lineWidth = 6;
  for (let i = 0; i < 40; i++) { const x = r() * 1024; g.beginPath(); g.moveTo(x, 0); g.lineTo(x + (r() - 0.5) * 80, 300 + r() * 500); g.stroke(); }
});
export const CRATER: V3 = [0, 50, -110];
export const Volcano: React.FC<{ smoke?: number; glow?: number }> = ({ smoke = 1, glow = 0 }) => {
  const tex = useMemo(volcanoTex, []);
  const t = useT();
  const puffs = useMemo(() => { const r = rng(31); return Array.from({ length: 16 }, (_, i) => ({ x: (r() - 0.5) * 10, y: i * 3.2, z: (r() - 0.5) * 6, s: 4 + i * 0.7 + r() * 2, d: r() })); }, []);
  return (
    <group>
      <mesh position={[0, 25, -110]} receiveShadow>
        <cylinderGeometry args={[9, 64, 50, 40, 1, true]} />
        <meshStandardMaterial map={tex} roughness={1} />
      </mesh>
      <mesh position={[0, 50.1, -110]} rotation={[-Math.PI / 2, 0, 0]}>
        <circleGeometry args={[9, 32]} />
        <meshStandardMaterial color={glow ? "#ff6a2a" : "#3a2e28"} emissive="#ff4a10" emissiveIntensity={glow * 2} />
      </mesh>
      {/* the neighbouring hills */}
      <mesh position={[-70, 8, -90]} scale={[40, 18, 30]}><sphereGeometry args={[1, 24, 16]} /><meshStandardMaterial color="#3f7a40" roughness={1} /></mesh>
      <mesh position={[75, 10, -95]} scale={[45, 22, 30]}><sphereGeometry args={[1, 24, 16]} /><meshStandardMaterial color="#3a7040" roughness={1} /></mesh>
      {smoke > 0 ? puffs.map((p, i) => (
        <mesh key={i} layers={LAYER_FX} position={[p.x + Math.sin(t * 0.3 + i) * 1.5 + i * 0.9, 52 + p.y * smoke + t * 0.6, -110 + p.z]} scale={p.s * (0.6 + 0.4 * smoke)}>
          <sphereGeometry args={[1, 16, 12]} />
          <meshStandardMaterial color={i < 3 && glow ? "#a85a3a" : "#8a8580"} transparent opacity={0.85} roughness={1} emissive={glow ? "#ff5a20" : "#000000"} emissiveIntensity={glow * (i < 4 ? 0.6 : 0.1)} />
        </mesh>
      )) : null}
    </group>
  );
};

// ---------- the burning cloud (nuée ardente) ----------
// k: 0 = still in the crater, 0.5 = at the foot of the mountain, 1 = over the town and out to sea
const PATH: V3[] = [CRATER, [0, 4, -48], [0, 4, 40]];
const along = (s: number): V3 => {
  const L1 = 78, L2 = 88, d = s * (L1 + L2);
  const [a, b] = d < L1 ? [PATH[0], PATH[1]] : [PATH[1], PATH[2]];
  const k = d < L1 ? d / L1 : (d - L1) / L2;
  return [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k, a[2] + (b[2] - a[2]) * k];
};
export const Cloud: React.FC<{ k: number; width?: number }> = ({ k, width = 1 }) => {
  const t = useT();
  const puffs = useMemo(() => { const r = rng(13); return Array.from({ length: 200 }, () => ({ u: r(), x: r() - 0.5, y: r(), s: 0.6 + r() * 0.7, d: r() })); }, []);
  if (k <= 0) return null;
  return (
    <group>
      {puffs.map((p, i) => {
        const s = Math.min(1, p.u * k);
        const c = along(s);
        const grow = 0.4 + 0.6 * Math.min(1, s * 2.2);
        const r = (3 + 6.5 * grow) * p.s;
        const front = 1 - (k - s) / Math.max(0.01, k); // 1 at the front
        const roll = Math.sin(t * 1.6 + i) * 0.6;
        return (
          <mesh key={i} position={[c[0] + p.x * (14 + 60 * grow) * width, c[1] + r * 0.6 + p.y * r * 0.9 + roll, c[2] + (p.d - 0.5) * 6]} scale={r}>
            <icosahedronGeometry args={[1, 2]} />
            <meshStandardMaterial color={p.y < 0.3 ? "#5a3426" : "#4a4440"} emissive="#ff5a1a" emissiveIntensity={(p.y < 0.3 ? 0.55 : 0.04) * (0.4 + front * 0.6)} roughness={1} flatShading />
          </mesh>
        );
      })}
    </group>
  );
};

// ---------- the town ----------
const WALL = ["#f2d27a", "#e8a86a", "#f4e4c4", "#9ec8b8", "#e8b4a4", "#f2c890", "#c8d8e8"];
const SHUT = ["#2f6a4a", "#3a5a9a", "#7a3a2a", "#2f7a7a", "#5a4a8a"];
const roofRed = (k = 1) => roofSlate(shade("#b4542f", k), [2, 1.5]);

export const CHouse: React.FC<{ pos: V3; w?: number; h?: number; d?: number; rotY?: number; seed?: number; ruin?: boolean; ash?: number }> = ({ pos, w = 6, h = 7, d = 6, rotY = 0, seed = 1, ruin, ash = 0 }) => {
  const r = rng(seed);
  const wall = ruin ? "#9a948c" : WALL[Math.floor(r() * WALL.length)];
  const sh = ruin ? "#4a4440" : SHUT[Math.floor(r() * SHUT.length)];
  const wallMap = useMemo(() => painted(ash ? shade(wall, 1 - ash * 0.25) : wall, [1, 1], 300), [wall, ash]);
  const H = ruin ? h * (0.45 + r() * 0.3) : h;
  const wins: JSX.Element[] = [];
  for (let f = 0; f < 2; f++)
    for (let i = 0; i < 3; i++) {
      const y = 1.6 + f * 3.1, x = -w / 3 + (i * w) / 3;
      if (ruin && y + 1 > H) continue;
      if (f === 0 && i === 1) continue;
      wins.push(
        <group key={f + "-" + i} position={[x, y, d / 2]}>
          <Box size={[0.9, 1.7, 0.1]} pos={[0, 0, 0.02]} color={ruin ? "#1a1614" : "#3a2a22"} />
          {ruin ? null : <Box size={[0.42, 1.7, 0.08]} pos={[-0.68, 0, 0.08]} color={sh} />}
          {ruin ? null : <Box size={[0.42, 1.7, 0.08]} pos={[0.68, 0, 0.08]} color={sh} />}
        </group>,
      );
    }
  return (
    <group position={pos} rotation={[0, rotY, 0]}>
      <Box size={[w, H, d]} pos={[0, H / 2, 0]} map={wallMap} />
      {ruin ? (
        <group>
          {[-1, 0, 1].map((i) => <Box key={i} size={[w / 3, 0.6 + r() * 1.4, d]} pos={[(i * w) / 3, H + 0.3, 0]} rot={[0, 0, (r() - 0.5) * 0.4]} color="#8a847c" />)}
          <Box size={[w * 1.2, 0.5, 2]} pos={[0, 0.25, d / 2 + 1]} rot={[0.1, 0.1, 0]} color="#5a5450" />
        </group>
      ) : (
        <group>
          <Box size={[w + 0.3, 0.3, d + 0.3]} pos={[0, h + 0.05, 0]} color="#f4ece0" />
          <Roof w={w} d={d} h={2.0} pos={[0, h + 0.2, 0]} over={0.4} map={roofRed(0.9 + r() * 0.2)} />
          {ash ? <Roof w={w} d={d} h={2.02} pos={[0, h + 0.24, 0]} over={0.42} color="#a8a098" /> : null}
          {/* balcony */}
          <Box size={[w * 0.9, 0.12, 0.9]} pos={[0, 3.35, d / 2 + 0.45]} color="#f4ece0" />
          {Array.from({ length: 13 }).map((_, i) => <Box key={"b" + i} size={[0.05, 0.8, 0.05]} pos={[-w * 0.43 + (i * w * 0.86) / 12, 3.8, d / 2 + 0.86]} color="#2a2a2a" shadow={false} />)}
          <Box size={[w * 0.9, 0.06, 0.06]} pos={[0, 4.2, d / 2 + 0.86]} color="#2a2a2a" />
          <Box size={[1.2, 2.3, 0.12]} pos={[0, 1.15, d / 2 + 0.02]} color={sh} />
          <Box size={[1.6, 0.2, 0.3]} pos={[0, 2.45, d / 2 + 0.1]} color="#f4ece0" />
        </group>
      )}
      {wins}
    </group>
  );
};

export const Palm: React.FC<{ pos: V3; h?: number; seed?: number; burnt?: boolean }> = ({ pos, h = 7, seed = 1, burnt }) => {
  const t = useT();
  const r = rng(seed);
  const lean = (r() - 0.5) * 0.3;
  const segs = 7;
  return (
    <group position={pos} rotation={[0, r() * 6, 0]}>
      {Array.from({ length: segs }).map((_, i) => (
        <Cyl key={i} r={0.28 - i * 0.02} r2={0.25 - i * 0.02} h={h / segs + 0.05} pos={[Math.sin((i / segs) * 1.2) * lean * h, (i + 0.5) * (h / segs), 0]} rot={[0, 0, -lean * 0.8]} color={burnt ? "#2a2420" : i % 2 ? "#8a6a4a" : "#7a5a3a"} />
      ))}
      {burnt ? null : Array.from({ length: 8 }).map((_, i) => {
        const a = (i / 8) * Math.PI * 2, sw = Math.sin(t * 1.4 + i) * 0.05;
        return (
          <group key={"l" + i} position={[Math.sin(1.2) * lean * h, h, 0]} rotation={[0, a, 0]}>
            <mesh position={[1.4, -0.35, 0]} rotation={[0, 0, -0.45 + sw]} castShadow>
              <boxGeometry args={[3.0, 0.08, 0.7]} />
              <meshStandardMaterial color={i % 2 ? "#3a8a3a" : "#2f7a35"} roughness={0.9} />
            </mesh>
          </group>
        );
      })}
    </group>
  );
};

export const Boat: React.FC<{ pos: V3; rotY?: number; size?: number; color?: string; steam?: boolean; children?: React.ReactNode }> = ({ pos, rotY = 0, size = 1, color = "#2a3a5a", steam, children }) => {
  const t = useT();
  const bob = Math.sin(t * 1.3 + pos[0]) * 0.12;
  return (
    <group position={[pos[0], pos[1] + bob, pos[2]]} rotation={[Math.sin(t + pos[2]) * 0.02, rotY, 0]} scale={size}>
      <Box size={[8, 1.6, 2.6]} pos={[0, 0.3, 0]} color={color} />
      <Box size={[1.6, 1.6, 1.8]} pos={[4.6, 0.3, 0]} rot={[0, Math.PI / 4, 0]} color={color} />
      <Box size={[8.4, 0.2, 2.8]} pos={[0.2, 1.15, 0]} map={planks("#b88a5a", [2, 1])} />
      {steam ? (
        <group>
          <Box size={[3, 1.4, 2]} pos={[-0.5, 1.95, 0]} color="#f2ece0" />
          <Cyl r={0.45} h={2.6} pos={[0, 3.8, 0]} color="#1a1a1e" />
          <Cyl r={0.48} h={0.5} pos={[0, 4.9, 0]} color="#c0262c" />
        </group>
      ) : (
        <group>
          <Cyl r={0.1} h={7} pos={[0.5, 4.6, 0]} color="#5a3a22" />
          <mesh position={[-0.9, 4.6, 0]}><planeGeometry args={[2.6, 5]} /><meshStandardMaterial color="#f4ecd8" side={THREE.DoubleSide} /></mesh>
        </group>
      )}
      <group position={[0, 1.25, 0]}>{children}</group>
    </group>
  );
};

export const SeaAndQuay: React.FC<{ ruin?: boolean }> = ({ ruin }) => (
  <group>
    <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.6, 70]} receiveShadow>
      <planeGeometry args={[400, 120]} />
      <meshStandardMaterial map={water(ruin ? "#4a5a62" : "#1f7a9a", [20, 8])} roughness={0.35} />
    </mesh>
    <Box size={[200, 1.2, 1.2]} pos={[0, -0.3, 9.6]} color={ruin ? "#7a746c" : "#c8b8a0"} />
  </group>
);

// The whole town: two rows of houses facing the sea, a street, the quay, palms, boats; the volcano behind.
export const Town: React.FC<{ ruin?: boolean; ash?: number; boats?: boolean; sign?: boolean; smoke?: number; glow?: number; children?: React.ReactNode }> = ({ ruin, ash = 0, boats = true, sign = true, smoke = 1, glow = 0, children }) => {
  const houses: JSX.Element[] = [];
  for (let i = -7; i <= 7; i++) {
    houses.push(<CHouse key={"a" + i} pos={[i * 7, 0, -6]} seed={i + 40} h={i % 3 === 0 ? 8.4 : 7} ruin={ruin} ash={ash} />);
    houses.push(<CHouse key={"b" + i} pos={[i * 7 + 3.5, 1.5, -18]} seed={i + 80} h={i % 2 ? 8.4 : 7} ruin={ruin} ash={ash} />);
    houses.push(<CHouse key={"c" + i} pos={[i * 7, 3.5, -30]} seed={i + 120} h={7} ruin={ruin} ash={ash} />);
  }
  return (
    <group>
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, -90.4]} receiveShadow>
        <planeGeometry args={[260, 200]} />
        <meshStandardMaterial map={cobbles(ruin ? "#8a847c" : ash ? "#a89e90" : "#c8b498", [150, 115])} roughness={1} />
      </mesh>
      <Box size={[200, 1.5, 12]} pos={[0, 0.75, -18]} color={ruin ? "#7a746c" : "#b8a488"} />
      <Box size={[200, 3.5, 12]} pos={[0, 1.75, -30]} color={ruin ? "#7a746c" : "#b8a488"} />
      {houses}
      {[-42, -28, -14, 0, 14, 28, 42].map((x, i) => <Palm key={"p" + x} pos={[x + 3.5, 0, 6]} seed={i + 3} burnt={ruin} />)}
      <SeaAndQuay ruin={ruin} />
      {boats && !ruin ? (
        <group>
          <Boat pos={[-18, 0, 22]} rotY={0.2} color="#7a2a2a" />
          <Boat pos={[10, 0, 30]} rotY={-0.3} steam color="#1f2a3a" size={1.3} />
          <Boat pos={[32, 0, 20]} rotY={0.5} color="#2a5a4a" />
          <Boat pos={[-40, 0, 36]} rotY={0.1} steam color="#2a2a3a" size={1.5} />
          <Boat pos={[-7, 0, 15.5]} rotY={0.05} color="#c0662a" size={0.7} />
          <Boat pos={[4, 0, 18]} rotY={-0.15} color="#2a6a9a" size={0.75} />
          <Boat pos={[-26, 0, 15]} rotY={0.3} color="#e8d8b8" size={0.7} />
        </group>
      ) : null}
      {sign ? <Sign lines={["SAINT-PIERRE"]} pos={[6, 3.4, 4.2]} w={6.4} h={1.6} bg="#f4ecd8" fg="#1d3a6a" /> : null}
      {sign ? <Box size={[0.2, 3.4, 0.2]} pos={[3.4, 1.7, 4.1]} color="#3a2416" /> : null}
      {sign ? <Box size={[0.2, 3.4, 0.2]} pos={[8.6, 1.7, 4.1]} color="#3a2416" /> : null}
      <Volcano smoke={smoke} glow={glow} />
      {ash ? <Snow count={2600} area={[70, 24, 50]} center={[0, 0, 0]} speed={0.7} size={0.12} color="#5a5450" opacity={0.85} /> : null}
      {children}
    </group>
  );
};

// ---------- the prison and the cachot ----------
const stone = (k = 1) => bricks(shade("#8a8274", k), [1, 1], "#4a443c");
export const Cachot: React.FC<{ open?: number; light?: string; ruin?: boolean; plaque?: boolean }> = ({ open = 0, light, ruin, plaque = true }) => (
  <group>
    {/* earth heaped on the sides and back: half underground */}
    <mesh position={[0, 0, -2.0]} scale={[3.2, 2.5, 3.5]} receiveShadow castShadow>
      <sphereGeometry args={[1, 28, 16, 0, Math.PI * 2, 0, Math.PI / 2]} />
      <meshStandardMaterial color={ruin ? "#6a645c" : "#6a7a3a"} roughness={1} />
    </mesh>
    {/* thick stone block + vault */}
    <Box size={[3.4, 2.6, 4.8]} pos={[0, 1.3, -0.8]} map={stone(ruin ? 0.8 : 1)} />
    <mesh position={[0, 2.6, -0.8]} rotation={[Math.PI / 2, 0, 0]} castShadow receiveShadow>
      <cylinderGeometry args={[1.7, 1.7, 4.8, 24, 1, false, Math.PI / 2, Math.PI]} />
      <meshStandardMaterial map={stone(ruin ? 0.75 : 0.95)} roughness={1} />
    </mesh>
    {/* door: thick planks with iron bands and a slit; opens around its left hinge */}
    <group position={[-0.55, 0, 1.62]} rotation={[0, -open * 1.6, 0]}>
      <Box size={[1.1, 1.95, 0.16]} pos={[0.55, 0.98, 0]} map={planks("#4a2e1a", [1, 1], true)} />
      {[0.4, 1.5].map((y) => <Box key={y} size={[1.12, 0.1, 0.2]} pos={[0.55, y, 0]} color="#2a2a2e" />)}
      <Box size={[0.5, 0.06, 0.2]} pos={[0.55, 1.68, 0.01]} color={light ?? "#0a0808"} emissive={light} emissiveIntensity={light ? 2 : 0} shadow={false} />
    </group>
    <Box size={[1.4, 0.25, 0.3]} pos={[0, 2.05, 1.6]} color="#5a544c" />
    {open > 0 ? <mesh position={[0, 0.98, 1.612]}><planeGeometry args={[1.1, 1.95]} /><meshBasicMaterial color="#050303" /></mesh> : null}
    {plaque && !ruin ? <Sign lines={["CACHOT"]} pos={[0, 2.5, 1.64]} w={1.3} h={0.38} bg="#2a2420" fg="#e8dcc0" /> : null}
    {/* steps down to the door */}
    {[0, 1, 2].map((i) => <Box key={"s" + i} size={[1.6, 0.15, 0.4]} pos={[0, 0.075 + 0.0, 2.0 + i * 0.4]} color="#7a7268" />)}
  </group>
);

export const Prison: React.FC<{ ruin?: boolean; ash?: number; door?: number; children?: React.ReactNode; volcano?: boolean }> = ({ ruin, ash = 0, door = 0, children, volcano = true }) => (
  <group>
    <Ground map={cobbles(ruin ? "#8a847c" : "#a89a84", [70, 70])} size={200} />
    {/* back building with barred windows */}
    <Box size={[22, ruin ? 3.6 : 7, 5]} pos={[0, ruin ? 1.8 : 3.5, -9]} map={painted(ruin ? "#8a8278" : "#d8c8a8", [3, 1], 400)} />
    {ruin ? null : <Roof w={22} d={5} h={1.6} pos={[0, 7, -9]} over={0.3} map={roofRed()} />}
    {ruin ? null : [-8, -4, 4, 8].map((x) => (
      <group key={x} position={[x, 4.6, -6.48]}>
        <Box size={[1.1, 1.3, 0.05]} color="#1a1414" />
        {[-0.35, -0.12, 0.12, 0.35].map((bx) => <Box key={bx} size={[0.06, 1.3, 0.1]} pos={[bx, 0, 0.05]} color="#2a2a2e" />)}
      </group>
    ))}
    {ruin ? null : <Sign lines={["PRISON"]} pos={[0, 5.4, -6.42]} w={3} h={0.7} bg="#f4ecd8" fg="#3a2416" />}
    {/* side walls */}
    <Box size={[0.8, ruin ? 2.2 : 4, 20]} pos={[-11, ruin ? 1.1 : 2, 1]} map={stone()} />
    <Box size={[0.8, ruin ? 1.6 : 4, 20]} pos={[11, ruin ? 0.8 : 2, 1]} map={stone()} />
    <group position={[3, 0, -0.5]}><Cachot open={door} ruin={ruin} /></group>
    {volcano ? <Volcano smoke={ruin ? 0.5 : 1} /> : null}
    {ruin ? <Palm pos={[-7, 0, 6]} burnt seed={4} /> : <Palm pos={[-7, 0, 6]} seed={4} />}
    {ruin ? Array.from({ length: 14 }).map((_, i) => { const r = rng(i + 3); const x = (r() - 0.5) * 18, z = (r() - 0.3) * 12; if (x > -1 && x < 8 && z > -1) return null; return <Box key={"rb" + i} size={[0.5 + r(), 0.3 + r() * 0.5, 0.5 + r()]} pos={[x, 0.2, z]} rot={[r(), r() * 3, r()]} color="#6a645c" />; }) : null}
    {ash ? <Snow count={1500} area={[30, 14, 30]} center={[0, 0, 0]} speed={0.6} size={0.08} color="#5a5450" opacity={0.85} /> : null}
    {children}
  </group>
);

// Inside the cachot: a tiny stone room, the door with its slit on the far wall (camera looks at -z).
export const CellInside: React.FC<{ glow?: string; slit?: number; smoke?: boolean }> = ({ glow = "#fff0c8", slit = 1, smoke }) => {
  const t = useT();
  const flick = glow === "#ff6a20" ? 0.75 + Math.sin(t * 17) * 0.15 + Math.sin(t * 5) * 0.1 : 1;
  return (
    <group>
      <Ground map={stone(0.6)} size={12} />
      <Box size={[3.0, 2.8, 0.4]} pos={[0, 1.4, -2.2]} map={stone(0.7)} />
      <Box size={[0.4, 2.8, 5]} pos={[-1.4, 1.4, 0]} map={stone(0.65)} />
      <Box size={[0.4, 2.8, 5]} pos={[1.4, 1.4, 0]} map={stone(0.6)} />
      <Box size={[3.0, 0.4, 5]} pos={[0, 2.9, 0]} map={stone(0.5)} />
      <Box size={[3.0, 2.8, 0.4]} pos={[0, 1.4, 2.5]} map={stone(0.6)} />
      {/* the door + the slit of light */}
      <Box size={[1.1, 1.95, 0.12]} pos={[0.2, 0.98, -1.98]} map={planks("#3a2414", [1, 1], true)} />
      {[0.4, 1.5].map((y) => <Box key={y} size={[1.12, 0.1, 0.16]} pos={[0.2, y, -1.95]} color="#1a1a1e" />)}
      <mesh position={[0.2, 1.68, -1.9]}><planeGeometry args={[0.5, 0.07]} /><meshBasicMaterial color={glow} toneMapped={false} /></mesh>
      <mesh position={[0.2, 1.4, -1.1]} rotation={[-0.35, 0, 0]} layers={LAYER_FX}>
        <planeGeometry args={[0.5 * slit, 1.6]} />
        <meshBasicMaterial color={glow} transparent opacity={0.1 * slit * flick} depthWrite={false} side={THREE.DoubleSide} />
      </mesh>
      <pointLight position={[0.2, 1.6, -1.6]} intensity={3 * slit * flick} distance={6} decay={1.5} color={glow} />
      {/* bench */}
      <Box size={[0.6, 0.45, 2.2]} pos={[-0.85, 0.22, -0.2]} color="#4a3a2a" />
      {smoke ? <Snow count={500} area={[2.6, 2.8, 4]} center={[0, 0, 0]} speed={-0.3} size={0.05} color="#ff9a5a" opacity={0.6} /> : null}
    </group>
  );
};

// ---------- small sets ----------
export const Rock1000: React.FC = () => {
  const t = useT();
  const tex = useMemo(() => canvasTex(1024, 1024, (g) => {
    g.fillStyle = "#000"; g.fillRect(0, 0, 1024, 1024);
    g.textAlign = "center"; g.textBaseline = "middle";
    g.fillStyle = "#ffb050"; g.shadowColor = "#ff5a10"; g.shadowBlur = 40;
    g.font = "900 330px Georgia, serif"; g.fillText("1000", 512, 380);
    g.font = "900 260px Georgia, serif"; g.fillText("°C", 512, 700);
  }), []);
  return (
    <group>
      <Ground map={cobbles("#3a2a24", [10, 10])} size={80} />
      <mesh position={[0, 2.2, -1]} scale={[4.2, 2.8, 1.6]} castShadow receiveShadow>
        <dodecahedronGeometry args={[1, 1]} />
        <meshStandardMaterial color="#2a2220" roughness={1} flatShading />
      </mesh>
      <mesh position={[0, 2.3, 0.62]}>
        <planeGeometry args={[3.2, 3.2]} />
        <meshBasicMaterial map={tex} transparent blending={THREE.AdditiveBlending} toneMapped={false} opacity={0.85 + Math.sin(t * 6) * 0.1} />
      </mesh>
      {[-5, -2.5, 3, 5.5].map((x, i) => <Fire key={i} pos={[x, 0, 1.5 + (i % 2)]} scale={1.4} light={10} />)}
      <Snow count={700} area={[16, 8, 10]} center={[0, 0, 1]} speed={-0.8} size={0.08} color="#ff8a3a" opacity={0.9} />
    </group>
  );
};

// Night: the prison's outer wall, a moon, the town's lanterns behind.
export const WallNight: React.FC<{ children?: React.ReactNode; party?: boolean }> = ({ children, party }) => {
  const t = useT();
  return (
    <group>
      <Ground map={cobbles("#6a6a7a", [60, 60])} size={160} />
      {party ? null : <Box size={[30, 3.4, 0.8]} pos={[0, 1.7, -2]} map={stone(0.9)} />}
      {party ? null : <Box size={[30.2, 0.25, 1.0]} pos={[0, 3.5, -2]} color="#7a7268" />}
      <mesh position={[18, 40, -90]} layers={LAYER_FX}><sphereGeometry args={[5, 24, 16]} /><meshBasicMaterial color="#fff6d8" fog={false} /></mesh>
      {Array.from({ length: 5 }).map((_, i) => <CHouse key={i} pos={[-16 + i * 8, 0, party ? -8 : -14]} seed={i + 7} />)}
      {/* strings of lanterns */}
      {Array.from({ length: party ? 24 : 0 }).map((_, i) => {
        const x = -12 + i, y = 4.2 - Math.sin(((i % 12) / 11) * Math.PI) * 0.8;
        const c = ["#ff5a3a", "#ffd23a", "#3ad06a", "#3a9aff"][i % 4];
        return <mesh key={"lan" + i} position={[x, y, i < 12 ? -3 : -1]} layers={LAYER_FX}><sphereGeometry args={[0.18, 12, 8]} /><meshBasicMaterial color={c} toneMapped={false} /></mesh>;
      })}
      {party ? <pointLight position={[0, 4, 1]} intensity={40 + Math.sin(t * 9) * 4} distance={18} decay={1.6} color="#ffb060" /> : null}
      {party ? <Fire pos={[5, 0, -4]} scale={1.2} light={12} /> : null}
      {children}
    </group>
  );
};

// Hospital room: bed, window onto the sea
export const Infirmary: React.FC<{ children?: React.ReactNode }> = ({ children }) => (
  <group>
    <Ground map={planks("#b88a5a", [4, 4])} size={30} />
    <Box size={[14, 5, 0.3]} pos={[0, 2.5, -3]} map={painted("#e8e0c8", [2, 1], 300)} />
    <Box size={[0.3, 5, 10]} pos={[-5, 2.5, 1]} map={painted("#e2d8bc", [2, 1], 300)} />
    <Window w={2} h={2.2} pos={[2.2, 2.6, -2.84]} lit={false} panes={[2, 2]} frame="#f4f1ea" />
    <Box size={[2.2, 0.5, 1.2]} pos={[-1.8, 0.65, -1.6]} color="#f4f1ea" />
    <Box size={[2.2, 0.15, 1.2]} pos={[-1.8, 0.95, -1.6]} color="#cfd8e8" />
    {[[-2.8, -2.1], [-0.8, -2.1], [-2.8, -1.1], [-0.8, -1.1]].map(([x, z], i) => <Cyl key={i} r={0.05} h={0.5} pos={[x, 0.25, z]} color="#5a5a62" />)}
    <Box size={[0.1, 1.4, 1.2]} pos={[-2.9, 1.1, -1.6]} color="#5a5a62" />
    <pointLight position={[1, 3.5, 1]} intensity={18} distance={12} decay={1.6} color="#fff0d8" />
    {children}
  </group>
);

// The circus: striped big top + a poster wall
const stripes = () => canvasTex(1024, 256, (g) => { for (let i = 0; i < 16; i++) { g.fillStyle = i % 2 ? "#f4ecd8" : "#c0262c"; g.fillRect(i * 64, 0, 64, 256); } });
export const posterTex = () => canvasTex(768, 1024, (g) => {
  g.fillStyle = "#f2e2b4"; g.fillRect(0, 0, 768, 1024);
  g.strokeStyle = "#b2222a"; g.lineWidth = 22; g.strokeRect(24, 24, 720, 976);
  g.fillStyle = "#b2222a"; g.textAlign = "center"; g.textBaseline = "middle";
  g.font = "900 64px Georgia, serif"; g.fillText("BARNUM & BAILEY", 384, 110);
  g.fillStyle = "#1d2a52"; g.font = "italic 700 40px Georgia, serif"; g.fillText("le plus grand spectacle du monde", 384, 175);
  // the man, drawn simple
  g.fillStyle = "#6e4228"; g.beginPath(); g.arc(384, 380, 95, 0, 7); g.fill(); g.lineWidth = 10; g.strokeStyle = "#161212"; g.stroke();
  g.fillStyle = "#161212"; g.beginPath(); g.ellipse(350, 370, 10, 14, 0, 0, 7); g.ellipse(418, 370, 10, 14, 0, 0, 7); g.fill();
  g.beginPath(); g.arc(384, 400, 30, 0.2, Math.PI - 0.2); g.lineWidth = 7; g.stroke();
  g.fillStyle = "#e6d3a4"; g.beginPath(); g.roundRect(290, 470, 188, 170, 60); g.fill(); g.lineWidth = 10; g.stroke();
  g.fillStyle = "#b2222a"; g.font = "900 82px Georgia, serif"; g.fillText("LE SEUL", 384, 730);
  g.fillText("SURVIVANT", 384, 815);
  g.fillStyle = "#1d2a52"; g.font = "italic 700 36px Georgia, serif"; g.fillText("de la cité silencieuse de la mort", 384, 900);
  g.font = "700 30px Georgia, serif"; g.fillText("SAINT-PIERRE · 1902", 384, 950);
});
export const Circus: React.FC<{ children?: React.ReactNode; poster?: boolean; night?: boolean }> = ({ children, poster = true, night }) => {
  const st = useMemo(stripes, []);
  const pt = useMemo(posterTex, []);
  const t = useT();
  return (
    <group>
      <Ground map={cobbles("#9a8a6a", [70, 70])} size={200} />
      <group position={[0, 0, -16]}>
        <mesh position={[0, 2.5, 0]} castShadow receiveShadow><cylinderGeometry args={[9, 9, 5, 32, 1, true]} /><meshStandardMaterial map={st} side={THREE.DoubleSide} /></mesh>
        <mesh position={[0, 8, 0]} castShadow><coneGeometry args={[10, 6, 32, 1, true]} /><meshStandardMaterial map={st} side={THREE.DoubleSide} /></mesh>
        <Cyl r={0.12} h={3} pos={[0, 12, 0]} color="#3a2416" />
        <mesh position={[0.7, 13, 0]}><planeGeometry args={[1.2, 0.7]} /><meshStandardMaterial color="#c0262c" side={THREE.DoubleSide} /></mesh>
        <mesh position={[0, 1.6, 9.02]}><planeGeometry args={[2.4, 3.2]} /><meshStandardMaterial color="#2a1410" /></mesh>
      </group>
      {Array.from({ length: 16 }).map((_, i) => (
        <mesh key={i} position={[-14 + i * 1.9, 6.2 - Math.sin((i / 15) * Math.PI) * 1.2, -4]} layers={LAYER_FX}><sphereGeometry args={[0.16, 10, 8]} /><meshBasicMaterial color={["#ffd23a", "#ff5a3a", "#ffffff"][i % 3]} toneMapped={false} /></mesh>
      ))}
      {poster ? (
        <group position={[-3.2, 0, -1]}>
          <Box size={[4.2, 4.6, 0.4]} pos={[0, 2.3, 0]} map={bricks("#a85a3a", [1, 1])} />
          <mesh position={[0, 2.5, 0.21]} rotation={[0, 0, 0.02]}><planeGeometry args={[2.6, 3.47]} /><meshStandardMaterial map={pt} roughness={0.9} emissive="#ffffff" emissiveMap={pt} emissiveIntensity={0.15} /></mesh>
        </group>
      ) : null}
      {night ? <pointLight position={[0, 6, 4]} intensity={60 + Math.sin(t * 7) * 5} distance={24} decay={1.6} color="#ffc070" /> : null}
      {children}
    </group>
  );
};
