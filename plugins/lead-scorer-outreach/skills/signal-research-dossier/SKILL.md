---
name: signal-research-dossier
description: >-
  Research each lead until there are at least two verified, dated signals with sources,
  and skip the lead honestly when there are none. Use when the user mentions
  personalization, research before outreach, buying signals, triggers, relevance, or
  complains that their messages feel generic or templated.
---

# Verified signal dossier

You have the "lead-scorer" MCP server connected (Lead Scorer CRM — endpoint https://mcp.lead-scorer.com/mcp, authenticated with Lead Scorer OAuth). Use its tools for every read and write. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

> **Context first.** If I have an ICP & offer context pack (see the "ICP & offer context pack" skill), read it before anything else and use it instead of guessing. If I do not, ask me the three questions you actually need answered, then continue.

## Goal
Before any campaign on list <LIST_ID>, build a short dossier per lead containing only facts you can point at. Personalization quality is a research problem, not a writing problem.

## Signal hierarchy (use the highest available, record its level)
1. **The lead's own words** — a post, comment or talk from the last ~8 weeks (`get_lead_posts`). Strongest; quote it.
2. **A company event** — funding, hiring wave, launch, new market, leadership change (`get_company_info`, `enrich_leads`, web).
3. **Role reality** — recent role change, unusual scope, a team they clearly own.
4. **Segment truth** — something demonstrably true of their exact segment, not of "companies like yours".
5. **Nothing.** Say so and skip the lead. This is a valid, expected outcome.

## Steps
1. `get_leads_from_list` and work lead by lead.
2. For each: pull `get_lead`, `get_lead_posts`, `get_company_info`; fill gaps with `enrich_leads` (requires linkedin_url) and targeted web research.
3. Write the dossier: 2-4 signals max, each with **level · the fact · the source URL · a date**. Add one line of "so what for this lead" — the angle the signal unlocks.
4. Store it with `submit_lead_ai_enrichment` so the campaign-authoring skills read it instead of re-researching.
5. **Report** three buckets: ready (≥2 signals, at least one level 1-2), thin (1 signal), skip (nothing verified) — with counts.

## Hard rules
- A signal needs a source and a date. "They seem focused on growth" is not a signal.
- Never infer a signal from the company's marketing site copy. That is their claim, not an event.
- Undated signals older than ~3 months are stale for level 1 — demote them.
