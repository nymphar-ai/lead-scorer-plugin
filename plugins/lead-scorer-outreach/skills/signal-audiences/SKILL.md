---
name: signal-audiences
description: >-
  Capture, deduplicate and qualify LinkedIn audiences in Lead Scorer. Use for post/profile
  engagers (reactions, likes, comments), people searches, event participants, capture budgets/queues,
  connection-degree routing, or a prospect's saved event registrations.
---

# LinkedIn signal audiences

Use the authenticated `lead-scorer` MCP for CRM work; native search/browsing for public research. Save verified findings. Discover IDs through list/search tools; ask when discovery is unavailable. Never guess IDs or data; report empty results. OAuth is configured by the plugin; API keys are a manual fallback for clients without OAuth.

## Capture and qualify
1. Pick an ICP-relevant post/profile or people-search URL. `fetch_profile_posts` finds recent posts from the user, competitors or creators.
2. Check `list_audience_sources` and reuse matching sources. Inspect `list_sender_accounts` and estimate as described below, then `create_audience_source` to capture into a list.
3. Poll `list_audience_sources` for status and `next_sync_at`. Post captures continue automatically with separate reaction/comment cursors. Use `sync_audience_source` only on explicit capture/refresh requests; people-search limits follow below.
4. Load `get_leads_from_list`; enrich ICP matches with `enrich_leads` (requires `linkedin_url`). Reactions may yield partial profiles. Flag the top 10 with a one-line "why now".
5. Report new captures, ICP matches and campaign candidates. Engagement is a signal, not consent; qualify before outreach.

## Budgets and estimates
Discover budget/queue tools before use. If unavailable, explain the missing backend/MCP support and use existing list/sync tools.

- `list_sender_accounts` reports capture allowance, used/reserved/uncertain reads, campaign and total reads, and UTC reset. Campaign reads do not reduce capture allowance.
- Explicit `estimate_audience` reads at most one people-search page (up to 10 capture reads), with no enrichment credits. Report preview reads, capture and optional degree-read upper bounds, and remaining allowance; preview reads are separate from capture. Unknown totals have a lower bound, not an empty audience. Do not estimate on every URL edit or repeatedly retry timeouts.
- Classic people-search pages need 10 available reads. Higher daily quotas do not bypass LinkedIn's per-query result cap.
- A provider timeout is not exhausted quota. Saved pages remain captured; the cursor stays on the failed page. Retry the existing source within its authorized cap; avoid repeated retries and duplicates. An unknown outcome may count as one uncertain page, not a full day.

## Queue controls
`list_audience_sources` reports IDs, queue positions and current/before/after read budgets. One capture runs per connected account; the first eligible source finishes before the next.

- `pause_audience_source` preserves leads and cursor; `resume_audience_source` continues from that cursor.
- `reorder_audience_sources`: pass the complete ordered set of pending and paused sources for one discovered account; exclude active, idle and error sources.
- `delete_audience_source`: obtain human confirmation, then `confirm: true`. Only the source is removed; its list and leads remain.
- Active captures cannot be paused/deleted; wait for the current run to end.
- Before `update_sender_account`, agree `linkedin_daily_capture_read_limit` with the user and explain restriction risk: 1–10,000; `null` inherits the global setting.

## People-search limits
- `max_profiles`: default 100; 10–1,000 in multiples of 10. Scanned duplicates consume reads and count toward the cap.
- `scan_limit` and `profiles_scanned` persist across quota continuations, worker restarts and pause/resume. `limit_reached` stops capture; `continuation_available` indicates saved progress.
- `update_audience_source` sets the next batch's cap without starting work or enlarging the current allowance. An authorized `sync_audience_source` starts another configured batch from the saved cursor, or a fresh scan if exhausted. Never silently raise caps or repeatedly sync to bypass them.
- Report unavailable scan controls before broad searches, and unavailable degree fields without inventing data.

## Connection degrees
- Preserve degrees returned by captures without extra lookups. Select the sender's `linkedin_account_id`: `connection_degree` is account-specific. Show `connection_degree_observed_at`.
- Filter `get_leads_from_list` with `connection_degrees: [1]` for re-engagement, `[2, 3]` for cold outreach, or `connection_degree_unknown: true` for missing observations. Totals and pagination are filtered. Split saved results into lists or draft campaigns using existing add tools; do not recapture.
- Source `degrees` filters native people search before import. Preserve other criteria, including events. Opaque saved searches may need an explicit degree-filtered URL; never widen the search after that error.
- Missing degrees stay unknown; absence of a connection flag does not imply second/third degree. Never silently spend reads or launch imports/campaign refreshes to answer CRM questions.

### Optional missing-degree lookups
Present the additional-read estimate and per-run cap; obtain opt-in before setting `refresh_missing_degrees: true` and `degree_lookup_limit` (default 100, maximum 1,000) through `update_audience_source`. Settings persist until disabled; updating starts no capture. Explicit re-sync applies them. Post lookups require an explicitly selected owned `linkedin_account_id`.

These Unipile reads use the LinkedIn capture allowance without extra Lead Scorer credits; normal new-lead capture pricing still applies. Respect partial results, caps, quotas and provider errors; avoid repeated retries.

## Campaign preflight
Preflight may warn about leads already connected to the sender. Review follow-up copy before activation. Redundant invitations are skipped; the configured follow-up delay starts at bypass. New acceptances retain acceptance-based timing. Never claim skipped invitations were sent or activate without human review and approval.

## Event registrations
- Capture an event's LinkedIn participants URL with one `eventAttending` filter, including others' events. Reuse existing sources; normal import credits and LinkedIn read budgets apply.
- Discover the lead via lists, then `get_lead`. Report `event_registrations.items` with event links, source names and observation dates; paginate with `event_offset` through `total`. If absent, report history unavailable.
- Saved registration is not proof of attendance, current registration or acceptance of our invitation. List membership alone is not registration evidence.
