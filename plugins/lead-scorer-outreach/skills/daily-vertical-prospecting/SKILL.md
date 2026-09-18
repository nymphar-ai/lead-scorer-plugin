---
name: daily-vertical-prospecting
description: >-
  Cover one new vertical per run: find real companies and decision-makers on the web and
  land them in a clean, tagged Lead Scorer list. Use when the user mentions prospecting,
  sourcing leads, finding companies, a new niche, segment or vertical, building a lead
  list, or wants a daily prospecting routine.
---

# Daily vertical prospecting

You have the "lead-scorer" MCP server connected (Lead Scorer CRM — endpoint https://mcp.lead-scorer.com/mcp, authenticated with Lead Scorer OAuth). Use its tools for CRM reads and writes. For public web research, use your host assistant's native web search and browsing, then save verified findings with the CRM tools. Do not delegate web search to Lead Scorer workflows or call its HTTP endpoints as a fallback: those searches incur server-side provider costs. If native search is unavailable, ask me to enable it or provide sources; do not silently switch to a paid backend search. Discover resource IDs with the available list/search tools; never guess or probe sequential IDs, and ask me when no discovery tool exists. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

## Goal
Each run covers ONE new vertical (a niche, industry segment, or country) for my product and turns it into a clean list of companies + decision-makers in Lead Scorer.

## My inputs (edit these)
- Product: <what I sell, in one line>
- ICP: <company size, geography, buyer role>
- Vertical rotation: pick the next uncovered vertical from <my list of verticals>, or propose the next logical one.

## Steps
1. **Check coverage.** Call `get_lead_lists` and look at my existing list names and tags. Never redo a vertical that already has a list; announce which vertical you picked and why.
2. **Source companies (web research).** Find 15-30 real companies in the vertical that match the ICP. Only companies you can verify exist (official site, LinkedIn, registry). No directories, no dead brands.
3. **Source people.** For each company, identify 1-2 decision-makers matching the buyer role. Use verified person names and LinkedIn profiles or email addresses. For a company mailbox, omit the person name and use contact_kind=company. NEVER guess a LinkedIn handle or person name.
4. **Write to Lead Scorer.**
   - `create_list` named "<VERTICAL> — <today's date>".
   - `create_company` for each company (it dedups by LinkedIn username), then `create_lead` for each contact with email or verified LinkedIn identity (or full_name plus an authorized company_id), and that list ID in `list_ids`. Creation, deduplication and list membership are atomic.
   - Reuse or create a company list and persist every authorized company with `add_companies_to_list`. A company mentioned in a note is not a CRM association. Supply `company_id` when creating a new lead; for an existing lead, read `get_lead` and use `set_lead_primary_company` with a company from its returned career. Enrich first if career data is missing. Never silently substitute a holding company for the recruiting subsidiary.
   - For hiring-led prospecting, read `list_hiring_taxonomy` first (roles, skills, seniorities; iterate until has_more=false). Reuse canonical slugs; use `ensure_hiring_term` only for a genuinely missing generic term. Pass normalized.roles, normalized.skills and normalized.seniorities as arrays of {slug,evidence}, quoting relevant saved job facts verbatim. Unknown values are rejected; casing/aliases reuse one term. Then search existing saved vacancies first with `search_hiring_companies` (normalized role, all skills on the same job, location, status, observation date). Use status=all only when historical hiring is useful. Then verify the public vacancy and save it with `upsert_company_hiring_signal`: title, location, URL, status, and observation date. Capture all available public facts in details: salary and its stated period, remote policy, seniority, profile criteria, responsibilities, stack, benefits, interview process, and dated sources. Keep missing facts absent; do not infer the hiring manager. Publication dates are optional and must not be invented. Preserve relative wording in details.publication_label and contradictions in details.source_notes. Read it back with `get_company_signals` and verify each lead's company with `get_lead` before claiming completion.
   - Tag every lead with the vertical name via `add_tags_to_lead` — tags are the coverage ledger.
5. **Report.** Companies found / created / already existing, leads created, and which vertical to do tomorrow.

## Hard rules
- Quality over volume: 15 verified leads beat 50 guessed ones.
- If `create_lead` returns authorized:false or already_exists, move on — never force.
- No outreach in this skill. Sourcing only; campaigns are a separate decision.
