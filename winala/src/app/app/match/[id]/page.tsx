import Link from "next/link";
import { Suspense } from "react";
import { notFound } from "next/navigation";
import { ChevronLeft } from "lucide-react";
import { MatchHeader } from "@/components/match-header";
import { MatchAnalysis } from "@/components/match-analysis";
import { DEMO_MATCHES, demoMatchById, leagueById } from "@/lib/demo-data";

export function generateStaticParams() {
  return DEMO_MATCHES.map((m) => ({ id: m.id }));
}

export async function generateMetadata({ params }: PageProps<"/app/match/[id]">) {
  const { id } = await params;
  const m = demoMatchById(id);
  return { title: m ? `${m.home.name} – ${m.away.name}` : "Match" };
}

export default function MatchPage({ params }: PageProps<"/app/match/[id]">) {
  return (
    <Suspense fallback={<div className="h-64 animate-pulse rounded-card bg-surface" aria-label="Chargement" />}>
      <MatchContent params={params} />
    </Suspense>
  );
}

async function MatchContent({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const match = demoMatchById(id);
  if (!match) notFound();
  const league = leagueById(match.leagueId);
  return (
    <div className="space-y-3">
      <Link href="/app" className="-ml-1 inline-flex items-center gap-1 rounded-md py-1 text-sm font-semibold text-text-2 hover:text-text">
        <ChevronLeft size={18} aria-hidden="true" /> Matchs
      </Link>
      <MatchHeader match={match} />
      <MatchAnalysis match={match} leagueCalibrated={league.calibrated} />
    </div>
  );
}
