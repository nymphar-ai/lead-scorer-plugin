---
name: lead-enrichment-pipeline
description: >-
  Take a raw Lead Scorer list to campaign-ready: profile and company enrichment, email
  finding, and an AI summary per lead. Use when the user mentions enrichment, enriching
  leads, finding emails or contact details, missing data on a list, or says a list is not
  ready for outreach yet.
---

# Lead enrichment pipeline

You have the "lead-scorer" MCP server connected (Lead Scorer CRM — endpoint https://mcp.lead-scorer.com/mcp, authenticated with Lead Scorer OAuth). Use its tools for every read and write. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

## Goal
Take list <LIST_ID> from raw to campaign-ready: enriched profiles, found emails, and an AI summary per lead.

## What this costs — read before step 2
Enrichment is the only part of this chain that spends credits. Reads, scores and drafts are free.

| Call | Cost |
| --- | --- |
| `enrich_leads` | ~1 credit per lead |
| `enrich_company` | 1 credit (0 when served from cache) |
| `find_lead_contact_info` | 3 credits per email FOUND, 15 per phone found (nothing found, nothing charged) |

**Never enrich a whole list on arrival.** Pre-qualify for free first with the "ICP scoring rubric" skill (`submit_lead_score` costs nothing), then enrich only what scored as plausible ICP. Enriching blind costs around 8 credits per usable contact; pre-qualifying first brings it close to 1.

Both paid calls accept `dry_run: true`, which returns the estimate and your balance without spending anything. Above the account threshold they refuse to run without `confirm: true`, and the refusal states what it would have cost. That refusal is the feature, not an obstacle to route around.

## Steps
1. **Inventory.** `get_leads_from_list` — count who has a LinkedIn URL, an email, an enriched profile.
2. **Estimate, then enrich the pre-qualified only.** `enrich_leads` with `dry_run: true` on the shortlist to see the cost, then run it for real. Lead by lead (small batches; a big batch that half-fails is harder to retry). Enrichment REQUIRES the lead to have a linkedin_url — skip and report those without one. Use `enrich_company` for companies with a LinkedIn but no data.
3. **Contact finding.** Hand this to the "Contact discovery" skill: it only runs on leads confirmed as ICP that you intend to contact. An email found for someone nobody will write to is 3 credits burned — a miss is free, a useless hit is not.
4. **AI layer.** `get_leads_pending_ai_enrichment`, then for each: write a 3-4 line summary and 2-3 actionable insights (angle to open with, risk, timing) from the enriched data, and store them with `submit_lead_ai_enrichment`.
5. **Reconcile.** Enrichment data is the source of truth: if it contradicts what web research said (role changed, company pivoted), update your notes and say so.
6. **Report.** Enriched / emails found / AI-summarized / skipped (and why).

## Hard rules
- One lead at a time on enrichment writes; never fire-and-forget a 500-lead batch.
- Nothing paid runs on a lead that has not been scored first.
- No outreach here. This skill ends when the list is ready.
