---
name: crm-hygiene-audit
description: >-
  Sweep the CRM for broken LinkedIn URLs, missing emails, unscored leads and enrichment
  gaps, fixing what a tool can fix and flagging the rest. Use when the user mentions CRM
  hygiene, data quality, cleaning lists, duplicates, missing data, or wants a weekly
  maintenance routine.
---

# CRM hygiene audit

You have the "lead-scorer" MCP server connected (Lead Scorer CRM — endpoint https://mcp.lead-scorer.com/mcp, authenticated with Lead Scorer OAuth). Use its tools for every read and write. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

## Goal
Keep the CRM trustworthy: every campaign and score is only as good as the data under it.

## Steps
1. **Sweep.** `get_lead_lists`, then sample each meaningful list with `get_leads_from_list`: count leads missing linkedin_url, email, enrichment, score.
2. **Fix what a tool can fix.** Malformed LinkedIn URLs → `update_lead_linkedin` / `update_company_linkedin` with the verified profile. Do not guess: verify, or leave and flag.
3. **Score the backlog.** `get_leads_pending_scoring`; score each against my ICP with `submit_lead_score` + a 2-line explanation.
4. **Tags.** `list_tags` — flag near-duplicate or inconsistent tags for my decision (do not mass-rename on your own).
5. **Report.** Defects found / fixed / needing me, per list, with a week-over-week comparison if a previous report exists.

## Hard rules
- Never delete anything. Flag for my decision.
- A verified empty field beats a guessed value, always.
