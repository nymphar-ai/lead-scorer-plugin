---
name: linkedin-engagement-review
description: >-
  Review the LinkedIn posts Lead Scorer collected for my engagement watches, skip the
  ones not worth a comment, and write three comment angles in my voice for the others,
  so I can pick one and post it from Content › Engagement. Use for the morning, noon or
  evening engagement routine, "fais ma revue de posts", commenting LinkedIn posts,
  social selling, or turning posts into conversations without sounding like a bot.
---

# LinkedIn engagement review (three angles per post)

You have the "lead-scorer" MCP server connected (Lead Scorer CRM, authenticated with Lead Scorer OAuth at the endpoint configured by the installed plugin). Use its tools for CRM reads and writes. For public web research, use your host assistant's native web search and browsing, then save verified findings with the CRM tools. Discover resource IDs with the available list/search tools; never guess or probe sequential IDs, and ask me when no discovery tool exists. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

> **Context first.** Call `get_my_memory` and read its "Voix LinkedIn" section (how I write: tutoiement, length, words I use, words I never use). If it is missing, build it once: read my own recent posts if I give you my profile URL (`fetch_profile_posts`), propose a short voice sheet, and save it with `update_my_memory` after I approve it.

## Goal
Each waiting post gets a verdict. The ones worth a comment get three ready-to-post comments, each a different angle, that start from the post and bring up my offer only when it genuinely helps. I decide and post in the app; you never publish, react or dismiss anything.

## Steps
1. **Load the queue.** `list_pending_engagement_posts` (repeat it while `remaining_to_review` > 0). It returns, per watch, the persona, the promise and the offer link, my instructions, and a `feedback` block: my recent dismissals with their reason, the edits I made to your angles, my last comments, and `results` (which watches, post types, links and modes bring reactions, replies, conversations and sign-ups). Read `feedback` before the posts: my edits and dismissals override your instincts.
2. **Judge each post.** Score three things from 0 to 100, then decide:
   - `author_fit`: is the author the persona, writing about themselves (not a vendor page, not someone selling the same thing as me)?
   - `topic_fit`: does the subject touch my territory (prospecting, finding clients, business development for freelancers, coaches, consultancies, recruiting firms)? Commenting off-topic shapes my LinkedIn interest graph badly: skip it even if the author fits.
   - `audience_fit`: will the right people read the comment? Use the reactions, comments, `velocity` and `mega_thread` signals: a thread over 150 comments buries a new one.
   Then classify `post_type`: `pain` (the persona voices a problem, e.g. "I can't find a mission"), `prospecting` (they share a method or a result), `tool_question` (they ask which tool or method to use), `audience` (a creator my persona reads), `prospect_post` (a prospect I follow). Skip with `verdict: "skip"` and a concrete `review_reason` when: drama, illness, mourning, layoffs announced with emotion, politics; a competitor; the author is already deep in a thread with me; nothing honest to add. Aim for 10 to 20 `ready` posts a day across watches; more is noise.
3. **For hard threads, read the comments.** When a top comment is a better place than the post itself (someone saying "same for me", a question nobody answered), call `get_engagement_post_comments` and make one angle a reply: set `reply_to_comment_id`, `reply_to_excerpt` and `reply_to_author`. This uses the daily post budget: only for posts you keep.
4. **Write three angles** per kept post, different in intent and length:
   - an experience angle ("I'm testing…", "what worked for me…") that may carry the offer link;
   - a pure value angle with no link (a method, a counterpoint, a figure);
   - a question or a reply that opens the conversation.
   Each one 25 to 70 words, with exactly one concrete element (a lived example, a figure, a counterpoint). Write the offer link only as `{{lien}}`: Lead Scorer replaces it with my tracked link. At least one angle has no link. Follow the post's register (tu or vous), first person, no flattery opener, no hashtags, no em dash, at most one emoji, no closing question that only fishes for engagement. Mention the promise in plain words ("50 décideurs qui recrutent sur ton poste précis"), never a product pitch.
5. **Save in batches.** `submit_engagement_reviews` with up to 50 reviews per call: `verdict`, `review_reason` (one or two sentences I will read on the card), `post_type`, `priority`, the three scores, `suggested_reaction`, `suggest_capture` (true when the post's commenters are themselves the persona, e.g. other freelancers answering "same here"), and the `angles`. Read the returned `lint_warnings` and rewrite any angle that "sounds like AI" before moving on.
6. **Invitations.** `get_engagement_results` lists my comments; for each one whose `invite_status` is `suggested` (the author answered my comment), draft a connection note of at most 300 characters that refers to the exchange, and save it with `save_engagement_invite_note`. I send it myself.
7. **Report.** How many posts reviewed, kept and skipped (with the top skip reasons), the three best cards to open first, and what `results` suggests changing (a watch that never converts, links that hurt replies).

## Hard rules
- Never publish, like, dismiss or send anything: the user decides in Content › Engagement.
- Never pretend to be a customer, invent a result, or claim we already spoke.
- No comment that would read the same under another post: if it fits anywhere, rewrite it.
- If my voice sheet and my recent edits disagree, follow the edits.
