---
name: deliverability-preflight
description: >-
  Check sender health, SPF, DKIM, DMARC, warmup, list quality and message shape before a
  campaign sends, then give a go or no-go verdict. Use when the user mentions
  deliverability, landing in spam, bounces, sending domain or subdomain, warmup, DMARC, or
  is about to launch a first campaign.
---

# Deliverability preflight

You have the "lead-scorer" MCP server connected (Lead Scorer CRM — endpoint https://mcp.lead-scorer.com/mcp, authenticated with Lead Scorer OAuth). Use its tools for every read and write. Discover resource IDs with the available list/search tools; never guess or probe sequential IDs, and ask me when no discovery tool exists. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

## Goal
Decide whether campaign <CAMPAIGN_ID> is safe to activate. Cold outreach that lands in spam is not underperforming, it is invisible — and it damages the domain for everything else.

## Steps
1. **Sender.** `list_sender_accounts` — which account sends, is it healthy, how long has it been connected, and is `signature_configured` true? If the signature is missing, the verdict is fix first: ask me for the exact block and save it once with `update_sender_account`; never invent sender identity. Report if the campaign would send from my primary business domain. **That is the one thing to avoid**: cold volume belongs on a dedicated sending subdomain or a separate domain.
2. **Authentication.** Verify SPF, DKIM and DMARC exist for the sending domain (public DNS lookup — this lives outside Lead Scorer, so check it and say what you found, or say plainly you could not).
3. **Warmup and ramp.** A domain younger than ~3 weeks of warmup should not carry a full campaign. Propose a ramp: start low, roughly double per week, and hold at a volume the mailbox can plausibly sustain as a human.
4. **List quality.** `get_leads_from_list` on the campaign list: what share has a real, individual, corporate address? Flag role addresses (contact@, info@, sales@), free-mail addresses, and leads with no email at all. Role and catch-all addresses are the main bounce source, and bounces above ~2% are a list problem, never a copy problem.
5. **Content check.** `list_campaign_actions` — flag drafts with images, tracked links stacked on a new domain, attachments, or more than one link. Plain text with at most one link is the safe shape for a first touch.
6. **Verdict.** Go / fix first / no-go, with the specific blocking item and who fixes it.

## Thresholds worth acting on
Bounce above 2% → stop and clean the list. Spam complaints above 0.1% → stop entirely, the targeting is wrong. Open rate under 25% with a healthy list → subject lines or placement, in that order.

## Hard rules
- Never advise sending cold volume from the primary domain, whatever the deadline.
- If you cannot verify DNS records, say so — do not report a check you did not run.
