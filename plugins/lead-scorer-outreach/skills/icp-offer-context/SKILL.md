---
name: icp-offer-context
description: >-
  Define who you sell to, what disqualifies a lead, and which proof points you may claim,
  then store it in Lead Scorer as reusable context. Use when the user is setting up
  outreach, or mentions their ICP, ideal customer profile, positioning, value proposition,
  buyer persona, disqualifiers, or says the agents keep guessing who they target.
---

# ICP & offer context pack

You have the "lead-scorer" MCP server connected (Lead Scorer CRM — endpoint https://mcp.lead-scorer.com/mcp, authenticated with Lead Scorer OAuth). Use its tools for every read and write. Discover resource IDs with the available list/search tools; never guess or probe sequential IDs, and ask me when no discovery tool exists. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

## Goal
Produce ONE context block that every other skill reads before it sources, scores or writes anything. Without it, each agent re-invents my positioning slightly differently and the outreach drifts.

## Steps
1. **Look at reality before asking me.** `list_products` (what I already sell, as the CRM knows it), `get_lead_lists` and `list_tags` (who I have actually been targeting). Show me the gap between what I say I sell and who is in the CRM.
2. **Interview me.** Ask these, one at a time, and push back on vague answers:
   - What do I sell, in one sentence a customer would recognize?
   - Which problem does the buyer already know they have? (If they do not know it, outreach is education, and that is a different motion.)
   - Who signs, who blocks, who uses?
   - What makes a company an obvious fit — size, stack, motion, geography, moment?
   - **What disqualifies one?** Push until I give at least three real disqualifiers.
   - Which buying triggers mean "now" rather than "someday"?
   - What proof can I show — named customer, measured result, public case? What can I NOT claim publicly?
   - How do I talk: tu/vous, formal, first-person, jargon tolerated or not?
3. **Write the pack** with exactly these sections: Offer · ICP · Buying triggers · Disqualifiers · Proof points (each with source) · Forbidden claims · Voice rules.
4. **Store it in the right layers.** Read `get_my_memory`, merge the full pack into my canonical personal Markdown with `update_my_memory`, preserving useful existing sections and the returned revision. Use `create_product` for the product-specific offer and value proposition. Personal identity, voice, relationships and durable preferences belong in memory; product facts belong on the product.
5. **Verify reuse.** Call `compile_context_pack` for a representative operation. Check that the personal memory and product overlay remain distinguishable and that no private relationship claim was inferred from public profile data.
6. **Report.** The pack, the stored memory revision, plus the three answers you found weakest — those are what will break the outreach later.

## Hard rules
- Disqualifiers are mandatory output. A skill without them fabricates fit.
- A proof point I cannot name publicly is not a proof point. Move it to Forbidden claims.
- Never overwrite the whole personal memory from stale context: read the latest revision immediately before updating it.
- Do not soften my words into marketing copy. This pack is internal, and specificity is the whole value.
