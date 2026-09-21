---
name: sales-navigator-lookalikes
description: >-
  Turn a Lead Scorer list of known-good customers or leads into calibrated, browser-tested
  LinkedIn Sales Navigator searches for finding more similar profiles. Use when the user
  mentions Sales Navigator, lookalikes, more leads like these, reverse-engineering an
  existing customer list, or converting a proven list into filters and Boolean queries; do
  not use for net-new vertical discovery without positive examples.
---

# Sales Navigator lookalikes

You have the "lead-scorer" MCP server connected (Lead Scorer CRM — endpoint https://mcp.lead-scorer.com/mcp, authenticated with Lead Scorer OAuth). Use its tools for CRM reads and writes. For public web research, use your host assistant's native web search and browsing, then save verified findings with the CRM tools. Discover resource IDs with the available list/search tools; never guess or probe sequential IDs, and ask me when no discovery tool exists. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

> **Context first.** Call `get_my_memory`, then `compile_context_pack` when a lead or campaign is in scope. Treat personal memory as user-owned context, not verified public CRM data. If my memory is empty, ask me the three questions you actually need answered, then continue.

## Goal
Turn a Lead Scorer list of customers or leads I already consider valuable into repeatable LinkedIn Sales Navigator searches for finding more of the same kind. Infer from the examples; do not replace them with a generic ICP template.

This skill produces search strategy only. It does not scrape LinkedIn, import results, enrich contacts, create a campaign or send outreach.

## Steps
1. **Resolve the positive cohort.** Use `get_lead_lists` instead of guessing an ID, then read the full selected list with paginated `get_leads_from_list` calls. Confirm why the cohort is considered positive. If the list mixes customers, rejected leads and unreviewed imports, separate or label them before drawing conclusions.
2. **Read the commercial context.** Call `get_my_memory`, then `compile_context_pack` for the product or operation when one is in scope. Treat the positive cohort as evidence of fit and the context pack as an explanation of the offer; call out contradictions instead of silently choosing one.
3. **Measure observable patterns.** Report counts and denominators for current titles, decision level, geography, company size, industry, agency/freelance/company type, client audience, service keywords, acquisition channels and delivery model. Report missingness for every field used as a potential filter. Use `get_lead` only when list data does not contain enough existing context; never enrich just to build the search.
4. **Find cohorts, not an average persona.** Split materially different groups when their filters conflict — for example agencies versus freelancers, founders versus specialist operators, or companies with LinkedIn pages versus solo consultants. One forced query is worse than two saved searches when it erases a valid segment.
5. **Translate evidence into Sales Navigator.** For each cohort provide:
   - filters with exact values for lead Geography, Company headquarters location, Seniority level, Company headcount and Industry where supported;
   - a short copy-ready Boolean string for the keyword field;
   - Current job title values only when native Seniority filters cannot express the cohort, preferring individual native values over a second long Boolean expression;
   - exclusions that remove a business model, not words that may merely describe the prospect's customers;
   - a broad coverage version and a stricter high-precision version when both are useful.
6. **Respect the current search contract.** Verify current filter names and Boolean syntax against official LinkedIn Sales Navigator help, but do not treat the documented operator limit as proof that a query works. Use uppercase `AND`, `OR`, `NOT`, straight quotes, parentheses and no wildcards. Start with at most five Boolean operators in Keywords. Expand only after a live test still returns useful results. Never combine a long Boolean Current job title with a long Keywords expression; use native Seniority filters or split the motion into several saved searches.
7. **Test incrementally in a connected browser.** When a signed-in Sales Navigator browser is available, a final search must be tested there before delivery:
   - preserve the original search URL so the state can be restored unless the user asked to keep the result open;
   - establish a baseline using only company size and location filters;
   - add one short Keywords expression and record the new result count;
   - add native Seniority, Industry and Geography filters one group at a time, recording the count after every group;
   - if one addition drops the search to zero, remove only that last addition and shorten or split it;
   - inspect the first visible page, not just the count. Name the obvious true positives and false positives that justify the final filters.
   If no connected browser is available, label the queries **provisional and untested** and provide this same incremental test order. Never say a query works because its syntax merely looks valid.
8. **Distinguish company from person geography.** Company headquarters in France does not mean the lead is in France. Apply both Company headquarters location and lead Geography when the person must be local. Likewise, use Company headcount for agencies but leave it empty for a freelancer cohort whose company data is often missing.
9. **Prefer native precision filters.** Use Owner/Partner and Executive seniority before Director when targeting agency principals; Director often introduces internal operators and unrelated project roles. Add Industry only to the strict version and inspect the false negatives, because valid agencies are frequently uncategorized or misclassified. A useful search can be a family of short saved searches by motion — outbound, ABM/demand generation, cold email/LinkedIn — rather than one fragile mega-query.
10. **Back-test every proposed filter.** Estimate how many source positives each filter would retain, name the examples it would wrongly exclude, and explain whether the loss comes from a real mismatch or missing/misclassified LinkedIn data. If a headcount or industry filter loses more than 20% of positives mainly because the field is missing or dirty, make it optional or create a separate search.
11. **Add the qualification gate.** Give 4-6 observable weighted criteria for reviewing new results, score bands for accept/review/reject, and hard disqualifiers. A result enters only a staging list until its business model and role are confirmed; contact discovery and campaign enrollment remain separate decisions.
12. **Report the reusable package.** Return: source cohort and confidence · observed ICP with counts · searches by cohort · live-test funnel or explicit untested warning · first-page precision observations · back-test coverage · exclusions · qualification rubric · suggested saved-search and staging-list names.

## Hard rules
- Ten confirmed positive examples are the preferred minimum. With fewer, still help but label the output low-confidence and avoid narrow filters.
- A list proves what has worked; it does not prove that every absent trait is a disqualifier.
- Never make Industry or Company headcount mandatory merely because the filter exists. LinkedIn classifications are often absent or wrong.
- Do not use broad exclusions such as `NOT SaaS` when valid agencies may mention SaaS as a customer vertical. Exclude software vendors by their actual offer or company, not by incidental profile language.
- Do not mistake a blue `+ <value>` suggestion for an active filter; active selections appear as removable filter values. Read the actual query state before diagnosing a zero-result search.
- A result count is not a relevance test. Inspect at least the first visible page and tighten filters when obvious internal employees or unrelated businesses dominate it.
- Saving a search can subscribe the user to alerts. Do not save it unless the user explicitly asks; testing filters does not authorize a subscription.
- Do not invent precision: all percentages need a numerator, denominator and missing-data note.
- No paid enrichment, CRM writes, LinkedIn automation, campaign changes or outreach without a separate explicit request.
