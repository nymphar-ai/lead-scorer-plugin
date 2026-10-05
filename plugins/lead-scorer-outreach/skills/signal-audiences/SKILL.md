---
name: signal-audiences
description: >-
  Capture the people who engaged with a LinkedIn post or profile into a deduplicated Lead
  Scorer list, then enrich and qualify them. Use when the user mentions LinkedIn engagers,
  likers, reactors, commenters, post engagement, warm audiences, audience capture, or
  wants leads out of a post that performed, or wants to see which events a prospect registered for.
---

# Signal audiences — engagers to pipeline

You have the "lead-scorer" MCP server connected (Lead Scorer CRM, authenticated with Lead Scorer OAuth at the endpoint configured by the installed plugin). Use its tools for CRM reads and writes. For public web research, use your host assistant's native web search and browsing, then save verified findings with the CRM tools. Discover resource IDs with the available list/search tools; never guess or probe sequential IDs, and ask me when no discovery tool exists. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

## Goal
People who engage with relevant LinkedIn content are warm. Capture them as an audience, enrich them, and keep the source fresh.

## Steps
1. **Pick the signal.** A post URL of mine that performed, or a competitor/creator profile whose audience matches my ICP (`fetch_profile_posts` to find their top recent post).
2. **Plan the capture.** `list_sender_accounts` reports capture budget, reserved and uncertain reads, campaign reads, total reads and the UTC reset. Campaign reads do not reduce the capture allowance. Discover `estimate_audience` before using it: an explicit estimate reads at most one people-search page (up to 10 capture reads), costs no enrichment credits, and returns a provider total or an unknown total with a lower bound. Missing totals never mean an empty audience. Do not run estimates on every URL edit or repeatedly retry a timeout. These queue/quota tools require the audience-budget backend/MCP release; if discovery does not list them, explain their unavailability and use the existing list/sync tools.
3. **Capture.** `create_audience_source` with the post/profile — it lands engagers in a list. `list_audience_sources` first to avoid duplicating an existing source.
4. **Sync.** `sync_audience_source` resumes an unfinished capture or refreshes an exhausted source. Large post audiences continue automatically in batches, saving reactions and comments separately; poll `list_audience_sources` for status and next_sync_at instead of repeatedly launching syncs.
5. **Control the queue.** `list_audience_sources` returns source IDs, queue positions and current/read-before/read-after budgets. One capture runs per connected account; the first eligible source finishes before the next. `pause_audience_source` preserves captured leads and cursor; `resume_audience_source` resumes that cursor. `reorder_audience_sources` requires the complete ordered set of pending and paused sources for one discovered account, excluding active, idle and error sources. `delete_audience_source` requires human confirmation (`confirm: true`), removes only the source, and keeps its list and leads. Pause/delete refuse active captures: wait until their current run ends. Before changing `linkedin_daily_capture_read_limit` through `update_sender_account` (1–10,000, null inherits the global setting), agree the value with the user and explain the account restriction risk. Ten available reads are needed to fetch a classic people-search page. A higher daily quota does not bypass LinkedIn's per-query result cap.
6. **Qualify.** `get_leads_from_list` on the audience list; enrich the ICP matches with `enrich_leads` (needs linkedin_url). Flag the top 10 with a one-line "why now" each.
7. **Report.** New engagers captured, ICP matches, and which ones deserve a campaign.

## Event registrations in the CRM
- For an event, use its LinkedIn participants people-search URL with one `eventAttending` filter, including events organized by others. Reuse the existing audience source; importing it retains the import's normal credits and LinkedIn read budget.
- After discovering the lead through your lists, read `get_lead`. If `event_registrations` is available, report its `items` with the event links, source names and observation dates. Read further pages with `event_offset` until the `total` observations have been covered. If the field is absent on an older deployment, report this history as unavailable.
- This is saved registration evidence, not proof of attendance, current registration or acceptance of our particular invitation. List membership alone is not registration evidence. Never silently launch an import or campaign refresh just to answer a CRM read.

## Hard rules
- Engagement is a signal, not consent: qualification before any outreach decision.
- Reactions sometimes expose less profile data than comments — expect partial profiles and let enrichment fill the gaps.

- A provider timeout is different from exhausted quota. Saved pages remain in the list and the cursor stays on the failed page; retry the existing source instead of creating a duplicate. An unknown request outcome can count as one uncertain page, not a full day.
