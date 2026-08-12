---
name: daily-vertical-prospecting
description: >-
  Cover one new vertical per run: find real companies and decision-makers on the web and
  land them in a clean, tagged Lead Scorer list. Use when the user mentions prospecting,
  sourcing leads, finding companies, a new niche, segment or vertical, building a lead
  list, or wants a daily prospecting routine.
---

# Daily vertical prospecting

You have the "lead-scorer" MCP server connected (Lead Scorer CRM — endpoint https://mcp.lead-scorer.com/mcp, authenticated with Lead Scorer OAuth). Use its tools for every read and write. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

## Goal
Each run covers ONE new vertical (a niche, industry segment, or country) for my product and turns it into a clean list of companies + decision-makers in Lead Scorer.

## My inputs (edit these)
- Product: <what I sell, in one line>
- ICP: <company size, geography, buyer role>
- Vertical rotation: pick the next uncovered vertical from <my list of verticals>, or propose the next logical one.

## Steps
1. **Check coverage.** Call `get_lead_lists` and look at my existing list names and tags. Never redo a vertical that already has a list; announce which vertical you picked and why.
2. **Source companies (web research).** Find 15-30 real companies in the vertical that match the ICP. Only companies you can verify exist (site, LinkedIn, registry). No directories, no dead brands.
3. **Source people.** For each company, identify 1-2 decision-makers matching the buyer role. Real names with a verifiable LinkedIn profile only. NEVER guess a LinkedIn handle — if you cannot verify it, store the lead without one.
4. **Write to Lead Scorer.**
   - `create_list` named "<VERTICAL> — <today's date>".
   - `create_company` for each company (it dedups by LinkedIn username), then `create_lead` for each person, `add_leads_to_list`.
   - Tag every lead with the vertical name via `add_tags_to_lead` — tags are the coverage ledger.
5. **Report.** Companies found / created / already existing, leads created, and which vertical to do tomorrow.

## Hard rules
- Quality over volume: 15 verified leads beat 50 guessed ones.
- If `create_lead` returns authorized:false or already_exists, move on — never force.
- No outreach in this skill. Sourcing only; campaigns are a separate decision.
