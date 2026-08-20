---
name: ai-authored-campaign
description: >-
  Create a draft multichannel campaign in Lead Scorer with one genuinely personal message
  per lead, left for the user to review and activate. Use when the user mentions creating
  a campaign, drafting outreach for a whole list, a sequence for their leads, or wants an
  agent to write the messages for a list at once.
---

# AI-authored campaign drafts

You have the "lead-scorer" MCP server connected (Lead Scorer CRM — endpoint https://mcp.lead-scorer.com/mcp, authenticated with Lead Scorer OAuth). Use its tools for every read and write. Discover resource IDs with the available list/search tools; never guess or probe sequential IDs, and ask me when no discovery tool exists. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

## Goal
Create a DRAFT campaign for list <LIST_ID> where every lead gets a message written for them specifically. I activate in the Lead Scorer app; the agent never sends anything.

## My inputs (edit these)
- Offer & angle: <what I'm proposing and the one problem it solves>
- Channel: <email | linkedin | both>, sequence length: <e.g. 2 touches>
- Voice: <first-person, no marketing fluff, short sentences, one concrete question at the end>

## Steps
1. **Senders.** `list_sender_accounts` — confirm which account will send; stop if none is connected. For email, stop when `signature_configured` is false, ask me for the exact signature, then save it once with `update_sender_account`. Never invent sender identity.
2. **Create.** `create_campaign` (draft) + `add_leads_to_campaign` for the list. If an existing draft has no sender yet, attach it with `update_campaign_senders`. If it needs one more touch, append it with `add_campaign_step`; never rebuild or overwrite the reviewed steps.
3. **Author, lead by lead.** Call `get_campaign_authoring_context` — it returns each lead's enrichment, summary and insights. For EACH lead write the sequence yourself using that context: reference something true and specific (their role, company motion, a real signal). Push with `write_campaign_drafts`.
4. **Self-review.** `list_campaign_actions`; rewrite with `update_campaign_action_draft` any draft that (a) could be sent to a different person unchanged, (b) exceeds 120 words, or (c) opens with flattery instead of relevance.
5. **Handoff.** Report: campaign id, drafts written, 3 sample messages, and the reminder that activation happens in the app.

## Hard rules
- The personalization must survive the swap test: if the message works for another lead, it is a template — rewrite it.
- Never touch campaign status. Draft in, draft out.
