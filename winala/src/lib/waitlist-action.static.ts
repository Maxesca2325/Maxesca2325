// Static test build: no server, so nothing is stored. Says so plainly.
import { normalizeContact } from "./contact";

export type WaitlistState = { status: "idle" | "ok" | "error"; message: string };

export async function joinWaitlist(_prev: WaitlistState, form: FormData): Promise<WaitlistState> {
  if (!normalizeContact(String(form.get("contact") ?? ""))) {
    return { status: "error", message: "Numéro ou email invalide. Exemple : 3712 3456 ou toi@exemple.com" };
  }
  return {
    status: "error",
    message: "Version de test : la liste d'attente n'est pas active ici. Rien n'a été enregistré.",
  };
}
