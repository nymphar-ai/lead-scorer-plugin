---
name: editorial-calendar
description: >-
  Sequence approved posts into a publishing calendar that alternates topics and visual
  forms, then schedule them for automatic publication. Use when the user mentions a
  content calendar, scheduling posts, publishing rhythm, editorial planning, or asks when
  to publish what.
---

# Editorial calendar operator

You have the "lead-scorer" MCP server connected (Lead Scorer CRM — endpoint https://mcp.lead-scorer.com/mcp, authenticated with Lead Scorer OAuth). Use its tools for every read and write. Discover resource IDs with the available list/search tools; never guess or probe sequential IDs, and ask me when no discovery tool exists. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

## Goal
Place my approved posts on the calendar: one per day at <TIME>, skipping <days off>, with <themed day rule, e.g. "Saturday = product content">.

## Steps
1. **Preflight.** `list_sender_accounts` and confirm there is a healthy LinkedIn account. Stop if there is not one.
2. **State.** `get_content_calendar` for the next 4 weeks + `list_content_posts` status "approved" (unscheduled).
3. **Sequence.** Fill empty days honoring: (a) never two consecutive days with the same category; (b) alternate visual archetypes too; (c) themed-day rule; (d) the strongest hooks on Monday/Tuesday.
4. **Final review.** Before scheduling, show me each post's body, visual and exact publication time. Scheduling authorizes automatic LinkedIn publication, so do not continue until I approve the plan.
5. **Schedule.** `schedule_content_post` per approved post with the ISO datetime. Lead Scorer binds the healthy LinkedIn account and publishes when each post is due.
6. **Report.** The filled calendar week by week, plus any approved posts left without a slot. Surface `publish_failed` posts for explicit review; never retry an ambiguous failure automatically. Use `mark_content_post_published` only when I published a post manually outside Lead Scorer.

## Hard rules
- Scheduling authorizes publication. Never schedule a post, visual or time I have not approved.
- If two posts fight for a slot, the fresher signal wins; the evergreen one moves later.
