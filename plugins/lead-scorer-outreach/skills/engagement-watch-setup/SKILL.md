---
name: engagement-watch-setup
description: >-
  Set up Lead Scorer engagement watches on LinkedIn, X and/or Reddit through a short
  interview in the chat: who to reach, what they post when they have the problem, the
  offer and its promise, the link and the tone, then one watch per network, shown before
  saving, tested once and tuned, with an optional daily review routine. Use when the user
  wants to start commenting their prospects' posts, "mettre en place ma veille
  d'engagement", set up a veille on one or several networks, or when Lead Scorer's
  "Avec votre IA" screen sends them here.
---

# Engagement watch setup (interview → one watch per network)

You have the "lead-scorer" MCP server connected (Lead Scorer CRM, authenticated with Lead Scorer OAuth at the endpoint configured by the installed plugin). Use its tools for CRM reads and writes. For public web research, use your host assistant's native web search and browsing, then save verified findings with the CRM tools. Discover resource IDs with the available list/search tools; never guess or probe sequential IDs, and ask me when no discovery tool exists. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

> **Context first.** Call `get_my_memory` (my offer, my targets, the "Voix LinkedIn" section) and `list_engagement_watches`. A watch is one persona on one network: if one already exists for this persona and network, improve it instead of creating a duplicate.

## Goal
At the end, each network I chose has one watch that brings back, three times a day, posts where my comment is welcome and useful, and I know how the daily review works.

## Steps
1. **Interview me, one question at a time.** Each question comes with your recommendation, drawn from my memory and my existing watches, so I can answer "yes" or correct it. Do not propose a watch before you understand:
   - **the persona**: who writes (role, situation, size of business);
   - **what they post when they have the problem**: the words they actually use, not the way I sell ("je cherche une mission", "intercontrat", "comment trouvez-vous vos clients ?");
   - **the offer and its promise**: what my offer brings them, in one plain sentence ("50 décideurs qui recrutent sur ton poste précis");
   - **the link**: the https page a comment may point to (`cta_url`), or none;
   - **the tone**: tu or vous, what I never say, anything the "Voix LinkedIn" section does not cover.
   Stop asking as soon as you can write the watch: five or six questions are usually enough. Save durable answers (offer, voice) with `update_my_memory` only after I approve the wording.
2. **Pick the networks.** Use the ones I named. Otherwise recommend where this persona really posts: LinkedIn for professionals posting under their name, X for founders and tech people who post short and often, Reddit for people asking peers for advice under a pseudonym. One watch per network.
3. **Build each watch with its network skill.** Each network has its own rules for the query, the sources and the budget. Follow, for each chosen network:
   - LinkedIn: the `linkedin-post-sourcing` skill;
   - X: the `x-post-sourcing` skill;
   - Reddit: the `reddit-post-sourcing` skill.
   If a network skill is not installed, follow the descriptions of `upsert_engagement_watch` and `search_linkedin_posts`, which state each network's rules. Reuse the interview answers: do not ask me the same thing twice.
4. **Show, then save.** For each watch, show me the network, persona, query, sources (creators, X accounts, subreddits), promise, offer link and comment instructions. Save with `upsert_engagement_watch` only after my approval, one watch at a time.
5. **Test once, then tune.** Run one `search_linkedin_posts` per new watch (the tool serves all three networks). Count how many posts are truly from the persona and on topic. Fewer than half: adjust as the network skill says, update the watch, and do not search again today unless I ask: every network has a daily read budget.
6. **Review what the test found.** Hand over to the `linkedin-engagement-review` skill (or `list_pending_engagement_posts`, then `submit_engagement_reviews`) so the first cards are ready in Content › Engagement.
7. **Offer the routine.** Watches collect posts at 7:45, 11:45 and 16:45 (Paris time). If you can schedule a recurring task, offer me a daily review a few minutes after one or several of those collections, running the `linkedin-engagement-review` skill. Create it only after I say yes, and tell me how to stop it.
8. **Report.** The watches saved (network, persona, sources), the on-target rate of each test, the first cards to open, and the routine if I accepted it.

## Hard rules
- One question at a time, always with a recommendation; never a questionnaire.
- Never create a second watch for the same persona on the same network: update the existing one.
- Never save a watch I have not seen, and never follow an account or a subreddit I have not approved.
- Lead Scorer never publishes: I always post my comments myself.
