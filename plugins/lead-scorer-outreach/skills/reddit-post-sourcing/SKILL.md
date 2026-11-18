---
name: reddit-post-sourcing
description: >-
  Turn a persona into a Lead Scorer Reddit engagement watch that finds the Reddit threads
  worth answering: the subreddits where the persona asks for advice first (found by web
  search, judged on activity and rules), then a strict query, the user's Reddit
  username, and a test search within the daily Reddit read allowance. Use when the user
  wants a Reddit veille, to find the subreddits where their prospects ask questions, or
  to improve a Reddit watch that brings irrelevant threads. For several networks at once
  use engagement-watch-setup.
---

# Reddit post sourcing (persona → subreddits → watch)

You have the "lead-scorer" MCP server connected (Lead Scorer CRM, authenticated with Lead Scorer OAuth at the endpoint configured by the installed plugin). Use its tools for CRM reads and writes. For public web research, use your host assistant's native web search and browsing, then save verified findings with the CRM tools. Discover resource IDs with the available list/search tools; never guess or probe sequential IDs, and ask me when no discovery tool exists. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

> **Context first.** Call `get_my_memory` for my offer, my targets and my voice, and `list_engagement_watches` to reuse or improve an existing Reddit watch (`network: "reddit"`) instead of duplicating it. If I want watches on several networks, follow `engagement-watch-setup` instead: it runs the interview once.

## How Reddit differs
- **Subreddits first, query second.** Reddit search is loose: it returns posts unrelated to the query and finds almost nothing in French. Lead Scorer keeps only the searched posts whose title or text satisfy the whole query, so a query alone often brings back little. A well-chosen subreddit gives the best posts.
- **No people to follow.** A Reddit account says nothing about the person and Lead Scorer cannot read a user's posts: a Reddit watch follows subreddits, not creators.
- **Communities punish marketing.** Subreddits remove self-promotion and ban accounts that do it. A comment is an expert's answer to the question asked: no link, no pitch, no "DM me". The age and karma of my account matter: a new account with little karma gets filtered or removed in many subreddits.
- **I always comment myself.** The card copies the comment and opens the thread; Lead Scorer never posts or votes on Reddit.
- Posts are public and read without any account of mine, within a daily allowance of Reddit post reads (at most 40 posts per call), reported in `post_reads`. A thread stays open about two days: the review window is 48 hours.

## Goal
One Reddit watch per persona, following the few subreddits where that persona asks peers for advice, so that each collection brings threads where an honest, expert answer from me helps.

## Steps
1. **Pin the persona.** In one or two sentences: who asks (role, situation), what they ask when they have the problem, and what my expertise can answer. Reddit is mostly English-speaking: ask me whether English threads are fine. Ask me only what you cannot infer, one question at a time with your recommendation.
2. **Find the subreddits.** Use your native web search (for example `site:reddit.com/r "<a question the persona asks>"`) to find where the persona really asks. For each candidate, judge:
   - **activity**: subscribers, and above all recent posts and comments (several new threads a week on my topic);
   - **fit**: threads asked by the persona, not by vendors or students;
   - **rules**: read the subreddit's rules and sidebar: self-promotion, links, minimum account age or karma, mandatory flairs, days reserved for promotion. Drop a subreddit whose rules forbid what I would do.
   Propose at most 10 subreddits (`r/nom`), each with its activity, why it fits and the rule that matters most. A watch follows at most 10.
3. **Write a strict query (optional).** At most 300 characters, in the language of the threads: every term, OR, NOT or `-mot`, quoted phrases, for example `("first client" OR "find clients") freelance -hiring`. Remember that the whole query must match the title or text of a post, or Lead Scorer drops it: keep it short. The subreddits do most of the work.
4. **Ask for my username and check my account.** My own `reddit_username` (`u/nom`) keeps my own posts out and lets Lead Scorer find the comments I posted, which feeds the results; without it, a comment can only be confirmed by hand. Ask whether my account is old enough and has enough karma for the subreddits chosen; if not, recommend commenting without any mention of my offer for a few weeks first.
5. **Show, then save.** Show me the persona, subreddits (with their rules), query, username and comment instructions (expert advice, no link, no pitch). After my approval, `upsert_engagement_watch` with `network: "reddit"` at creation (a watch keeps its network), `subreddits` and `reddit_username`. A Reddit watch has no creators, no sender account and no prospect list, and `cta_url` is never written in a Reddit comment.
6. **Test once.** `search_linkedin_posts` on the new watch: the tool keeps its name, reads the subreddits and runs the search at once (it can take about 40 seconds). One search, not five. Count how many threads are truly from the persona and on topic. To add a thread you or I found, use `add_linkedin_post` with its `reddit.com/r/…/comments/…` URL (it counts in the daily Reddit allowance).
7. **Tune.** Fewer than half on target: replace the subreddit that brings noise, simplify a query that keeps nothing, or exclude the noise with `-mot`; then update the watch. Later, `list_engagement_watches` shows `subreddit_suggestions` (subreddits that gave the watch at least two retained posts): propose them, and after my yes call `follow_engagement_subreddit`. When the watch already follows 10, ask me which one to drop with `upsert_engagement_watch` first.
8. **Report.** The watch saved, the subreddits with their key rule, the on-target rate of the test, the three best threads found, and the next step: the `linkedin-engagement-review` skill writes the comments.

## Hard rules
- Never create a second Reddit watch for the same persona: update the existing one.
- Never follow a subreddit without my explicit yes, and never one whose rules forbid what I would post.
- Never put a link, the offer or a call to action in a Reddit comment, even if the watch's instructions mention the offer.
- Never search more than twice in a row; stop when `post_reads.remaining` is low.
- Lead Scorer never posts or votes on Reddit: I always comment myself.
