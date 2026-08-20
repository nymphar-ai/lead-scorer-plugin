---
name: cold-email-first-touch
description: >-
  Write a per-lead cold email first touch under 150 words with a single ask, built on
  verified signals, as drafts in a Lead Scorer campaign. Use when the user mentions cold
  email, cold outreach, prospecting email, outbound email, first touch, SDR or sales
  emails, email copy, or says nobody replies to their emails.
---

# Cold email first touch

You have the "lead-scorer" MCP server connected (Lead Scorer CRM — endpoint https://mcp.lead-scorer.com/mcp, authenticated with Lead Scorer OAuth). Use its tools for every read and write. Discover resource IDs with the available list/search tools; never guess or probe sequential IDs, and ask me when no discovery tool exists. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

> **Context first.** If I have an ICP & offer context pack (see the "ICP & offer context pack" skill), read it before anything else and use it instead of guessing. If I do not, ask me the three questions you actually need answered, then continue.

## Goal
Write the first email for every lead in campaign <CAMPAIGN_ID> so that it could only have been sent to that person. I review and activate in the app; you never send.

## My inputs (edit these)
- Offer: <what I propose, and the ONE problem it solves>
- Proof: <a named customer, a measured result, or "none yet — say so honestly">
- Ask: <the single low-friction next step>

## Steps
1. **Preflight.** `list_sender_accounts` — stop if no healthy sender is connected. For email, also stop when `signature_configured` is false: ask me for the exact signature, then persist it once with `update_sender_account`. Never invent sender identity.
2. **Load context.** Resolve the campaign with `list_campaigns` when its ID is unknown, then call `get_campaign_authoring_context`; it returns each lead's enrichment, summary, insights and signal dossier. Use it; do not re-research what is already there.
3. **Write, lead by lead**, to this shape:
   - **Subject**: 2-4 words, lowercase, no punctuation tricks, no first name, no emoji. It should look like a note from a colleague.
   - **Opener** (1 sentence): about their world — the signal, dated and specific.
   - **Relevance** (1-2 sentences): why that signal makes my offer worth 20 seconds of their time.
   - **Proof** (1 sentence): a real number or a named customer. If I have none, drop this line rather than inflate one.
   - **Ask** (1 sentence): one question, low friction. Not a 30-minute demo in email one.
4. **Push drafts** with `write_campaign_drafts`.
5. **Self-check every draft** against this list and rewrite failures with `update_campaign_action_draft`:
   - Under 150 words total
   - The opener is about them, not me
   - No sentence starts with "I" or "We"
   - Exactly one ask, phrased as a question
   - Would survive the swap test: paste it under another lead's name and it should stop making sense
   - No jargon, no "quick question", no fake Re:/Fwd:
6. **Report.** Drafts written, 3 samples, and any lead you refused to write for (no verified signal) — those should be removed from the campaign, not templated.

## Voice calibration by seniority
- Founder / C-level: 3-5 sentences. They read the first line and decide.
- VP / Director: 5-7 sentences. They want the mechanism.
- Manager / IC / technical: 7-10 sentences. Detail earns credibility here.

## Anti-patterns (never ship these)
"I hope this email finds you well" · "I wanted to reach out" · "I came across your profile" · feature dumps · two CTAs · HTML templates · leverage / synergy / best-in-class · flattery as an opener.

## Hard rules
- Never fabricate a signal, a customer name or a number. Missing proof is a shorter email, not an invented one.
- Draft in, draft out: never touch campaign status.
