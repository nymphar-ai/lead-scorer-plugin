---
name: contact-discovery
description: >-
  Find verified emails and phone numbers, but only for leads already confirmed as ICP and
  about to be contacted — the most expensive call in the platform, spent last and on
  purpose. Use when the user mentions trouver les emails, contact discovery, find emails,
  enrichir les contacts, FullEnrich, or asks why a run consumed so many credits.
---

# Contact discovery (spend last)

You have the "lead-scorer" MCP server connected (Lead Scorer CRM — endpoint https://mcp.lead-scorer.com/mcp, authenticated with Lead Scorer OAuth). Use its tools for every read and write. Discover resource IDs with the available list/search tools; never guess or probe sequential IDs, and ask me when no discovery tool exists. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

> **Context first.** If I have an ICP & offer context pack (see the "ICP & offer context pack" skill), read it before anything else and use it instead of guessing. If I do not, ask me the three questions you actually need answered, then continue.

## Goal
Find contact details for list <LIST_ID> — and only for the leads that survived scoring and enrichment and are going into a campaign now.

## Why this one runs last
`find_lead_contact_info` is the most expensive call in the platform: **3 credits per email FOUND, 15 per phone number found**. A lead the provider cannot resolve costs nothing; an address served from our cache counts as found and is charged normally. Scoring is free, enrichment is about 1 credit a lead. So the order is not a style preference, it is where the money goes.

The full amount is reserved when you call, then the unused part is refunded once the lookups report back a few minutes later. Your balance therefore dips by the worst case and recovers — do not read the first figure as the bill.

The failure mode is well documented: a run that finds emails for a whole list before deciding who is worth contacting spends roughly 8 credits per usable contact. Running score → enrich → contact, in that order, brings it close to 1. Same leads, same outcome, a fraction of the spend.

An email found for a lead nobody writes to is not an asset. It is 3 credits, gone.

## Steps
1. **Confirm the shortlist.** `get_leads_from_list` filtered to the leads that scored well AND are enriched AND are going into this campaign. If you cannot name the campaign, stop — you are not ready to spend.
2. **Estimate first.** `find_lead_contact_info` with `dry_run: true`. It returns the worst-case cost (every lead resolving) and your balance, spends nothing, runs nothing. Show me the figure before proceeding, and say it is a ceiling.
3. **Ask before a large spend.** Above the account threshold the call refuses without `confirm: true`, and says what it would have cost. Do not pass `confirm` to make an error go away — come back to me with the number.
4. **Email before phone.** A phone number costs five times an email. Only look for one if the sequence actually calls.
5. **Collect asynchronously.** Results land minutes later. Re-read with `get_leads_from_list` rather than assuming a failure and re-running — a re-run is a second charge.
6. **Report.** Leads targeted, credits reserved, credits actually kept after settlement, emails found, and the ratio of credits per contact obtained.

## Hard rules
- Never on a whole list. Only on a named shortlist headed for a named campaign.
- Never without a `dry_run` first.
- Never re-run a lookup because results have not arrived yet.
- A refusal from the spend guardrail is information, not an obstacle: report it, do not route around it.
