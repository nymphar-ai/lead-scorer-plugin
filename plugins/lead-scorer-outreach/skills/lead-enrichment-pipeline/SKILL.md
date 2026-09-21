---
name: lead-enrichment-pipeline
description: >-
  Take a raw Lead Scorer list to campaign-ready: profile and company enrichment, email
  finding, and an AI summary per lead. Use when the user mentions enrichment, enriching
  leads, finding emails or contact details, missing data on a list, or says a list is not
  ready for outreach yet.
---

# Lead enrichment pipeline

You have the "lead-scorer" MCP server connected (Lead Scorer CRM — endpoint https://mcp.lead-scorer.com/mcp, authenticated with Lead Scorer OAuth). Use its tools for CRM reads and writes. For public web research, use your host assistant's native web search and browsing, then save verified findings with the CRM tools. Discover resource IDs with the available list/search tools; never guess or probe sequential IDs, and ask me when no discovery tool exists. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

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
2. **Estimate, then enrich the pre-qualified only.** Call `enrich_leads` once with `dry_run: true` and the complete shortlist, then call it once for real with the same `lead_ids`. The backend persists one resumable run and processes it in restartable chunks of at most 10 leads; one tool call per lead creates a burst of competing runs and must never be used. Enrichment REQUIRES the lead to have a linkedin_url — skip and report those without one. Use `enrich_company` for companies with a LinkedIn but no data.
3. **Contact finding.** Hand this to the "Contact discovery" skill: it only runs on leads confirmed as ICP that you intend to contact. An email found for someone nobody will write to is 3 credits burned — a miss is free, a useless hit is not.
4. **Company research.** Select the owned product/ICP, call `get_companies_pending_research` (optionally scoped to the company list), then read each official product site. Save a factual, source-backed site summary plus a separate analysis against that product and ICP with `submit_company_research`. Do not draft outreach in this step.
5. **Lead AI layer.** `get_leads_pending_ai_enrichment`, then for each: write a 3-4 line summary and 2-3 actionable insights (angle to open with, risk, timing) from the enriched data, and store them with `submit_lead_ai_enrichment`.
6. **Reconcile.** Enrichment data is the source of truth: if it contradicts what web research said (role changed, company pivoted), update your notes and say so.
7. **Report.** Enriched / company-researched / emails found / AI-summarized / skipped (and why).

## Hard rules
- One shortlist per `enrich_leads` call, up to 1,000 leads. The safe client request is 1,000 because the server chunks execution at 10; never loop or parallelize one call per lead.
- Keep the returned run ID and poll it with `get_lead_enrichment_run`; stop on either `completed` or `failed`, and use `list_lead_enrichment_runs` to recover progress after a restarted session. Never wait for every lead to become `full`.
- Nothing paid runs on a lead that has not been scored first.
- Company research must cite the official site. Keep factual site summary separate from the interpretation tied to the selected product/ICP.
- Write CRM summaries, research analyses and insights in English, even with non-English sources. Preserve names and source quotations. Outreach language is selected independently.
- No outreach here. This skill ends when the list is ready.
