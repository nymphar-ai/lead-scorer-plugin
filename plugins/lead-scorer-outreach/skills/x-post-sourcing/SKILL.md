---
name: x-post-sourcing
description: >-
  Turn a persona into a Lead Scorer X (Twitter) engagement watch that finds the X posts
  worth replying to: an X search query written the way they actually tweet, the X
  accounts and lists they read, the user's own X handle, then a test search to tune it
  within the daily X read allowance. Use when the user wants an X or Twitter veille,
  to monitor what founders, freelancers or tech people tweet, or to improve an X watch
  that brings irrelevant posts. For several networks at once use engagement-watch-setup.
---

# X post sourcing (persona → watch → tuned query)

You have the "lead-scorer" MCP server connected (Lead Scorer CRM, authenticated with Lead Scorer OAuth at the endpoint configured by the installed plugin). Use its tools for CRM reads and writes. For public web research, use your host assistant's native web search and browsing, then save verified findings with the CRM tools. Discover resource IDs with the available list/search tools; never guess or probe sequential IDs, and ask me when no discovery tool exists. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

> **Context first.** Call `get_my_memory` for my offer, my targets and my voice, and `list_engagement_watches` to reuse or improve an existing X watch (`network: "x"`) instead of duplicating it. If I want watches on several networks, follow `engagement-watch-setup` instead: it runs the interview once.

## How X differs
- X posts are public and read without any account of mine, within a daily allowance of X post reads (at most 40 posts per call), reported in `post_reads`.
- I always post my reply myself: the card opens X with the reply prefilled, because X refuses replies sent by an application. A reply is short: at most 280 characters counted the X way (a link counts 23, an emoji 2), and a link makes it less visible.
- A post ages fast: the review window is 24 hours (48 hours for a post added by hand). The review should follow each collection the same day.

## Goal
One X watch per persona that brings back, at each collection, fresh posts where a short reply from me is welcome and useful.

## Steps
1. **Pin the persona.** In one or two sentences: who tweets (role, situation), what they write when they have the problem, and the promise that answers it. Check they really post on X; if they mostly post on LinkedIn, say so. Ask me only what you cannot infer, one question at a time with your recommendation.
2. **Write the query the way they tweet.** Collect 6 to 10 short phrases the persona actually types (X is shorter and more casual than LinkedIn: "dispo pour une mission", "je cherche des clients", "intercontrat"). Check wording with your native web search. Build one X search query, at most 420 characters: quoted phrases, OR, parentheses, a space for AND, `-mot` to exclude and `lang:fr`, for example `("cherche une mission" OR intercontrat OR "dispo pour une mission") (freelance OR indépendant) -recrute lang:fr`. NOT is useless on X: write `-mot`. Lead Scorer leaves replies and reposts out itself.
3. **Add sources.**
   - **X accounts:** propose the accounts the persona reads, as `@nom` in `creators`, with the reason for each. A watch follows at most 60; Lead Scorer reads them with one `from:` search per 20 accounts, so each one costs reads on every run.
   - **X lists (optional):** up to 5 public lists (`x.com/i/lists/<id>`) in `x_lists` that already gather the right accounts.
4. **Ask for my handle.** My own `x_handle` (`@nom`) keeps my own posts out and lets Lead Scorer find the replies I posted, which feeds the results. Without it, a reply can only be confirmed by hand.
5. **Show, then save.** Show me the persona, query, accounts, lists, handle, promise and offer link. After my approval, `upsert_engagement_watch` with `network: "x"` at creation (a watch keeps its network). An X watch has no sender account and no prospect list.
6. **Test once.** `search_linkedin_posts` on the new watch: the tool keeps its name and runs the X search, then the followed accounts and lists. One search, not five. Count how many posts are truly from the persona and on topic. To add a post you or I found, use `add_linkedin_post` with its `x.com/…/status/…` URL (it counts in the daily X allowance).
7. **Tune.** Fewer than half on target: narrow on the persona's words, remove a phrase that drags in job offers, ads or bots, add `-mot` for the noise you saw, or drop an account that posts off-topic; then update the watch. A test that reads 0 posts means the query matches nothing: simplify it. Do not re-run the search until the next collection unless I ask.
8. **Report.** The watch saved, the on-target rate of the test, the three best posts found, and the next step: the `linkedin-engagement-review` skill writes the replies, and the sooner the better on X.

## Hard rules
- Never create a second X watch for the same persona: update the existing one.
- Never search more than twice in a row; stop when `post_reads.remaining` is low.
- An account is someone the persona reads, not a competitor whose audience you want to poach.
- Lead Scorer never posts on X: I always reply myself.
