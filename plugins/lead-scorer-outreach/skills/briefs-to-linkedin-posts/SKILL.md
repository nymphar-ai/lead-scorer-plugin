---
name: briefs-to-linkedin-posts
description: >-
  Turn editorial briefs into human-sounding LinkedIn draft posts with fact-first hooks,
  varied structures and no AI tells. Use when the user mentions writing LinkedIn posts,
  content drafts, turning research into posts, post hooks, or complains that their posts
  sound AI-generated.
---

# Briefs → LinkedIn posts

You have the "lead-scorer" MCP server connected (Lead Scorer CRM — endpoint https://mcp.lead-scorer.com/mcp, authenticated with Lead Scorer OAuth). Use its tools for every read and write. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

## Goal
Turn today's fresh editorial briefs into LinkedIn draft posts in my voice, ready for MY review.

## Steps
1. **Discover.** `list_content_items` filtered on item_type "brief" and today's date. If none, stop cleanly.
2. **Read ENTIRELY.** `get_content_item` — the value lives in the Interpretation and Raw material sections, not the TL;DR.
3. **Write 1-3 posts per brief** — one per genuinely distinct thesis. Never pad to hit a count.
4. **Store.** `create_content_post` per post: status "draft", external_id "post:linkedin/<slug>" (idempotent), category = the brief's topic.

## Voice rules (hard)
- **Hook = a fact, never a theory.** Line 1 carries a number, a name, a date or a scene. "Ford just rehired 350 veteran engineers." beats "AI is a multiplier."
- **One line of lived operator experience** — something only I could write (what I see in companies, a pattern from my work). Never fabricate clients or numbers.
- **Length = the "so what?" test**, not a word cap. Every sentence must add a fact, a tension, or lived experience; cut the rest.
- **Vary the structure across the batch**: reframing, scene, two-numbers collision, cost-vs-asset, case study, contrarian, stat teardown. Never two posts in a row from the same mold.
- Zero emoji. Zero em-dash (—). Short and long sentences mixed. External links go in a comment, never the body.
- **End with a sincere question about the reader's situation** — never "comment below" bait.

## Hard rules
- Draft only. I schedule and publish myself.
- Re-running the same day must update the same posts (external_id), not duplicate them.
