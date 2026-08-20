---
name: daily-topic-briefs
description: >-
  Research a topic's fresh signals and write a sourced editorial brief (signals,
  interpretation, angles, hooks) into Lead Scorer's content library. Use when the user
  mentions veille, content research, editorial briefs, industry monitoring, or wants raw
  material before writing posts.
---

# Daily topic brief (veille → editorial brief)

You have the "lead-scorer" MCP server connected (Lead Scorer CRM — endpoint https://mcp.lead-scorer.com/mcp, authenticated with Lead Scorer OAuth). Use its tools for every read and write. Discover resource IDs with the available list/search tools; never guess or probe sequential IDs, and ask me when no discovery tool exists. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

## Goal
Produce ONE editorial brief for topic <TOPIC> from today's fresh signals, structured so a writing agent (or I) can turn it into posts without re-researching.

## Steps
1. **Research.** Find 4-6 FRESH signals (last 30 days) on the topic: studies with numbers, named company cases, practitioner verbatims. Web sources only; keep the URL of each.
2. **Write the brief** with exactly these sections:
   - **TL;DR** (3 lines max)
   - **Signals** — each: the fact, the number, the source URL
   - **Interpretation** — the operator take: what this means for my audience, what everyone gets wrong, the consequence at 12 months
   - **Possible angles** (2-3, each one thesis)
   - **Candidate hooks** (2-3 one-liners, fact-first)
   - **Raw material** — verbatims and exact figures ready to quote
3. **Store.** `upsert_content_item` with item_type "brief", category "<topic-slug>", external_id "brief:<topic-slug>/<YYYY-MM-DD>" (idempotent: re-running the same day updates, not duplicates).
4. **Report.** The TL;DR + the strongest angle.

## Hard rules
- No signal without a source. No round numbers you cannot cite.
- The Interpretation is the value: never ship a brief that only lists news.
- Distinguish verified facts from vendor-claimed numbers ("self-reported").
