import type { Metadata } from "next";
import { Recharge } from "@/components/recharge";

export const metadata: Metadata = { title: "Crédits" };

export default function CreditsPage() {
  return <Recharge />;
}
