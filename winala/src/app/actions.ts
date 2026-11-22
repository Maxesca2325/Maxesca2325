"use server";

import { normalizeContact } from "@/lib/contact";
import { adminClient } from "@/lib/supabase/server";

export type WaitlistState = { status: "idle" | "ok" | "error"; message: string };

export async function joinWaitlist(_prev: WaitlistState, form: FormData): Promise<WaitlistState> {
  // Honeypot: bots fill every field; humans never see this one.
  if (String(form.get("website") ?? "").length > 0) {
    return { status: "ok", message: "C'est noté." };
  }
  const contact = normalizeContact(String(form.get("contact") ?? ""));
  if (!contact) {
    return {
      status: "error",
      message: "Numéro ou email invalide. Exemple : 3712 3456 ou toi@exemple.com",
    };
  }
  const db = adminClient();
  if (!db) {
    return {
      status: "error",
      message: "La liste d'attente n'est pas encore connectée. Réessaie bientôt.",
    };
  }
  const source = String(form.get("source") ?? "landing").slice(0, 40);
  // ON CONFLICT DO NOTHING: a second sign-up is silently accepted, so nobody can
  // probe which numbers are already on the list.
  const { error } = await db
    .from("waitlist")
    .upsert({ contact: contact.value, kind: contact.kind, source }, { onConflict: "contact", ignoreDuplicates: true });
  if (error) {
    return { status: "error", message: "Connexion difficile. Réessaie dans un instant." };
  }
  return {
    status: "ok",
    message:
      contact.kind === "phone"
        ? `C'est noté. On t'écrit au ${contact.value} à l'ouverture, avec tes 3 crédits offerts.`
        : "C'est noté. On t'écrit à l'ouverture, avec tes 3 crédits offerts.",
  };
}
