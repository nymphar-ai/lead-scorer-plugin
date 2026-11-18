---
name: linkedin-post-sourcing
description: >-
  Turn a persona into a Lead Scorer LinkedIn engagement watch that finds the LinkedIn
  posts worth commenting: a LinkedIn boolean query written the way they actually post,
  creators they read, an optional prospect list, the commenting account, then a test
  search to tune it within the daily post budget. Use when the user wants a LinkedIn
  veille on a topic, to monitor what freelancers, coaches, consultancies or recruiters
  write on LinkedIn, or to improve a LinkedIn watch that brings irrelevant posts. For X
  use x-post-sourcing, for Reddit reddit-post-sourcing, for several networks at once
  engagement-watch-setup.
---

# LinkedIn post sourcing (persona → watch → tuned query)

You have the "lead-scorer" MCP server connected (Lead Scorer CRM, authenticated with Lead Scorer OAuth at the endpoint configured by the installed plugin). Use its tools for CRM reads and writes. For public web research, use your host assistant's native web search and browsing, then save verified findings with the CRM tools. Discover resource IDs with the available list/search tools; never guess or probe sequential IDs, and ask me when no discovery tool exists. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

> **Context first.** Call `get_my_memory` for my offer, my targets and my voice, and `list_engagement_watches` to reuse or improve an existing LinkedIn watch (`network: "linkedin"`) instead of duplicating it. If I want watches on several networks, follow `engagement-watch-setup` instead: it runs the interview once.

## Goal
One LinkedIn watch per persona that brings back, every morning, posts where my comment is welcome and useful: a person voicing the problem my offer solves, asking which tool to use, or discussing how they find clients.

## Steps
1. **Pin the persona.** In one or two sentences: who writes (role, situation), what they write when they have the problem, and the promise that answers it (for example freelancers between missions → "50 décideurs qui recrutent sur ton poste précis"). Ask me only what you cannot infer, one question at a time with your recommendation.
2. **Write the query the way they post, not the way I sell.** Collect 6 to 10 phrases the persona actually writes ("recherche mission", "intercontrat", "disponible pour une mission", "remplir mon agenda", "nouveaux mandats"). Use your native web search on public LinkedIn posts to check wording. Build one LinkedIn boolean query: quoted phrases, uppercase OR/AND, parentheses, for example `("recherche mission" OR intercontrat OR "disponible pour une mission") AND (freelance OR indépendant)`. Keep the (…) AND (…) shape. LinkedIn returns no post at all for a query with NOT, so Lead Scorer takes NOT terms out of the search and filters the keyword-search posts that mention them (`excluded_terms` on the watch); those posts still use read budget, and posts from followed creators or the prospect list are not filtered. Add `author_job_titles` only if the query alone is too broad.
3. **Add sources.**
   - **Creators:** propose up to 10 public LinkedIn creators the persona reads (found with web search, with the reason for each), as `/in/<handle>` profile URLs. A watch follows at most 30 (`creator_limit`), and each followed creator costs reads on every run.
   - **Prospect list (optional):** a lead list from `get_lead_lists` whose members' posts are followed (`lead_list_id`), when I want to comment my prospects' own posts.
4. **Show, then save.** Show me the persona, query, creators, prospect list, promise and offer link. After my approval, `upsert_engagement_watch` with the commenting account from `list_sender_accounts` (`sender_account_id`: my own LinkedIn account, which reads the posts; null uses the first connected one).
5. **Test once.** `search_linkedin_posts` on the new watch. Each post read uses my LinkedIn account's daily budget (100 posts a day per account, at most 30 per call), reported in `post_reads`: one search, not five. Read the posts it returns: count how many are truly from the persona and on topic. To add a post you or I found, use `add_linkedin_post` with its URL (it uses no budget).
6. **Tune.** Fewer than half on target: add an AND on the persona's role, remove a phrase that drags vendors or job offers in, or add NOT terms for the noise you saw (filtered after the search, not by LinkedIn); then update the watch. A test that reads 0 posts means the query matches nothing on LinkedIn: simplify it, it is not a filter problem. Do not re-run the search until tomorrow's runs unless I ask.
7. **Report.** The watch saved, the on-target rate of the test, the three best posts found, and the next step: the `linkedin-engagement-review` skill writes the comments.

## Hard rules
- Never create a second LinkedIn watch for the same persona: update the existing one.
- Never search more than twice in a row; stop when `post_reads.remaining` is low.
- A creator is someone the persona reads, not a competitor whose audience you want to poach.
