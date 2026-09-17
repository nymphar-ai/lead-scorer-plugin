---
name: freelance-talent-sourcing
description: >-
  Build a recruiter-grade freelance talent pool from public web profiles and platforms
  such as Collective, Malt and Free-Work, with one source list, normalized skills, dated
  availability and provenance per profile. Use when the user mentions sourcing
  freelancers, consultants, candidates, a talent pool, staffing, availability, TJM or
  daily rate, Collective, Malt, Free-Work, or finding freelance Data Engineers; do not use
  for company prospecting.
---

# Freelance talent sourcing

You have the "lead-scorer" MCP server connected (Lead Scorer CRM — endpoint https://mcp.lead-scorer.com/mcp, authenticated with Lead Scorer OAuth). Use its tools for every read and write. Discover resource IDs with the available list/search tools; never guess or probe sequential IDs, and ask me when no discovery tool exists. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

## Goal
Build a recruiter-ready pool for <ROLE> from <SOURCES>, aiming for <TARGET COUNT> real people. Keep one Lead Scorer lead list per source, plus structured profile facts that remain searchable across every list.

## Source order
1. Search the existing CRM first with `search_freelancers`.
2. Search the public web for named individual profiles and portfolios.
3. Search Collective, Malt and Free-Work when the user has access. Respect the visible site and account state; never bypass authentication, rate limits or access controls.
4. Record the publishing platform as the source. A marketplace, collective or intermediary shown on a page is not the candidate's employer.

## Steps
1. **Prepare the vocabulary.** Read `list_hiring_taxonomy` for role, skill and seniority, following every page. Reuse canonical slugs and call `ensure_hiring_term` only for a genuinely missing generic term. Python/python/PYTHON must remain one skill.
2. **Prepare lists.** Read `get_lead_lists`. Create or reuse one lead list per source: "Freelance <ROLE> — Web", "— Collective", "— Malt" and "— Free-Work". Do not create a duplicate list on refresh.
3. **Search deliberately.** Capture only named people with a stable public identity or profile URL. Record the exact source URL and observation date. Prefer explicit technical detail over generic titles. Do not claim availability, a date, a TJM, work mode, location preference or years of experience unless the page states it.
4. **Deduplicate before writing.** Match verified LinkedIn URL first, then exact platform profile URL, then name plus location/headline. Use `get_lead` or `get_freelance_profile` to review uncertain matches. Report uncertain pairs instead of merging them.
5. **Create the CRM identity.** Call `create_lead` with the verified LinkedIn URL when present, otherwise a public email, or the real full name plus the available profile facts. Include the source list ID in `list_ids`; for an existing accessible lead, use `add_leads_to_list`.
6. **Save the structured profile.** Call `upsert_freelance_profile` with:
   - every source's provider, public profile URL and `observed_at`;
   - normalized roles, atomic technical skills and seniority, each with a verbatim evidence excerpt;
   - explicit availability status/date and its visible label;
   - daily-rate range and ISO currency, experience, work modes, contract preferences, locations, languages, sector experience, portfolio/CV links and a concise recruiter summary when supported.
   Omit unknown fields. Empty normalized arrays mean verified none; omission preserves current terms; `normalized=null` clears them.
7. **Verify.** Read `get_freelance_profile` after every write. Confirm list membership, canonical terms, source URLs and freshness. An older observation may add provenance but must not replace newer facts.
8. **Report.** Per source: pages reviewed, profiles accepted, existing leads reused, new leads created, exact duplicates, uncertain duplicates and rejected profiles. Then show coverage gaps: missing availability, rate, location, LinkedIn identity or technical evidence.

## Hard rules
- Public professional facts only. Keep private recruiter notes in CRM notes or relationship memory.
- Never fabricate a person's identity, LinkedIn handle, rate or availability.
- A title alone does not prove a skill. Evidence must quote the profile or a supplied source.
- A stale availability statement stays dated; it is not silently treated as current.
- This skill sources and structures data. It does not enrich contacts, create a campaign or contact anyone.
