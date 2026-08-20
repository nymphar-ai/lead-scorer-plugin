---
name: registry-first-sourcing
description: >-
  Source French SMEs from the official State company registry (SIREN, NAF), verify each
  one on the open web, then score them into Lead Scorer. Use when the user mentions the
  French registry, SIREN, SIRET, NAF codes, recherche-entreprises, sourcing French
  companies or PME, or wants prospects grounded in official data rather than scraped
  directories.
---

# Registry-first company sourcing (France)

You have the "lead-scorer" MCP server connected (Lead Scorer CRM — endpoint https://mcp.lead-scorer.com/mcp, authenticated with Lead Scorer OAuth). Use its tools for every read and write. Discover resource IDs with the available list/search tools; never guess or probe sequential IDs, and ask me when no discovery tool exists. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

## Goal
Build a shortlist of real French SMEs matching my ICP, starting from the official State registry (not scraped directories), verified on the open web, then scored.

## My inputs (edit these)
- ICP: <sector keywords / NAF hints, headcount range, region>
- Score criteria: <what makes a company a 9/10 for me>

## Steps
1. **Registry pass.** Use `search_official_company_registry` with sector terms. Note its quirks: filter results yourself on headcount and location; derive company age from the SIREN when the creation date is missing.
2. **Web verification.** For each candidate: does it have a live site? Signs of activity (news, jobs, LinkedIn)? Kill anything you cannot verify — the registry contains shells and dormant entities.
3. **CRM write.** `create_list` for today's batch; `create_company` + `create_lead` with the new list in `list_ids` (leaders found via the web/LinkedIn — never guess handles).
4. **Score.** For each lead call `submit_lead_score` with a 1-10 score and a 2-3 line `score_explanation` tied to MY criteria, not generic praise.
5. **Report.** Registry hits → verified → created → scored, plus the 5 best with one line each on why.

## Hard rules
- Registry data wins over web claims for legal facts; web wins for "is this company actually alive".
- Never create a lead whose LinkedIn you have not verified. Skip unverifiable identities instead of polluting the CRM.
