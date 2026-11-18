---
name: linkedin-post-sourcing
description: >-
  Turn a theme or a persona into a Lead Scorer engagement watch that finds the LinkedIn
  or X posts worth commenting: the persona, a search query written the way they
  actually post, creators or X accounts they read, then a test search to tune it. Use
  when the user wants to find posts on a topic, set up a veille on LinkedIn or X
  (Twitter), monitor what freelancers, coaches, consultancies or recruiters write, or
  improve a watch that brings irrelevant posts.
---

# LinkedIn and X post sourcing (persona → watch → tuned query)

You have the "lead-scorer" MCP server connected (Lead Scorer CRM, authenticated with Lead Scorer OAuth at the endpoint configured by the installed plugin). Use its tools for CRM reads and writes. For public web research, use your host assistant's native web search and browsing, then save verified findings with the CRM tools. Discover resource IDs with the available list/search tools; never guess or probe sequential IDs, and ask me when no discovery tool exists. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

> **Context first.** Call `get_my_memory` for my offer, my targets and my voice, and `list_engagement_watches` to reuse or improve an existing watch instead of duplicating it. Each watch has a `network`, `linkedin` or `x`, set once at creation.

## Goal
One watch per persona and per network that brings back, every morning, posts where my comment is welcome and useful: a person voicing the problem my offer solves, asking which tool to use, or discussing how they find clients.

## Steps
1. **Pin the persona and the network.** In one or two sentences: who writes (role, situation), what they write when they have the problem, and the promise that answers it (for example freelancers between missions → "50 décideurs qui recrutent sur ton poste précis"). Then where they write: LinkedIn by default, X when the persona really posts there. Ask me only what you cannot infer.
2. **Write the query the way they post, not the way I sell.** Collect 6 to 10 phrases the persona actually writes ("recherche mission", "intercontrat", "disponible pour une mission", "remplir mon agenda", "nouveaux mandats"). Use your native web search on public posts to check wording.
   - **LinkedIn:** one boolean query with quoted phrases, uppercase OR/AND, parentheses, for example `("recherche mission" OR intercontrat OR "disponible pour une mission") AND (freelance OR indépendant)`. Keep the (…) AND (…) shape. LinkedIn returns no post at all for a query with NOT, so Lead Scorer takes NOT terms out of the search and filters the posts read that mention them (`excluded_terms` on the watch); they still use read budget. Add author titles only if the query alone is too broad.
   - **X:** X search syntax, at most 420 characters: quoted phrases, OR, parentheses, a space for AND, `-mot` to exclude and `lang:fr`, for example `("cherche une mission" OR intercontrat OR "dispo pour une mission") (freelance OR indépendant) -recrute lang:fr`. NOT is useless on X: write `-mot`. Lead Scorer leaves replies and reposts out itself. X posts are shorter and more casual than on LinkedIn: favour the short phrases people actually type.
3. **Add creators.**
   - **LinkedIn:** propose up to 10 public LinkedIn creators the persona reads (found with web search, with the reason for each). Their new posts are read without using my LinkedIn account.
   - **X:** propose the X accounts the persona reads, as `@nom` in `creators` (60 at most), with the reason for each, and optionally up to 5 public X lists in `x_lists` (`x.com/i/lists/<id>`) that already gather them.
4. **Show, then save.** Show me the network, persona, query, creators, promise and offer link. After my approval, `upsert_engagement_watch`:
   - **LinkedIn:** pick the commenting account with `list_sender_accounts`, and optionally a prospect list with `get_lead_lists`.
   - **X:** pass `network: "x"` at creation (a watch keeps its network) and my own `x_handle` (`@nom`): it keeps my own posts out and lets Lead Scorer find the replies I posted. Ask me for it if you do not know it. X posts are public and read without any account of mine; there is no sender account and no prospect list on an X watch.
5. **Test once.** `search_linkedin_posts` on the new watch: the tool keeps its name and runs the X search on an X watch. On LinkedIn it spends part of today's 100 post reads; on X it reads up to 40 posts per call within a daily allowance of X post reads, reported in `post_reads`. One search, not five. Read the posts it returns: count how many are truly from the persona and on topic. To add a post you found yourself, use `add_linkedin_post` with its URL (an `x.com/…/status/…` URL on an X watch).
6. **Tune.** Fewer than half on target: narrow on the persona's role, remove a phrase that drags vendors or job offers in, or exclude the noise you saw (NOT terms on LinkedIn, filtered after the search; `-mot` on X, sent to X); then update the watch. A test that reads 0 posts means the query matches nothing: simplify it, it is not a filter problem. Do not re-run the search until tomorrow's runs unless I ask: the budget is per day.
7. **Report.** The watch saved, the on-target rate of the test, the three best posts found, and the next step: the engagement review (`list_pending_engagement_posts`) writes the comments. On X the posts expire after 24 hours, so the review should follow the same day.

## Hard rules
- Never create a second watch for the same persona on the same network: update the existing one.
- Never search more than twice in a row; stop when `post_reads.remaining` is low.
- A creator is someone the persona reads, not a competitor whose audience you want to poach.
