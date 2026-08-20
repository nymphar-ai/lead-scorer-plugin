---
name: podcast-transcripts-to-posts
description: >-
  Mine full podcast transcripts for operator insights and accurate quotes, then draft
  LinkedIn posts from what was actually said. Use when the user mentions podcasts,
  transcripts, episodes, repurposing audio or video content, or quoting a guest.
---

# Podcast transcripts → LinkedIn posts

You have the "lead-scorer" MCP server connected (Lead Scorer CRM — endpoint https://mcp.lead-scorer.com/mcp, authenticated with Lead Scorer OAuth). Use its tools for every read and write. Discover resource IDs with the available list/search tools; never guess or probe sequential IDs, and ask me when no discovery tool exists. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

## Goal
Turn newly stored podcast transcripts into LinkedIn drafts built on what was ACTUALLY said.

## Steps
1. **Discover.** `list_content_items` with item_type "podcast_episode", added today. Pick the 1-3 most relevant for my audience.
2. **READ THE FULL TRANSCRIPT** via `get_content_item` (include_transcript). NEVER write from the episode title: titles are marketing. (Real case: an episode titled "Founder-led sales" was actually a podcast-marketing retrospective — a title-based post would have been fiction.)
3. **Extract the operator insight** — the lesson a practitioner takes away, not an episode summary. If a transcript has no exploitable angle, skip it and say why.
4. **Write 1-2 posts per kept episode.** Name the guest and their role; translate their best formulas as near-verbatim quotes. Same voice rules as my other content skills: fact-first hook, one line of my lived experience, "so what?" test, no emoji, no em-dash, sincere closing question.
5. **Store.** `create_content_post`, status "draft", external_id "post:linkedin/<slug>".

## Hard rules
- A quote must exist in the transcript. Paraphrase honestly or quote exactly; never improve someone's words.
- Draft only; I review everything.
