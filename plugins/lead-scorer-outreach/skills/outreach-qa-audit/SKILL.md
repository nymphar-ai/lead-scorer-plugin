---
name: outreach-qa-audit
description: >-
  Score every draft in a campaign out of 100 against a fixed rubric and rewrite anything
  below threshold before it reaches the user. Use when the user mentions reviewing drafts,
  message quality, a QA pass, auditing a campaign before sending, or asks whether their
  outreach is good enough to send.
---

# Outreach QA & scoring gate

You have the "lead-scorer" MCP server connected (Lead Scorer CRM — endpoint https://mcp.lead-scorer.com/mcp, authenticated with Lead Scorer OAuth). Use its tools for every read and write. Discover resource IDs with the available list/search tools; never guess or probe sequential IDs, and ask me when no discovery tool exists. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

## Goal
Nothing in campaign <CAMPAIGN_ID> reaches me for approval until it has been scored and, if needed, rewritten. Grading your own drafts is not optional — it is the step that separates outreach from spam.

## The rubric (100 points)
| Axis | Points | What earns them |
| --- | --- | --- |
| Grounded personalization | 30 | A dated, sourced signal appears in the first two sentences and drives the argument |
| Swap test | 20 | Pasting another lead's name breaks the message |
| Single ask | 15 | Exactly one CTA, phrased as a question, low friction |
| Length & rhythm | 15 | Under 150 words (email) / 600 characters (LinkedIn); mixed sentence lengths |
| Honesty | 10 | No invented number, customer, or shared history; no unearned claim |
| Voice | 10 | No corporate speak, no AI tells, sounds like one person writing to another |

## Steps
1. Resolve the campaign with `list_campaigns` when needed, then call `get_campaign` and `list_campaign_actions` — pull every draft.
2. `get_campaign_authoring_context` — you need the source signals to judge whether the personalization is real or hallucinated. **A message that references a signal not present in the context scores 0 on Honesty and is flagged, not fixed silently.**
3. Score every draft, axis by axis. Show the table.
4. **Rewrite everything under 70** with `update_campaign_action_draft`, then re-score. Two rewrites maximum — a third failure means the lead lacks a real signal, so flag it for removal instead.
5. **Campaign verdict:**
   - Median ≥ 80 and no honesty flags → ready for my approval
   - Median 70-79 → ship, but name the weakest axis so the next campaign fixes it upstream
   - Median < 70, or any honesty flag → do not present for approval; the problem is research, not copy
6. **Report.** Score distribution, worst axis, the 3 lowest drafts before/after, and any lead you recommend removing.

## Hard rules
- Never raise a score because a rewrite "feels better". The rubric decides.
- Never silently delete a flagged draft. Flagging is the deliverable.
