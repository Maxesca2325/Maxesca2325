// Episode 2 cast: Saint-Pierre, Martinique, 1902.
import type { ToonSpec } from "../engine/draw";
const S = ["#8a5634", "#6e4228", "#a8714a", "#5a3420", "#c48a5e", "#7a4a2e"]; // skin tones
export const C: Record<string, ToonSpec> = {
  // Louis-Auguste Cyparis: young worker, straw-coloured shirt, rolled sleeves, no hat
  cyparis: { hat: "none", coat: "#e6d3a4", vest: "#7a4a2a", hair: "#1a120e", skin: S[1], scarf: "#c0392b" },
  cyparisHurt: { hat: "none", coat: "#b9ab90", vest: "#5a3a26", hair: "#1a120e", skin: S[1], bandage: true },
  cyparisStar: { hat: "none", coat: "#c0392b", vest: "#f2c64b", hair: "#1a120e", skin: S[1], buttons: "#f2c64b", bandage: true },
  guard: { hat: "kepi", hatColor: "#1d2a52", band: "#c0262c", coat: "#1f2a52", buttons: "#e9c35a", hair: "#2a1e16", skin: S[4], moustache: true },
  rival: { hat: "flatcap", hatColor: "#4a3a2a", coat: "#3a5a7a", vest: "#d8c39a", hair: "#1a120e", skin: S[3] },
  gent: { hat: "boater", hatColor: "#e8d49a", band: "#1d1d1d", coat: "#f0ece0", vest: "#3a5a8a", hair: "#2a1e16", skin: S[2], moustache: true },
  gent2: { hat: "top", hatColor: "#1e1e24", coat: "#2f3b5c", vest: "#e9e4d8", hair: "#5a3a26", skin: "#f1d2b6", whiskers: true },
  lady: { hat: "madras", hatColor: "#d9452b", band: "#f2c64b", coat: "#f2e6c8", skirt: "#3a7a5a", skin: S[0], hair: "#1a120e" },
  lady2: { hat: "madras", hatColor: "#f2c64b", band: "#2f7a4a", coat: "#ffffff", skirt: "#c0392b", skin: S[4], hair: "#1a120e" },
  lady3: { hat: "madras", hatColor: "#3a6ab0", band: "#ffffff", coat: "#f4d6a0", skirt: "#7a3a8a", skin: S[3], hair: "#1a120e", height: 0.95 },
  fisher: { hat: "boater", hatColor: "#d9c58a", coat: "#2f6a8a", vest: "#e6d3a4", hair: "#1a120e", skin: S[5] },
  kid: { hat: "none", coat: "#f2c64b", hair: "#1a120e", skin: S[2], height: 0.62, wide: 0.95 },
  dancer: { hat: "boater", hatColor: "#e8d49a", band: "#c0392b", coat: "#ffffff", vest: "#c0392b", hair: "#1a120e", skin: S[0] },
  rescuer1: { hat: "boater", hatColor: "#cdb98a", coat: "#7a6a4a", vest: "#4a3a2a", hair: "#1a120e", skin: S[3], moustache: true },
  rescuer2: { hat: "flatcap", hatColor: "#5a4a3a", coat: "#4a5a3a", vest: "#c9b48a", hair: "#1a120e", skin: S[0] },
  doctor: { hat: "none", coat: "#f4f1ea", vest: "#9aa8b8", hair: "#d9d4c8", skin: "#f1d2b6", glasses: true, moustache: true },
  ringmaster: { hat: "top", hatColor: "#1c1c22", band: "#c0262c", coat: "#b2222a", vest: "#f2c64b", buttons: "#f2c64b", hair: "#3a2a1e", skin: "#f1d2b6", moustache: true },
};
