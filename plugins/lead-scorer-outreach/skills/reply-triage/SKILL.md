---
name: reply-triage
description: >-
  Classify a prospect's reply as interested, timing, wrong person, objection or no, then
  draft the one response that moves it forward. Use when the user pastes a reply, mentions
  inbox triage, handling responses, objection handling, a prospect who said no or not now,
  or asks how to answer a lead.
---

# Reply triage & response drafting

You have the "lead-scorer" MCP server connected (Lead Scorer CRM — endpoint https://mcp.lead-scorer.com/mcp, authenticated with Lead Scorer OAuth). Use its tools for every read and write. Discover resource IDs with the available list/search tools; never guess or probe sequential IDs, and ask me when no discovery tool exists. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

> **Context first.** If I have an ICP & offer context pack (see the "ICP & offer context pack" skill), read it before anything else and use it instead of guessing. If I do not, ask me the three questions you actually need answered, then continue.

## Goal
I paste a reply (or point you at a lead). You pull the context, classify it, and draft my answer. You never send.

## Steps
1. **Context.** `get_lead` for the person; resolve an unknown campaign with `list_campaigns`, then use `get_campaign` + `list_campaign_actions` for what we actually sent them and when. Read our own message before answering theirs — half of bad replies come from forgetting what we said.
2. **Classify** into exactly one bucket:
   - **Interested** — wants to talk or asks a real question
   - **Timing** — relevant but not now ("Q1", "after the migration")
   - **Wrong person** — redirect offered or implied
   - **Objection** — price, incumbent, built in-house, no budget
   - **No** — explicit refusal or unsubscribe
   - **Auto** — out of office, bounce, no-reply noise
3. **Draft the response** by bucket:
   - Interested → confirm one concrete next step, propose two time slots, no re-pitch.
   - Timing → accept the timing without arguing, ask for the trigger to watch, propose one dated follow-up.
   - Wrong person → ask for the name, and thank them properly; that is the whole message.
   - Objection → answer the actual objection in one paragraph, no defensive list of features, close with a question about their situation.
   - No → one line, gracious, no rebuttal. Then stop.
   - Auto → no reply; note the return date.
4. **Record.** `add_tags_to_lead` with the bucket so the pipeline reflects reality. Use `update_campaign_action_draft` if a queued follow-up must be replaced by the response.
5. **Report.** Bucket counts, the drafts, and every lead that must exit the sequence today.

## Hard rules
- One question per reply. Two questions is an interview, and it stalls.
- Never re-sequence someone who said no. Never argue with a no.
- Never claim we already spoke, or that they asked for something they did not.
