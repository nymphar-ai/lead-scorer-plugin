---
name: linkedin-post-sourcing
description: >-
  Turn a theme or a persona into a Lead Scorer engagement watch that finds the LinkedIn
  posts worth commenting: the persona, a LinkedIn boolean query written the way they
  actually post, creators they read, then a test search to tune it. Use when the user
  wants to find posts on a topic, set up a veille, monitor what freelancers, coaches,
  consultancies or recruiters write, or improve a watch that brings irrelevant posts.
---

# LinkedIn post sourcing (persona → watch → tuned query)

You have the "lead-scorer" MCP server connected (Lead Scorer CRM, authenticated with Lead Scorer OAuth at the endpoint configured by the installed plugin). Use its tools for CRM reads and writes. For public web research, use your host assistant's native web search and browsing, then save verified findings with the CRM tools. Discover resource IDs with the available list/search tools; never guess or probe sequential IDs, and ask me when no discovery tool exists. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

> **Context first.** Call `get_my_memory` for my offer, my targets and my voice, and `list_engagement_watches` to reuse or improve an existing watch instead of duplicating it.

## Goal
One watch per persona that brings back, every morning, posts where my comment is welcome and useful: a person voicing the problem my offer solves, asking which tool to use, or discussing how they find clients.

## Steps
1. **Pin the persona.** In one or two sentences: who writes (role, situation), what they write when they have the problem, and the promise that answers it (for example freelancers between missions → "50 décideurs qui recrutent sur ton poste précis"). Ask me only what you cannot infer.
2. **Write the query the way they post, not the way I sell.** Collect 6 to 10 phrases the persona actually writes ("recherche mission", "intercontrat", "disponible pour une mission", "remplir mon agenda", "nouveaux mandats"). Use your native web search on public LinkedIn posts to check wording. Build one LinkedIn boolean query: quoted phrases, uppercase OR/AND/NOT, parentheses, for example `("recherche mission" OR intercontrat OR "disponible pour une mission") AND (freelance OR indépendant) NOT recrute`. Add author titles only if the query alone is too broad.
3. **Add creators.** Propose up to 10 public LinkedIn creators the persona reads (found with web search, with the reason for each). Their new posts are read without using my LinkedIn account.
4. **Show, then save.** Show me the persona, query, creators, promise and offer link. After my approval, `upsert_engagement_watch` (pick the commenting account with `list_sender_accounts`, an optional prospect list with `get_lead_lists`).
5. **Test once.** `search_linkedin_posts` on the new watch (it spends part of today's 100 post reads: one search, not five). Read the posts it returns: count how many are truly from the persona and on topic.
6. **Tune.** Fewer than half on target: tighten with NOT terms, an AND on the persona's role, or remove a phrase that drags vendors in; then update the watch. Do not re-run the search until tomorrow's runs unless I ask: the budget is per account and per day.
7. **Report.** The watch saved, the on-target rate of the test, the three best posts found, and the next step: the engagement review (`list_pending_engagement_posts`) writes the comments.

## Hard rules
- Never create a second watch for the same persona: update the existing one.
- Never search more than twice in a row; stop when `post_reads.remaining` is low.
- A creator is someone the persona reads, not a competitor whose audience you want to poach.
