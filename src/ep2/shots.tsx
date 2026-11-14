// Episode 2 shot list: one entry per voice line (episodes/ep2/shots.json).
import React from "react";
import * as THREE from "three";
import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import type { CamKeys, Look } from "../engine/Stage";
import { Toon } from "../engine/Toon";
import { Ground } from "../engine/kit";
import { water } from "../engine/tex";
import { Town, Prison, CellInside, Cloud, Rock1000, WallNight, Infirmary, Circus, Boat, Volcano,
  tropLook, ashLook, eruptLook, burnLook, nightLook, ruinLook, cellLook } from "./sets";
import { C } from "./cast";

export type Shot = { look: Look; cam: CamKeys; focus: number; Body: React.FC<{ dur: number }> };
const useT = () => { const f = useCurrentFrame(); const { fps } = useVideoConfig(); return f / fps; };
const B = (fn: (t: number, dur: number) => React.ReactNode): React.FC<{ dur: number }> => ({ dur }) => { const t = useT(); return <>{fn(t, dur / 30)}</>; };
const ramp = (t: number, d: number, a: number, b: number) => interpolate(t, [0, d], [a, b], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

const trop = tropLook(), ash = ashLook(), erupt = eruptLook(), burn = burnLook(), night = nightLook(), ruin = ruinLook();
const cellDark = cellLook("#8a6a5a"), cellFire = { ...cellLook("#ff6a20"), exposure: 1.45 };
const DOOR: [number, number, number] = [3, 0, 1.12]; // the cachot's door in the Prison set

const Sea: React.FC<{ children?: React.ReactNode }> = ({ children }) => (
  <group>
    {children}
    <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.6, 0]} receiveShadow>
      <planeGeometry args={[400, 400]} />
      <meshStandardMaterial map={water("#1f7a9a", [30, 30])} roughness={0.35} />
    </mesh>
    <Volcano smoke={0.6} />
  </group>
);

export const SHOTS: Record<number, Shot> = {
  // En 1902, une ville française de 28 000 habitants
  1: { look: trop, focus: 50, cam: { from: [34, 30, 66], to: [20, 13, 42], lookFrom: [0, 12, -40], lookTo: [0, 8, -30], fov: 55 },
    Body: B(() => <Town />) },
  // a disparu en moins d'une minute.
  2: { look: erupt, focus: 60, cam: { from: [0, 18, 78], to: [0, 17, 72], lookFrom: [0, 14, -30], fov: 58, sway: 3 },
    Body: B((t, d) => <Town glow={1} smoke={2}><Cloud k={ramp(t, d, 0.55, 1)} /></Town>) },
  // Et l'un des seuls survivants… c'était le prisonnier.
  3: { look: ruin, focus: 3.6, cam: { from: [4.6, 1.6, 6.8], to: [3.9, 1.6, 5.5], lookFrom: [3, 1.5, 1.8], fov: 50 },
    Body: B(() => (
      <Prison ruin ash={1} door={1}>
        <Toon spec={C.cyparisHurt} pose={{ eyes: "wide", mouth: "o", armL: "shrug", armR: "shrug" }} pos={[3, 0, 2.3]} />
      </Prison>
    )) },
  // Ça se passe en Martinique, à Saint-Pierre.
  4: { look: trop, focus: 7, cam: { from: [-7, 2.2, 8.5], to: [-3, 2.3, 8], lookFrom: [4, 2.8, -4], fov: 55 },
    Body: B(() => (
      <Town>
        <Toon spec={C.lady} pose={{ eyes: "happy", mouth: "smile" }} pos={[0, 0, 0]} path={{ from: [-2, 0, 1.5], to: [3, 0, 1.5], start: 0, end: 4 }} />
        <Toon spec={C.fisher} pose={{ armR: "wave", eyes: "happy", mouth: "grin" }} pos={[2.5, 0, 3.4]} seed={2} />
        <Toon spec={C.kid} pose={{ eyes: "dot", mouth: "grin" }} pos={[0, 0, 0]} path={{ from: [5, 0, 2.6], to: [1, 0, 3], start: 0, end: 3 }} h={1.75} seed={3} />
      </Town>
    )) },
  // On l'appelle le Petit Paris des Antilles.
  5: { look: trop, focus: 4.6, cam: { from: [9.6, 1.5, 5.6], to: [8.4, 1.7, 4.6], lookFrom: [5.4, 2.4, -1], fov: 54 },
    Body: B(() => (
      <Town>
        <Toon spec={C.gent2} pose={{ armR: "hold", prop: "cane", eyes: "happy", mouth: "smile" }} pos={[5.6, 0, 0.6]} seed={1} />
        <Toon spec={C.lady2} pose={{ armL: "hips", eyes: "happy", mouth: "smile" }} pos={[7.0, 0, 0.9]} seed={2} />
        <Toon spec={C.gent} pose={{ armL: "wave", eyes: "dot", mouth: "grin" }} pos={[3.6, 0, -1.6]} seed={3} />
      </Town>
    )) },
  // Un grand port, très riche, plein de bateaux.
  6: { look: trop, focus: 20, cam: { from: [-9, 3.0, 5], to: [-4, 3.6, 6.5], lookFrom: [-9, 1.5, 18], lookTo: [2, 2, 22], fov: 56 },
    Body: B(() => (
      <Town sign={false}>
        <Toon spec={C.fisher} pose={{ armR: "point", eyes: "happy", mouth: "grin" }} pos={[-5.2, 0, 8.4]} seed={4} />
      </Town>
    )) },
  // Juste au-dessus, il y a un volcan : la montagne Pelée.
  7: { look: trop, focus: 80, cam: { from: [-3.5, 2.5, 8], to: [-3.5, 13, 27], lookFrom: [-2, 5, -6], lookTo: [0, 32, -110], fov: 56 },
    Body: B(() => <Town smoke={1.3} />) },
  // Depuis des semaines, il gronde. Il crache de la cendre sur les toits.
  8: { look: ash, focus: 30, cam: { from: [-12, 15, 6], to: [-7, 13.5, 1], lookFrom: [0, 9, -30], lookTo: [0, 14, -50], fov: 56, sway: 4 },
    Body: B(() => <Town ash={1} smoke={2.2} />) },
  // Mais la vie continue.
  9: { look: ash, focus: 4.8, cam: { from: [2.5, 1.8, 6.8], to: [1.6, 1.8, 6], lookFrom: [-0.5, 1.7, 1], fov: 52 },
    Body: B(() => (
      <Town ash={1} smoke={2}>
        <Toon spec={C.lady3} pose={{ eyes: "happy", mouth: "smile" }} pos={[0, 0, 0]} path={{ from: [-3, 0, 1.4], to: [1, 0, 1.4], start: 0, end: 2 }} />
        <Toon spec={C.gent} pose={{ armR: "wave", eyes: "happy", mouth: "grin" }} pos={[0.8, 0, 0.2]} seed={5} />
      </Town>
    )) },
  // Dans la prison de la ville, il y a un jeune ouvrier : Louis-Auguste Cyparis.
  10: { look: trop, focus: 4.6, cam: { from: [-3.4, 1.9, 8], to: [-2.6, 1.75, 6.8], lookFrom: [-2.0, 1.7, 2], fov: 50 },
    Body: B(() => (
      <Prison>
        <Toon spec={C.cyparis} pose={{ armL: "cross", armR: "cross", eyes: "half", mouth: "flat" }} pos={[-3.0, 0, 2.6]} />
        <Toon spec={C.guard} pose={{ armL: "hips", armR: "hips", eyes: "angry", mouth: "flat" }} pos={[-1.0, 0, 2.0]} seed={2} h={1.85} />
      </Prison>
    )) },
  // Il est là pour une bagarre. Un coup de couteau.
  11: { look: trop, focus: 4, cam: { from: [1.0, 1.6, 6.2], to: [0.3, 1.6, 5.3], lookFrom: [0, 1.5, 1.4], fov: 50, sway: 2 },
    Body: B((t) => (
      <Town sign={false}>
        <Toon spec={C.cyparis} pose={{ armR: "point", armL: "hips", eyes: "angry", mouth: "open" }} pos={[-0.9, 0, 1.6]} />
        <Toon spec={C.rival} pose={{ armL: t > 1.4 ? "warm" : "point", armR: t > 1.4 ? "warm" : "hips", eyes: t > 1.4 ? "wide" : "angry", mouth: t > 1.4 ? "o" : "open" }} pos={[0.95, 0, 1.4]} seed={4} flip />
      </Town>
    )) },
  // Et une nuit, il fait le mur.
  12: { look: night, focus: 4.6, cam: { from: [2.4, 1.4, 5], to: [1.6, 1.7, 4.2], lookFrom: [0, 3.2, -2], fov: 52 },
    Body: B((t) => (
      <WallNight>
        <Toon spec={C.cyparis} pose={{ sit: true, armR: "wave", eyes: "happy", mouth: "grin" }} pos={[0, 3.62 + Math.max(0, Math.sin(t * 6)) * 0.05, -2]} />
      </WallNight>
    )) },
  // Il sort pour aller faire la fête.
  13: { look: night, focus: 4.5, cam: { from: [0.6, 1.7, 6], to: [0.2, 1.8, 5], lookFrom: [0, 1.6, -1], fov: 54 },
    Body: B((t) => {
      const beat = Math.floor(t * 3) % 2 === 0;
      return (
        <WallNight party>
          <Toon spec={C.cyparis} pose={{ armL: beat ? "up" : "wave", armR: beat ? "wave" : "up", eyes: "happy", mouth: "grin", walk: 0.6 }} pos={[0, 0, 0.5]} />
          <Toon spec={C.lady2} pose={{ armL: beat ? "wave" : "hips", armR: "up", eyes: "happy", mouth: "grin" }} pos={[-1.7, 0, -0.3]} seed={2} />
          <Toon spec={C.dancer} pose={{ armR: beat ? "up" : "wave", armL: "hips", eyes: "closed", mouth: "grin" }} pos={[1.8, 0, -0.5]} seed={3} />
          <Toon spec={C.lady} pose={{ armL: "up", armR: beat ? "up" : "wave", eyes: "happy", mouth: "open" }} pos={[0.6, 0, -2.4]} seed={4} />
        </WallNight>
      );
    }) },
  // Quand il revient, on le punit. Direction le cachot.
  14: { look: trop, focus: 5.5, cam: { from: [-2.6, 1.9, 8.6], to: [-1.6, 1.8, 7.4], lookFrom: [1.2, 1.4, 0.8], fov: 54 },
    Body: B(() => (
      <Prison>
        <Toon spec={C.guard} pose={{ armR: "point", armL: "hips", eyes: "angry", mouth: "open" }} pos={[-1.2, 0, 2.4]} h={1.85} seed={2} />
        <Toon spec={C.cyparis} pose={{ eyes: "sad", mouth: "frown", look: 1 }} pos={[0.6, 0, 2.6]} />
      </Prison>
    )) },
  // Le cachot, c'est une petite pièce en pierre, à moitié sous terre.
  15: { look: trop, focus: 8, cam: { from: [9, 3.4, 8.5], to: [6, 2.4, 7.2], lookFrom: [3, 1.3, -1], fov: 54 },
    Body: B(() => <Prison />) },
  // Des murs très épais. Pas de fenêtre.
  16: { look: trop, focus: 3.8, cam: { from: [6.4, 1.5, 3.4], to: [5.7, 1.7, 2.6], lookFrom: [4.2, 1.5, 0.4], lookTo: [4.4, 1.6, -0.6], fov: 50 },
    Body: B(() => <Prison />) },
  // Juste une fente dans la porte.
  17: { look: trop, focus: 2.2, cam: { from: [3.25, 1.95, 3.9], to: [3.1, 1.9, 3.1], lookFrom: [3, 1.95, 1.1], fov: 46 },
    Body: B(() => <Prison />) },
  // Le 8 mai 1902, vers huit heures du matin, le volcan explose.
  18: { look: erupt, focus: 90, cam: { from: [-8, 15, 54], to: [-4, 16, 47], lookFrom: [0, 26, -90], fov: 56, sway: 5 },
    Body: B((t, d) => <Town glow={1} smoke={2.5}><Cloud k={ramp(t, d, 0.02, 0.22)} /></Town>) },
  // Un nuage brûlant dévale la montagne.
  19: { look: erupt, focus: 70, cam: { from: [-34, 10, 24], to: [-30, 11, 19], lookFrom: [0, 16, -60], fov: 56, sway: 3 },
    Body: B((t, d) => <Town glow={1} smoke={2.5}><Cloud k={ramp(t, d, 0.22, 0.5)} /></Town>) },
  // Plus de mille degrés.
  20: { look: burn, focus: 6.5, cam: { from: [0, 2.6, 7.4], to: [0, 2.4, 6.2], lookFrom: [0, 2.3, 0], fov: 52, sway: 2 },
    Body: B(() => <Rock1000 />) },
  // Il traverse toute la ville en moins d'une minute.
  21: { look: erupt, focus: 30, cam: { from: [2, 11, 22], to: [0, 9.5, 17], lookFrom: [0, 9, -20], fov: 58, sway: 4 },
    Body: B((t, d) => <Town glow={1} smoke={2.5} sign={false}><Cloud k={ramp(t, d, 0.55, 0.78)} /></Town>) },
  // Presque tout le monde meurt sur le coup.
  22: { look: { ...erupt, exposure: 0.95, saturation: 1.0 }, focus: 60, cam: { from: [0, 14, 72], to: [0, 13, 66], lookFrom: [0, 10, -10], fov: 58, sway: 2 },
    Body: B((t, d) => <Town glow={1} smoke={2.5}><Cloud k={ramp(t, d, 0.86, 1)} /></Town>) },
  // Dans son cachot, Cyparis voit tout devenir noir.
  23: { look: cellDark, focus: 2.2, cam: { from: [0.8, 1.55, 2.0], to: [0.6, 1.45, 1.55], lookFrom: [-0.5, 1.0, -0.6], fov: 58 },
    Body: B((t, d) => (
      <group>
        <CellInside glow="#e8c890" slit={ramp(t, d, 1, 0.05)} />
        <Toon spec={C.cyparis} pose={{ sit: true, eyes: "wide", mouth: "o", look: 1, armL: "warm", armR: "warm" }} pos={[-0.85, 0.22, -0.3]} h={1.7} light={0.18} />
      </group>
    )) },
  // L'air devient brûlant.
  24: { look: cellFire, focus: 2.0, cam: { from: [0.7, 1.5, 1.7], to: [0.5, 1.45, 1.35], lookFrom: [-0.6, 1.0, -0.5], fov: 56, sway: 2 },
    Body: B(() => (
      <group>
        <CellInside glow="#ff6a20" smoke />
        <Toon spec={C.cyparis} pose={{ sit: true, eyes: "sad", mouth: "wavy", shiver: true, armL: "warm", armR: "warm" }} pos={[-0.85, 0.22, -0.3]} h={1.7} light={0.18} />
      </group>
    )) },
  // Ses bras, ses jambes, son dos sont brûlés.
  25: { look: cellFire, focus: 1.5, cam: { from: [0.2, 1.4, 1.4], to: [0.0, 1.38, 1.05], lookFrom: [-0.85, 1.05, -0.3], fov: 50 },
    Body: B(() => (
      <group>
        <CellInside glow="#ff6a20" smoke />
        <Toon spec={C.cyparisHurt} pose={{ sit: true, eyes: "sad", mouth: "frown", shiver: true, armL: "warm", armR: "warm" }} pos={[-0.85, 0.22, -0.3]} h={1.7} light={0.18} />
      </group>
    )) },
  // Mais il respire encore.
  26: { look: { ...cellDark, exposure: 1.7 }, focus: 1.2, cam: { from: [-0.1, 1.35, 0.95], to: [-0.2, 1.33, 0.8], lookFrom: [-0.85, 1.25, -0.3], fov: 46 },
    Body: B((t) => (
      <group>
        <CellInside glow="#ffb070" slit={0.6} />
        <Toon spec={C.cyparisHurt} pose={{ sit: true, eyes: t < 0.5 ? "closed" : "half", mouth: t < 0.5 ? "flat" : "o", armL: "warm", armR: "warm" }} pos={[-0.85, 0.22, -0.3]} h={1.7} light={0.2} />
      </group>
    )) },
  // Tu vois, ce cachot avait été construit pour une seule chose : que personne ne puisse en sortir.
  27: { look: trop, focus: 8, cam: { from: [-2, 3, 9], to: [8.5, 3, 7.5], lookFrom: [3, 1.4, -0.5], fov: 54 },
    Body: B(() => <Prison />) },
  // Des murs épais. Presque aucune ouverture.
  28: { look: trop, focus: 9, cam: { from: [3.5, 9, 7], to: [3.2, 10, 3.5], lookFrom: [3, 0.5, -1], fov: 52 },
    Body: B(() => <Prison />) },
  // Et la seule fente était tournée de l'autre côté du volcan.
  29: { look: trop, focus: 9, cam: { from: [9, 3.5, 10], to: [6, 3.2, 9], lookFrom: [3, 1.8, 1], lookTo: [0, 12, -60], fov: 60 },
    Body: B(() => <Prison />) },
  // Tout ce qui servait à l'enfermer… a gardé le pire de la chaleur dehors.
  30: { look: burn, focus: 6, cam: { from: [4.3, 1.3, 7.5], to: [3.6, 1.4, 6.2], lookFrom: [3, 1.8, -2], fov: 58, sway: 3 },
    Body: B((t, d) => <Prison ash={1}><Cloud k={ramp(t, d, 0.72, 0.8)} width={0.7} /></Prison>) },
  // Trois jours plus tard, des sauveteurs du village voisin l'entendent appeler.
  31: { look: ruin, focus: 5, cam: { from: [-4, 1.8, 8.5], to: [-2.4, 1.8, 7.4], lookFrom: [0.8, 1.5, 0.8], fov: 54 },
    Body: B((t) => (
      <Town ruin sign={false} smoke={0.6}>
        <Toon spec={C.rescuer1} pose={{ armR: "hold", prop: "shovel", eyes: t > 1.2 ? "wide" : "dot", mouth: t > 1.2 ? "o" : "flat", look: 1 }} pos={[0, 0, 0]} path={{ from: [-2.5, 0, 1.2], to: [-0.2, 0, 1.6], start: 0, end: 1.2 }} />
        <Toon spec={C.rescuer2} pose={{ armR: "point", eyes: "wide", mouth: "open", look: 1 }} pos={[1.4, 0, 0.6]} seed={2} />
      </Town>
    )) },
  // Ils dégagent la porte. Il est vivant.
  32: { look: ruin, focus: 4.6, cam: { from: [5.6, 1.7, 7.4], to: [4.6, 1.7, 6.2], lookFrom: [3, 1.4, 1.6], fov: 54 },
    Body: B((t, d) => (
      <Prison ruin door={ramp(t, d * 0.5, 0, 1)}>
        <Toon spec={C.rescuer1} pose={{ armR: "up", prop: "shovel", eyes: "happy", mouth: "grin" }} pos={[1.4, 0, 2.4]} />
        <Toon spec={C.rescuer2} pose={{ armL: "wave", eyes: "wide", mouth: "grin" }} pos={[4.7, 0, 2.6]} seed={2} />
        {t > d * 0.45 ? <Toon spec={C.cyparisHurt} pose={{ eyes: "half", mouth: "smile" }} pos={[0, 0, 0]} path={{ from: [3, 0, 1.3], to: [3, 0, 2.2], start: d * 0.45, end: d }} seed={3} /> : null}
      </Prison>
    )) },
  // On le soigne. On lui pardonne.
  33: { look: { ...trop, fog: "#e8e0c8", fogNear: 20, fogFar: 60 }, focus: 3.6, cam: { from: [-0.9, 1.8, 4.6], to: [-1.3, 1.75, 3.9], lookFrom: [-1.7, 1.3, -1.2], fov: 56 },
    Body: B((t) => (
      <Infirmary>
        <Toon spec={C.cyparisHurt} pose={{ sit: true, eyes: "happy", mouth: "smile" }} pos={[-1.9, 0.75, -1.6]} h={1.7} />
        <Toon spec={C.doctor} pose={{ armR: "hold", prop: "teacup", eyes: "happy", mouth: "smile" }} pos={[-3.0, 0, -0.5]} seed={2} />
        <Toon spec={C.gent2} pose={{ armR: t > 1 ? "point" : "hold", prop: "paper", eyes: "dot", mouth: "smile" }} pos={[-0.4, 0, -0.6]} seed={3} flip />
      </Infirmary>
    )) },
  // Et le célèbre cirque Barnum l'emmène en Amérique.
  34: { look: trop, focus: 9, cam: { from: [-6, 3.6, 9.5], to: [-3.5, 3.2, 7.5], lookFrom: [3.2, 2.6, 0.6], fov: 52 },
    Body: B(() => (
      <Sea>
        <Boat pos={[0, 0, 0]} steam size={1.2} color="#1f2a3a">
          <Toon spec={C.ringmaster} pose={{ armL: "wave", armR: "point", eyes: "happy", mouth: "grin" }} pos={[2.2, 0, 0.6]} seed={1} />
          <Toon spec={C.cyparisHurt} pose={{ armR: "wave", eyes: "wide", mouth: "smile" }} pos={[3.4, 0, 0.7]} seed={2} />
        </Boat>
      </Sea>
    )) },
  // Sur les affiches, on écrit : «Le seul être vivant qui a survécu à la cité silencieuse de la mort.»
  35: { look: trop, focus: 4.2, cam: { from: [-1.2, 2.2, 7.5], to: [-3.1, 2.5, 4.0], lookFrom: [-3.2, 2.5, -1], fov: 52 },
    Body: B(() => (
      <Circus>
        <Toon spec={C.ringmaster} pose={{ armL: "point", armR: "hips", eyes: "happy", mouth: "grin", look: -1 }} pos={[0, 0, 0.6]} />
      </Circus>
    )) },
  // Il avait été puni parce qu'il était sorti une nuit.
  36: { look: night, focus: 5, cam: { from: [-2.6, 2.2, 5.5], to: [-1.8, 2.0, 4.6], lookFrom: [0, 3.0, -2], fov: 54 },
    Body: B((t) => (
      <WallNight>
        <Toon spec={C.cyparis} pose={{ sit: true, eyes: "dot", mouth: "smile", look: 1 }} pos={[0, 3.62, -2]} />
        <Toon spec={C.guard} pose={{ armR: "point", armL: "hips", eyes: "angry", mouth: "open" }} pos={[-2.6, 0, 0.2]} h={1.85} seed={2} />
      </WallNight>
    )) },
  // Et c'est parce qu'on l'avait enfermé… qu'il est sorti vivant.
  37: { look: { ...ruin, saturation: 1.05, exposure: 1.1 }, focus: 5, cam: { from: [3.4, 1.5, 8.5], to: [3.2, 1.6, 7.0], lookFrom: [3, 1.5, 1.4], fov: 50 },
    Body: B((t, d) => (
      <Prison ruin door={1}>
        <Toon spec={C.cyparisHurt} pose={{ eyes: t > d * 0.6 ? "happy" : "dot", mouth: "grin", armL: t > d * 0.6 ? "up" : "down", armR: t > d * 0.6 ? "up" : "down" }} pos={[0, 0, 0]} path={{ from: [3, 0, 1.3], to: [3, 0, 3.2], start: 0, end: d * 0.6 }} />
      </Prison>
    )) },
};
void THREE; void Ground; void DOOR;
