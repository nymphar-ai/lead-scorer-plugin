---
name: signal-audiences
description: >-
  Capture the people who engaged with a LinkedIn post or profile into a deduplicated Lead
  Scorer list, then enrich and qualify them. Use when the user mentions LinkedIn engagers,
  likers, reactors, commenters, post engagement, warm audiences, audience capture, or
  wants leads out of a post that performed.
---

# Signal audiences — engagers to pipeline

You have the "lead-scorer" MCP server connected (Lead Scorer CRM — endpoint https://mcp.lead-scorer.com/mcp, authenticated with Lead Scorer OAuth). Use its tools for CRM reads and writes. For public web research, use your host assistant's native web search and browsing, then save verified findings with the CRM tools. Do not delegate web search to Lead Scorer workflows or call its HTTP endpoints as a fallback: those searches incur server-side provider costs. If native search is unavailable, ask me to enable it or provide sources; do not silently switch to a paid backend search. Discover resource IDs with the available list/search tools; never guess or probe sequential IDs, and ask me when no discovery tool exists. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

## Goal
People who engage with relevant LinkedIn content are warm. Capture them as an audience, enrich them, and keep the source fresh.

## Steps
1. **Pick the signal.** A post URL of mine that performed, or a competitor/creator profile whose audience matches my ICP (`fetch_profile_posts` to find their top recent post).
2. **Capture.** `create_audience_source` with the post/profile — it lands engagers in a list. `list_audience_sources` first to avoid duplicating an existing source.
3. **Sync.** `sync_audience_source` resumes an unfinished capture or refreshes an exhausted source. Large post audiences continue automatically in batches, saving reactions and comments separately; poll `list_audience_sources` for status and next_sync_at instead of repeatedly launching syncs.
4. **Qualify.** `get_leads_from_list` on the audience list; enrich the ICP matches with `enrich_leads` (needs linkedin_url). Flag the top 10 with a one-line "why now" each.
5. **Report.** New engagers captured, ICP matches, and which ones deserve a campaign.

## Hard rules
- Engagement is a signal, not consent: qualification before any outreach decision.
- Reactions sometimes expose less profile data than comments — expect partial profiles and let enrichment fill the gaps.
