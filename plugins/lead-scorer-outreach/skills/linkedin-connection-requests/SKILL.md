---
name: linkedin-connection-requests
description: >-
  Write signal-based LinkedIn connection notes under 200 characters and keep the batch
  inside LinkedIn's real daily and weekly invitation limits. Use when the user mentions
  LinkedIn connection requests, invitations, connection notes, adding prospects on
  LinkedIn, accept rate, or asks how many invites are safe to send.
---

# LinkedIn connection requests that get accepted

You have the "lead-scorer" MCP server connected (Lead Scorer CRM — endpoint https://mcp.lead-scorer.com/mcp, authenticated with Lead Scorer OAuth). Use its tools for every read and write. Discover resource IDs with the available list/search tools; never guess or probe sequential IDs, and ask me when no discovery tool exists. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

> **Context first.** Call `get_my_memory`, then `compile_context_pack` when a lead or campaign is in scope. Treat personal memory as user-owned context, not verified public CRM data. If my memory is empty, ask me the three questions you actually need answered, then continue.

## Goal
Prepare today's connection requests for list <LIST_ID>: a short, signal-based note per person, inside safe volume limits. I review the batch and send.

## Steps
1. **Pick the batch.** `get_leads_from_list`, keep leads with a verified LinkedIn URL. Cap the batch (see limits below) and prioritize by score and signal freshness.
2. **Find the signal** per lead, best available first: `get_lead_posts` / `fetch_profile_posts` (their own recent post — strongest), then a mutual context or shared background, then a company event (`get_company_info`), then their role reality. **If none of these exists, skip the lead and say so.** A generic note is worse than no note.
3. **Write the note.** Target 150-200 characters, structured as: one hook sentence (the specific signal) + a blank line + the CTA.
   - Reference the signal in the first clause, concretely.
   - The CTA earns the connection, it does not ask for a conversation: "Connectons-nous pour [concrete gain for them]" — name the value in their terms ("l'IA appliquée au recrutement", "aux RH", "au conseil").
   - No pitch, no link, no meeting request. The ask is the connection itself.
   - **Banned closings**, they read as a template: "Je serais ravi d'en échanger.", "On reste en contact ?", "Au plaisir de vous compter dans mon réseau."
   - No em dash (— –), no Markdown, French typographic apostrophes (').
4. **Tag** what you used with `add_tags_to_lead` (e.g. `signal:post`, `signal:hiring`) so the post-accept follow-up knows what to build on.
5. **Report** the batch as a table: lead · signal level · note · character count · skip reason if skipped.

## Limits that protect the account (check yours before scaling)
- Personalized note length: **300 characters on Premium/Sales Navigator, 200 on Free/Basic** — and Free/Basic accounts can only add a note to a handful of invitations per month. Write for 200 unless I tell you I'm on Premium.
- Volume: LinkedIn throttles around 20-25 a day and ~100 per rolling 7 days, but **Lead Scorer caps invitations at 15 per account per day**, all campaigns combined, and lower while an account is warming up. Plan for the cap the engine enforces, not the one LinkedIn tolerates: anything above it is simply deferred to the next day.
- Stop immediately on a CAPTCHA or a "weekly invitation limit reached" warning, and tell me.

## Benchmarks (industry figures, not guarantees)
Personalized requests land roughly 35-55% acceptance; generic or blank ones 15-25%. Above 40% is healthy; sustained below 20% means the targeting or the note is wrong — and a low accept rate is itself an account risk. Diagnose the signal level before rewriting the copy.

## Hard rules
- Never guess a LinkedIn profile URL. Verified or skipped.
- Never claim a shared connection, event or read you have not verified.
- Draft only. I send the batch myself.
