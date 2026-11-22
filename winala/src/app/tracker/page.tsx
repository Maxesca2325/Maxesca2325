import type { Metadata } from "next";
import { Suspense } from "react";
import { Check, Clock3, Minus, X } from "lucide-react";
import { SiteFooter, SiteHeader } from "@/components/site-header";
import { getTracker, summarize, type TrackerRow } from "@/lib/tracker";

export const metadata: Metadata = {
  title: "Historique public",
  description:
    "Tous les pronostics Winala, horodatés avant le coup d'envoi et réglés après le match. Taux de réussite cumulé, visible sans compte.",
};

export default function TrackerPage() {
  return (
    <>
      <SiteHeader />
      <main className="mx-auto w-full max-w-3xl flex-1 px-4 py-8 md:py-12">
        <h1 className="font-display text-5xl leading-none">Historique public</h1>
        <p className="mt-4 text-lg text-text-2">
          Chaque pronostic est publié et horodaté <strong className="text-text">avant</strong> le coup d&apos;envoi, puis réglé après le
          match. Rien n&apos;est effacé, les pertes restent visibles.
        </p>
        <Suspense fallback={<TrackerSkeleton />}>
          <TrackerBody />
        </Suspense>

        <section className="mt-12 space-y-3 text-text-2">
          <h2 className="text-lg font-semibold text-text">Comment lire ces chiffres</h2>
          <p>
            <strong className="text-text">Réussite</strong> : part des pronostics gagnés parmi ceux réglés (les matchs reportés ou annulés
            ne comptent pas).
          </p>
          <p>
            <strong className="text-text">Attendu</strong> : nombre de pronostics qu&apos;on aurait dû gagner si les probabilités annoncées
            étaient parfaitement justes. Si on gagne beaucoup moins que l&apos;attendu, le modèle est trop optimiste.
          </p>
          <p>
            <strong className="text-text">Empreinte</strong> : avant le coup d&apos;envoi, le pronostic est scellé. On publie seulement
            son empreinte (SHA-256). Après le match, le pronostic et le code de vérification apparaissent : chacun peut recalculer
            l&apos;empreinte et vérifier qu&apos;on n&apos;a rien changé.
          </p>
          <p>
            <strong className="text-text">Score de Brier</strong> : l&apos;écart moyen entre la probabilité annoncée et le résultat. Plus il
            est bas, mieux le modèle est calibré.
          </p>
        </section>
      </main>
      <SiteFooter />
    </>
  );
}

async function TrackerBody() {
  const { rows } = await getTracker();
  const s = summarize(rows);
  return (
    <>
      <dl className="mt-8 grid grid-cols-2 gap-px overflow-hidden rounded-card border border-line bg-line sm:grid-cols-4">
        {[
          ["Réglés", String(s.settled)],
          ["Gagnés", String(s.wins)],
          ["Réussite", s.rate === null ? "—" : `${Math.round(s.rate * 100)} %`],
          ["Attendu", s.settled ? s.expected.toFixed(1).replace(".", ",") : "—"],
        ].map(([k, v]) => (
          <div key={k} className="bg-surface px-4 py-4">
            <dt className="text-xs text-text-2">{k}</dt>
            <dd className="font-display text-3xl">{v}</dd>
          </div>
        ))}
      </dl>
      {s.brier !== null && (
        <p className="mt-3 text-sm text-text-2">Score de Brier : {s.brier.toFixed(3).replace(".", ",")}</p>
      )}

      {rows.length === 0 ? (
        <div className="mt-6 flex flex-col items-center gap-2 rounded-card border border-dashed border-line px-6 py-12 text-center">
          <Clock3 className="text-text-3" size={24} aria-hidden="true" />
          <p className="font-semibold">Aucun pronostic publié pour l&apos;instant.</p>
          <p className="max-w-sm text-sm text-text-2">
            L&apos;historique démarre au lancement, avec le premier vrai pronostic. On n&apos;affiche aucun chiffre tant qu&apos;il n&apos;y a
            pas de vrais résultats.
          </p>
        </div>
      ) : (
        <ul className="mt-6 divide-y divide-line overflow-hidden rounded-card border border-line bg-surface">
          {rows.map((r) => (
            <TrackerItem key={r.id} r={r} />
          ))}
        </ul>
      )}
    </>
  );
}

const fmt = new Intl.DateTimeFormat("fr-HT", {
  timeZone: "America/Port-au-Prince",
  day: "2-digit",
  month: "short",
  hour: "2-digit",
  minute: "2-digit",
});

function TrackerItem({ r }: { r: TrackerRow }) {
  const icon =
    r.result === "WIN" ? (
      <Check className="text-good" size={18} aria-label="Gagné" />
    ) : r.result === "LOSS" ? (
      <X className="text-bad" size={18} aria-label="Perdu" />
    ) : r.result === "VOID" ? (
      <Minus className="text-text-3" size={18} aria-label="Annulé" />
    ) : (
      <Clock3 className="text-text-3" size={18} aria-label="En attente" />
    );
  return (
    <li className="flex items-start gap-3 px-4 py-3">
      <span className="mt-1">{icon}</span>
      <div className="min-w-0 flex-1">
        <div className="truncate font-semibold">
          {r.home_team} – {r.away_team}
        </div>
        {r.predicted_pick !== null && r.probability !== null ? (
          <div className="text-sm text-text-2">
            {r.market} : {r.predicted_pick} · {Math.round(r.probability * 100)} %
          </div>
        ) : (
          <div className="text-sm text-text-2">
            {r.market} : scellé avant le match · empreinte{" "}
            <code className="font-mono text-xs" title={r.commitment}>
              {r.commitment.slice(0, 10)}…
            </code>
          </div>
        )}
        <div className="mt-0.5 text-xs text-text-3">
          {r.league_name} · publié le {fmt.format(new Date(r.published_at))}, coup d&apos;envoi {fmt.format(new Date(r.kickoff_time))}
        </div>
      </div>
    </li>
  );
}

function TrackerSkeleton() {
  return <div className="mt-8 h-24 animate-pulse rounded-card bg-surface" aria-label="Chargement" />;
}
