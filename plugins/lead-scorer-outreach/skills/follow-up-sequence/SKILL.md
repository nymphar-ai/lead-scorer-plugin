---
name: follow-up-sequence
description: >-
  Build a cold email follow-up cadence on day 1, 4, 9, 16, 25 and 35 where every touch
  carries a new angle and the last one is a breakup email. Use when the user mentions
  follow-ups, relances, an email sequence or cadence, multi-touch outreach, a breakup
  email, or says prospects go silent after the first email.
---

# Follow-up sequence with a real angle

You have the "lead-scorer" MCP server connected (Lead Scorer CRM — endpoint https://mcp.lead-scorer.com/mcp, authenticated with Lead Scorer OAuth). Use its tools for every read and write. Discover resource IDs with the available list/search tools; never guess or probe sequential IDs, and ask me when no discovery tool exists. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

> **Context first.** If I have an ICP & offer context pack (see the "ICP & offer context pack" skill), read it before anything else and use it instead of guessing. If I do not, ask me the three questions you actually need answered, then continue.

## Goal
Extend campaign <CAMPAIGN_ID> into a sequence where each follow-up would work as a standalone first email. Most replies come from touches 2-5, so this is where the campaign is won or lost.

## Cadence (gaps grow, on purpose)
| Touch | Day | Angle |
| --- | --- | --- |
| 1 | 1 | The signal-based first touch |
| 2 | 4 | New evidence — a case, a number, a resource they can use without replying |
| 3 | 9 | A different pain the same buyer owns |
| 4 | 16 | An industry insight or a pattern I see across their segment |
| 5 | 25 | One direct question, three lines maximum |
| 6 | 35 | Breakup |

## Steps
1. Resolve the campaign with `list_campaigns` when its ID is unknown, then call `get_campaign` + `get_campaign_authoring_context` — read the first touch already written for each lead. Follow-ups must not repeat its argument. Append each missing touch in order with `add_campaign_step`, using a stable idempotency key per campaign + target day and `condition=if_no_reply`; never recreate the campaign or overwrite an existing step.
2. **Assign an angle per touch before writing.** If you cannot name the angle in four words, do not write the email.
3. **Write each follow-up standalone**: it must make sense to someone who never opened email one. Never open with "following up on my previous email" or "circling back".
4. Reload `get_campaign_authoring_context`, then push the returned new `step_order` drafts with `write_campaign_drafts`; review with `list_campaign_actions` and fix with `update_campaign_action_draft`.
5. **The breakup (touch 6)** does three things: closes the loop without guilt, leaves the door open, and asks for a redirect ("if someone else owns this, a name would help"). Keep it under 60 words.
6. **Exit rules — state them explicitly in the report:** stop on any reply, on an unsubscribe, on a bounce, or when touch 6 is sent. Never restart a lead who said no.

## Hard rules
- Each follow-up shorter than the one before. Touch 5 is three lines.
- "Just checking in", "bumping this to the top of your inbox", "did you see my last email" — these are not follow-ups, they are noise. Never write them.
- Draft only. Activation and sending happen in the app, by me.
