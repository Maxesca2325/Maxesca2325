"use client";

import Link from "next/link";
import { useId, useState } from "react";
import { Check, LoaderCircle } from "lucide-react";
import { normalizeContact } from "@/lib/contact";

/**
 * DEMO sign-up: shows the real flow (phone +509 or email → one-time code →
 * 3 credits) without creating an account. Step 3 wires it to Supabase Auth
 * (signInWithOtp / verifyOtp); the 3 credits are granted by the database
 * trigger in supabase/migrations, never by the client.
 */
export function SignUp() {
  const [step, setStep] = useState<"contact" | "code" | "done">("contact");
  const [contact, setContact] = useState("");
  const [code, setCode] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [pending, setPending] = useState(false);
  const id = useId();

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    if (step === "contact") {
      const c = normalizeContact(contact);
      if (!c) return setError("Numéro ou email invalide. Exemple : 3712 3456");
      setContact(c.value);
    } else if (!/^\d{6}$/.test(code)) {
      return setError("Le code a 6 chiffres.");
    }
    setPending(true);
    await new Promise((r) => setTimeout(r, 600));
    setPending(false);
    setStep(step === "contact" ? "code" : "done");
  }

  if (step === "done") {
    return (
      <div className="reveal space-y-5">
        <div className="flex items-start gap-3 rounded-card border border-good/40 bg-good/10 p-4">
          <Check className="mt-0.5 shrink-0 text-good" size={20} aria-hidden="true" />
          <p>
            <strong>Compte créé (démo).</strong> 3 crédits t&apos;attendent.
          </p>
        </div>
        <Link href="/app" className="flex h-14 items-center justify-center rounded-xl bg-accent font-semibold text-on-accent">
          Voir les matchs
        </Link>
      </div>
    );
  }

  return (
    <form onSubmit={submit} noValidate className="space-y-3">
      {step === "contact" ? (
        <>
          <label htmlFor={id} className="block text-sm font-medium text-text-2">
            Téléphone (+509) ou email
          </label>
          <input
              id={id}
              value={contact}
              onChange={(e) => setContact(e.target.value)}
              autoComplete="tel-national"
              placeholder="3712 3456 ou toi@exemple.com"
              className="h-14 w-full rounded-xl border border-line bg-surface-2 px-4 text-lg outline-none placeholder:text-text-3 focus:border-accent"
            />
        </>
      ) : (
        <>
          <label htmlFor={id} className="block text-sm font-medium text-text-2">
            Code reçu au {contact}
          </label>
          <input
            id={id}
            value={code}
            onChange={(e) => setCode(e.target.value.replace(/\D/g, "").slice(0, 6))}
            inputMode="numeric"
            autoComplete="one-time-code"
            placeholder="••••••"
            className="h-14 w-full rounded-xl border border-line bg-surface-2 px-4 text-center font-display text-3xl tracking-[0.4em] outline-none focus:border-accent"
          />
          <p className="text-xs text-text-3">Démo : n&apos;importe quel code à 6 chiffres.</p>
        </>
      )}
      {error && <p className="text-sm text-bad">{error}</p>}
      <button
        type="submit"
        disabled={pending}
        className="flex h-14 w-full items-center justify-center gap-2 rounded-xl bg-accent font-semibold text-on-accent hover:bg-accent-press disabled:opacity-70"
      >
        {pending && <LoaderCircle size={18} className="animate-spin" aria-hidden="true" />}
        {step === "contact" ? "Recevoir mon code" : "Valider"}
      </button>
    </form>
  );
}
