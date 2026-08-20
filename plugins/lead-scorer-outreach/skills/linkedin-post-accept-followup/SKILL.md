---
name: linkedin-post-accept-followup
description: >-
  Write the LinkedIn message sequence that runs once a connection is accepted: value first
  with no ask, then two distinct angles, then a clean stop. Use when the user mentions
  LinkedIn DMs, messaging new connections, post-accept follow-up, LinkedIn sequences, or
  asks what to say after someone accepts their invite.
---

# Post-accept LinkedIn follow-up

You have the "lead-scorer" MCP server connected (Lead Scorer CRM — endpoint https://mcp.lead-scorer.com/mcp, authenticated with Lead Scorer OAuth). Use its tools for every read and write. Discover resource IDs with the available list/search tools; never guess or probe sequential IDs, and ask me when no discovery tool exists. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

> **Context first.** Call `get_my_memory`, then `compile_context_pack` when a lead or campaign is in scope. Treat personal memory as user-owned context, not verified public CRM data. If my memory is empty, ask me the three questions you actually need answered, then continue.

## Goal
Write the sequence that runs after someone accepts my connection request. The accept is permission to talk, not permission to pitch.

## Cadence
| Touch | When | Job of the message |
| --- | --- | --- |
| 1 | Accept + 2 days | Continue the thread the note opened. Give something — an observation, a resource, a question about their situation. No ask. |
| 2 | + 5 days | A different angle: a pattern I see in their segment, or a concrete result from a comparable company. One low-friction question. |
| 3 | + 12 days | Close the loop. Name that I will stop, leave the door open, offer the redirect. |

## Steps
1. `get_lead` and `get_lead_posts` to recover the signal used in the connection note and check whether anything changed since (new post, new role — that becomes touch 1).
2. Resolve the campaign with `list_campaigns` when its ID is unknown, then call `get_campaign_authoring_context` for the enrichment and insights; write each touch per lead, never as a template.
3. Push with `write_campaign_drafts`, review with `list_campaign_actions`, fix with `update_campaign_action_draft`.
4. **Report** the sequence per lead with the angle of each touch named in four words.

## Writing rules
- 400-600 characters per message. LinkedIn is a chat window, not an inbox.
- Touch 1 contains no ask at all. If you cannot give something without asking, the lead was not ready for a connection request.
- No voice notes, no attachments, no calendar link before touch 2.
- Never open with "Thanks for connecting!" followed by a pitch. That is the single most ignored message on the platform.

## Hard rules
- Stop the sequence on any reply — hand it to the reply-triage skill.
- Three touches maximum, then the lead exits. Silence after three is an answer.
- Draft only. I send.
