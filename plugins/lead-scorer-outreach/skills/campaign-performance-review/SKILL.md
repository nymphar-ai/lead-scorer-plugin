---
name: campaign-performance-review
description: >-
  Diagnose campaign results and fix queued drafts in Lead Scorer. Use for open/click/reply/bounce
  rates, underperforming campaigns, post-mortems, cancelling queued messages or removing
  follow-up steps.
---

# Campaign review and cancellation

Use the authenticated `lead-scorer` MCP for CRM work; native search/browsing for public research. Save verified findings. Discover IDs through list/search tools; ask when discovery is unavailable. Never guess IDs or data; report empty results. OAuth is configured by the plugin; API keys are a manual fallback for clients without OAuth.

For cancellation requests, go directly to the cancellation section. For performance reviews, identify one cause and apply one fix.

## Review performance
1. Resolve the campaign with `list_campaigns`, then read `get_campaign` and `list_campaign_actions`: sent, clicked, replied, bounced and queued, per touch. Apply the email-click rules below. Check list quality with `get_leads_from_list`. For `event_invite` steps, use the event metrics below instead of the cold-email ladder.
2. Skip diagnostics with unavailable metrics. Clicks and enabled open-tracking flags do not establish measured opens. Stop at the first broken rung:
   - Bounces > 2%: list quality; stop and revisit sourcing/enrichment.
   - Opens < 25% with clean delivery: subject lines or placement; test subjects before the body.
   - Replies < 3% with healthy opens: personalization; check level 1–2 signals versus generic segment truths.
   - Replies without meetings: ask friction or a next step unsuited to the recipient's seniority.
   - Mostly "not now": timing; change the sourcing trigger.
3. Compare the five best and five worst messages; name their structural difference in one sentence.
4. Apply the fix to unsent drafts with `update_campaign_action_draft`.
5. Tag outcomes with `add_tags_to_lead`. Report the metric table, cause, applied change and one adjustment for the next campaign.

Below ~50 sends, report insufficient data instead of inventing a trend. Keep one cause per teardown and change only one variable between campaigns.

## Email click metrics
- Read `analytics.clicks` and `analytics.steps[].clicks`: `total` counts unique clicked email actions; `tracked` counts sent emails with tracked links; `rate = total / tracked`, null when `tracked = 0`. Missing fields mean unavailable.
- `clicked_at` is the first accepted click; `click_tracking_enabled` shows link coverage. Count each action once across repeated links/visits. Null timestamps on untracked/historical emails mean unknown engagement, not zero interest.
- Only future sends with `tracking.clicks` enabled get rewritten links; no historical/untracked backfill.
- Immediate clicks, known scanner user agents and prefetches are filtered heuristically. Remaining clicks do not prove human intent.
- Clicks with few replies warrant inspecting the destination page/CTA, not asserting abandonment causes.

## Cancel queued messages or steps
Check tool availability first. If unavailable, report the limitation; never remove enrolled leads or extend delays as a cancellation workaround.

- **One message:** discover `action_id` with `list_campaign_actions`; show its body and send date. After explicit confirmation, call `cancel_campaign_action` with `confirm: true`. Only scheduled, needs_review or approved actions can be cancelled; sending, unknown or sent actions cannot. The lead, step and sent history remain.
- **Entire follow-up step:** discover `step_id` with `get_campaign`, then call `preview_campaign_step_deletion`. Show waiting-action count, dated-action count and date range. After explicit confirmation, call `delete_campaign_step` with `confirm: true`. Waiting actions are cancelled and successors reconnect; sent history, statistics and enrolled leads remain. Resolve sending or unknown outcomes before deleting the step.

## Event invitation metrics
- For `event_invite` steps, read cached `analytics.event_registrations`: `registered / invited`, conversion rate, `cohort_at` and `refreshed_at`. This matches visible registrations to unique people with confirmed sent invitations; it does not prove acceptance of our invitation or attendance. Never substitute reply/connection rates or apply the cold-email ladder.
- Null rates, missing snapshots or absent fields mean unavailable, not 0%. Failed refreshes may retain older results; report their date and status. `get_campaign` reads only cached statistics. Only the user clicks the deployed UI's **Refresh registrations** button. Never refresh through MCP, automate/schedule refreshes or invent a daily quota.
- For a prospect's history, discover their ID through the campaign/list, then read `get_lead.event_registrations`. Paginate with `event_offset`; report observation dates and sources. If absent, report unavailable. Captured external events do not establish current registration or attendance. CRM reads never refresh LinkedIn.
