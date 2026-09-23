---
name: campaign-performance-review
description: >-
  Read a campaign's numbers, name the single broken link (list, subject line,
  personalization or ask), and fix the drafts still queued. Use when the user mentions
  campaign results, click rate, open rate, reply rate, bounce rate, performance, a post-mortem, or
  asks why a campaign is not working.
---

# Campaign performance teardown

You have the "lead-scorer" MCP server connected (Lead Scorer CRM — endpoint https://mcp.lead-scorer.com/mcp, authenticated with Lead Scorer OAuth). Use its tools for CRM reads and writes. For public web research, use your host assistant's native web search and browsing, then save verified findings with the CRM tools. Discover resource IDs with the available list/search tools; never guess or probe sequential IDs, and ask me when no discovery tool exists. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

## Goal
Turn campaign <CAMPAIGN_ID>'s numbers into one named cause and one applied fix. "Improve the copy" is not a diagnosis.

## Steps
1. **Pull the state.** Resolve the campaign with `list_campaigns` when needed, then call `get_campaign` and `list_campaign_actions` — sent, clicked, replied, bounced, still queued, per touch. Read `analytics.clicks` and each `analytics.steps[].clicks`: `total` counts unique email actions with a qualified click, `tracked` counts sent emails containing tracked links, and `rate` is `total / tracked` (null with no tracked emails). Actions expose `clicked_at` (first accepted click) and `click_tracking_enabled`. Count an action once across repeated links and visits. These fields require the NYM-1511 deployment; if absent, report click tracking as unavailable. Historical sends and emails without rewritten links cannot be backfilled; null `clicked_at` on an untracked action is unknown engagement, not zero interest. Only future sends with `tracking.clicks` enabled can add tracked links. Immediate clicks, known scanner user agents and prefetch requests are filtered heuristically; remaining clicks do not prove human intent. `get_leads_from_list` for the underlying list quality.
2. **Walk the ladder in order and stop at the first broken rung.** Never infer an open rate from a click, or treat a configured open-tracking flag as collected data. Skip diagnostics requiring metrics the tools do not provide. Qualified clicks with few replies can justify inspecting the destination page or call to action, but do not establish why recipients abandoned it. Fixing a later rung while an earlier one is broken wastes the campaign:
   - **Bounces > 2%** → list quality. Stop; go back to sourcing and enrichment.
   - **Open rate < 25%** with clean delivery → subject lines, or placement. Test subjects before touching the body.
   - **Reply rate < 3%** with healthy opens → the message. Almost always the personalization level, not the wording: check whether drafts used level 1-2 signals or fell back to segment truths.
   - **Replies but no meetings** → the ask. Too much friction, or the wrong next step for that seniority.
   - **Mostly "not now"** → timing and trigger choice, not copy. Change which signal you source on.
3. **Compare the top and bottom deciles.** Read the 5 best-performing messages and the 5 worst. What is structurally different? Name it in one sentence.
4. **Apply the fix to what has not gone out yet** with `update_campaign_action_draft`. A teardown that only produces advice changes nothing.
5. **Tag the outcome** on the leads (`add_tags_to_lead`) so segments stay honest across campaigns.
6. **Report.** Metric table, the one named cause, what you changed, and the single thing to do differently on the next campaign.

## Hard rules
- One cause per teardown. If you list five, you have not diagnosed anything.
- Small numbers lie: below ~50 sends, say the sample is too small instead of inventing a trend.
- Never change more than one variable between two campaigns, or the next teardown is unreadable.
