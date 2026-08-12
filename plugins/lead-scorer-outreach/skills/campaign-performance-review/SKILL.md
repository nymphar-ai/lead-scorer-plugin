---
name: campaign-performance-review
description: >-
  Read a campaign's numbers, name the single broken link (list, subject line,
  personalization or ask), and fix the drafts still queued. Use when the user mentions
  campaign results, open rate, reply rate, bounce rate, performance, a post-mortem, or
  asks why a campaign is not working.
---

# Campaign performance teardown

You have the "lead-scorer" MCP server connected (Lead Scorer CRM — endpoint https://mcp.lead-scorer.com/mcp, authenticated with Lead Scorer OAuth). Use its tools for every read and write. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

## Goal
Turn campaign <CAMPAIGN_ID>'s numbers into one named cause and one applied fix. "Improve the copy" is not a diagnosis.

## Steps
1. **Pull the state.** `get_campaign` and `list_campaign_actions` — sent, opened, replied, bounced, still queued, per touch. `get_leads_from_list` for the underlying list quality.
2. **Walk the ladder in order and stop at the first broken rung.** Fixing a later rung while an earlier one is broken wastes the campaign:
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
