---
name: contact-discovery
description: >-
  Find emails or phone numbers for qualified, campaign-ready Lead Scorer leads; verify
  saved CRM emails separately. Use for contact discovery, FullEnrich, trouver les emails,
  enrichir les contacts, vérifier les emails existants, or contact-lookup credit usage.
---

# Contact discovery and email verification

Use the authenticated `lead-scorer` MCP for CRM work; native search/browsing for public research. Save verified findings. Discover IDs through list/search tools; ask when discovery is unavailable. Never guess IDs or data; report empty results. OAuth is configured by the plugin; API keys are a manual fallback for clients without OAuth.

For saved-email verification, use the verification section. For discovery, score → enrich → contact: only qualified, enriched leads in a named shortlist for a named campaign. If the campaign is unknown, stop before spending.

For campaign context, call `get_my_memory`, then `compile_context_pack` when a lead/campaign is in scope. Personal memory is user-owned context, not verified public CRM evidence. If empty, ask the three questions needed to continue.

## Discover contacts
1. Confirm the shortlist with `get_leads_from_list`: scored ICP matches, enriched and going into this campaign. Choose `contact_type: email`; use `phone` only if the sequence includes calls.
2. Call `find_lead_contact_info` with `dry_run: true` and the complete shortlist (up to 1,000 leads). It checks eligibility and returns the maximum cost and balance without running lookups or spending. Show the estimate as a ceiling.
3. Above the account's confirmation threshold, obtain approval for that amount before passing `confirm: true`. Report a spend-guard refusal; never bypass it or use confirmation merely to clear an error.
4. Submit the shortlist once; never loop one call per lead. Existing professional addresses may be reused; use `refresh: true` only for an intentional fresh lookup. Results may include personal addresses.
5. Poll the returned `run_id` with `get_contact_enrichment_run` until completed/failed; use `list_contact_enrichment_runs` to recover IDs after a restart. Read contacts from the CRM afterward. Delayed results never justify resubmission: another lookup can incur another charge.
6. Report leads targeted, credits reserved and settled, emails/phones found, failures and credits per contact obtained.

## Discovery billing
- **3 credits per lead with an email result; 15 per lead with a phone result**, including reused contacts. No result means no charge. A phone lookup costs five times an email lookup.
- The maximum is reserved upfront; unused credits are refunded after completion. The initial balance drop is not the final bill.

## Verify saved emails
Use `verify_lead_emails`, never FullEnrich/contact discovery, when the request concerns existing CRM emails.

- Discover IDs with `get_lead_lists` and `get_leads_from_list`, then read `get_lead`. Call `verify_lead_emails` with `lead_id` and `dry_run: true`: it checks lead/contact access, visible emails and provider configuration without spending or calling the provider. It cannot guarantee live provider availability.
- Verify only emails accessible to the authenticated account. Cost: **1 credit per successful lead verification**, regardless of email count; failures are refunded. Apply the confirmation rule above.
- Read `verification_status`, `verification_provider` and `verified_at` through `get_lead`. Reads are free; repeating verification is another paid operation. Report inaccessible leads, missing email access, no visible emails, insufficient credits or provider unavailability explicitly.
