import "server-only";
import { createClient, type SupabaseClient } from "@supabase/supabase-js";

/**
 * Server-only Supabase clients. Keys never reach the browser:
 * - SUPABASE_SERVICE_ROLE_KEY bypasses RLS; used only by trusted server code.
 * - NEXT_PUBLIC_SUPABASE_ANON_KEY is safe to expose but we still read public
 *   data server-side to keep the client bundle small.
 */
const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
const anon = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
const service = process.env.SUPABASE_SERVICE_ROLE_KEY;

export const supabaseConfigured = Boolean(url && anon);

export function publicClient(): SupabaseClient | null {
  if (!url || !anon) return null;
  return createClient(url, anon, { auth: { persistSession: false } });
}

export function adminClient(): SupabaseClient | null {
  if (!url || !service) return null;
  return createClient(url, service, { auth: { persistSession: false } });
}
