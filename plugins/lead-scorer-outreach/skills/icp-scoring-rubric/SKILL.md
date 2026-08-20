---
name: icp-scoring-rubric
description: >-
  Build a weighted 1-10 ICP scoring rubric, calibrate it against leads the user already
  has an opinion on, then score the backlog in Lead Scorer. Use when the user mentions
  lead scoring, ICP score, scoring criteria, qualifying or prioritizing leads, or asks
  which leads in a list are worth contacting first.
---

# ICP scoring rubric

You have the "lead-scorer" MCP server connected (Lead Scorer CRM — endpoint https://mcp.lead-scorer.com/mcp, authenticated with Lead Scorer OAuth). Use its tools for every read and write. Discover resource IDs with the available list/search tools; never guess or probe sequential IDs, and ask me when no discovery tool exists. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

> **Context first.** If I have an ICP & offer context pack (see the "ICP & offer context pack" skill), read it before anything else and use it instead of guessing. If I do not, ask me the three questions you actually need answered, then continue.

## Goal
Define a scoring rubric I can defend, calibrate it against leads I already have an opinion on, then apply it to the backlog.

## This is free, and it runs first
You do the judging; the platform only stores the result. Reading leads and writing scores costs **zero credits** — `get_leads_from_list`, `get_lead`, `get_leads_pending_scoring` and `submit_lead_score` are all free, however many leads you run them on.

That is what makes this the first step of every list. Enrichment and contact discovery are the paid calls, and they should only ever touch what scored well here. Score the whole list, then spend on the top of it — never the reverse.

Score from what is already on the lead: headline, role, company name and whatever the source captured. Do not enrich to score; that inverts the order and is exactly how a run ends up spending 8 credits per usable contact instead of 1.

## Steps
1. **Draft the rubric.** 4-6 criteria max, each weighted, each observable from data the CRM actually holds (company size, sector, role seniority, buying trigger, tech/market signal). A criterion nobody can observe is a wish, not a criterion.
2. **Set the bands.** What does 9-10 mean, 7-8, 4-6, 1-3? Write one concrete example company per band.
3. **Calibrate before you scale.** Take 10 leads I already have a view on (`get_leads_from_list`, `get_lead`), score them by the rubric, and show me the table. Where your score and my gut disagree, the rubric is wrong — fix the weights, not my opinion.
4. **Persist.** `create_scoring_config` with the criteria and weights so runs stay comparable over time.
5. **Apply.** `get_leads_pending_scoring`, then `submit_lead_score` per lead with a 2-line `score_explanation` naming the criteria that drove the number. Never "strong fit for our solution".
6. **Report.** Score distribution, the 5 highest with why, and any criterion that never discriminated (every lead scored the same on it — cut it).

## Hard rules
- A score without an explanation tied to a named criterion is noise. Never submit one.
- If more than 40% of leads land 8+, the rubric is flattering, not scoring. Tighten it and say so.
- Missing data lowers confidence, it does not raise the score. Say "unknown" instead of assuming.
