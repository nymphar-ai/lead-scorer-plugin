---
name: linkedin-engagement-review
description: >-
  Review the LinkedIn and X posts Lead Scorer collected for my engagement watches, skip
  the ones not worth a comment, and write three comment angles in my voice for the
  others, so I can pick one and post it from Content › Engagement (on X, from X's
  prefilled reply box). Use for the morning, noon or evening engagement routine, "fais
  ma revue de posts", commenting LinkedIn posts, replying to X posts or tweets, social
  selling, turning posts into conversations without sounding like a bot, or deciding
  which engagement authors and subreddits to follow.
---

# LinkedIn and X engagement review (three angles per post)

You have the "lead-scorer" MCP server connected (Lead Scorer CRM, authenticated with Lead Scorer OAuth at the endpoint configured by the installed plugin). Use its tools for CRM reads and writes. For public web research, use your host assistant's native web search and browsing, then save verified findings with the CRM tools. Discover resource IDs with the available list/search tools; never guess or probe sequential IDs, and ask me when no discovery tool exists. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

> **Context first.** Call `get_my_memory` and read its "Voix LinkedIn" section (how I write: tutoiement, length, words I use, words I never use). It is my voice on X too. If it is missing, build it once: read my own recent posts if I give you my profile URL (`fetch_profile_posts`), propose a short voice sheet, and save it with `update_my_memory` after I approve it.

## Goal
Each waiting post gets a verdict. The ones worth a comment get three ready-to-post comments, each a different angle, that start from the post and bring up my offer only when it genuinely helps. I decide and post in the app; you never publish, react or dismiss anything. You may suggest authors and subreddits for my watches to follow, but you follow one only after I say yes.

## Steps
1. **Load the queue.** `list_pending_engagement_posts` (repeat it while `remaining_to_review` > 0). Each post has a `network`: `linkedin` or `x`. The result returns, per watch, the persona, the promise and the offer link, my instructions, and a `feedback` block: my recent dismissals with their reason, the edits I made to your angles, my last comments, and `results` (which watches, post types, links and modes bring reactions, replies, conversations and sign-ups). Read `feedback` before the posts: my edits and dismissals override your instincts. LinkedIn posts follow `writing_rules`, X posts follow `writing_rules_x`.
2. **Judge each post.** Score three things from 0 to 100, then decide:
   - `author_fit`: is the author the persona, writing about themselves (not a vendor page, not someone selling the same thing as me)?
   - `topic_fit`: does the subject touch my territory (prospecting, finding clients, business development for freelancers, coaches, consultancies, recruiting firms)? Commenting off-topic shapes my LinkedIn interest graph badly: skip it even if the author fits.
   - `audience_fit`: will the right people read the comment? Use the reactions, comments, `velocity` and `mega_thread` signals: a thread over 150 comments buries a new one. On X, also read the views and the author's followers.
   Then classify `post_type`: `pain` (the persona voices a problem, e.g. "I can't find a mission"), `prospecting` (they share a method or a result), `tool_question` (they ask which tool or method to use), `audience` (a creator my persona reads), `prospect_post` (a prospect I follow). Skip with `verdict: "skip"` and a concrete `review_reason` when: drama, illness, mourning, layoffs announced with emotion, politics; a competitor; the author is already deep in a thread with me; nothing honest to add. Aim for 10 to 20 `ready` posts a day across watches; more is noise. An X post lives a few hours: review X posts first.
3. **For hard threads, read the comments.** When a top comment is a better place than the post itself (someone saying "same for me", a question nobody answered), call `get_engagement_post_comments` and make one angle a reply: set `reply_to_comment_id`, `reply_to_excerpt` and `reply_to_author`. On X it returns the post's replies. On LinkedIn it uses the daily post budget: only for posts you keep.
4. **Write three angles** per kept post, different in intent and length:
   - an experience angle ("I'm testing…", "what worked for me…") that may carry the offer link;
   - a pure value angle with no link (a method, a counterpoint, a figure);
   - a question or a reply that opens the conversation.
   On LinkedIn each one is 25 to 70 words. Each angle has exactly one concrete element (a lived example, a figure, a counterpoint). Write the offer link only as `{{lien}}`: Lead Scorer replaces it with my tracked link. At least one angle has no link. Follow the post's register (tu or vous), first person, no flattery opener, no hashtags, no em dash, at most one emoji, no closing question that only fishes for engagement. Mention the promise in plain words ("50 décideurs qui recrutent sur ton poste précis"), never a product pitch.
5. **On X, write shorter.** For a post whose `network` is `x`, follow `writing_rules_x`:
   - 8 to 45 words and at most 280 characters counted the way X counts them: a link counts 23, an emoji counts 2;
   - X shows replies with a link less, so prefer angles without `{{lien}}`, and keep at least one angle without it;
   - a shorter, more direct tone, still in the voice of "Voix LinkedIn": one idea, no preamble;
   - `like` is the only reaction (`suggested_reaction: "like"`), `suggest_capture` stays false (X replies give no usable leads), and there is no invitation.
   I always post the reply myself: the card opens X with your text prefilled, because X refuses replies sent by an application.
6. **Save in batches.** `submit_engagement_reviews` with up to 50 reviews per call: `verdict`, `review_reason` (one or two sentences I will read on the card), `post_type`, `priority`, the three scores, `suggested_reaction`, `suggest_capture` (LinkedIn only: true when the post's commenters are themselves the persona, e.g. other freelancers answering "same here"), and the `angles`. Read the returned `lint_warnings` and rewrite any angle that "sounds like AI" or runs too long before moving on. Each `ready` author also joins my CRM list for that network ("Engagement · LinkedIn", "Engagement · X" or "Engagement · Reddit"): `authors_listed` counts the new entries. You have nothing to add to a list yourself.
7. **Invitations (LinkedIn only).** `get_engagement_results` lists my comments; for each one whose `invite_status` is `suggested` (the author answered my comment), draft a connection note of at most 300 characters that refers to the exchange, and save it with `save_engagement_invite_note`. I send it myself. On X, an author's reply is only recorded.
8. **Suggest follows.** Never follow without my explicit yes: each followed account or subreddit costs reads on every run.
   - **Authors (LinkedIn and X).** Among the posts you kept, pick the authors who are clearly the persona and worth reading every day (strong `author_fit` and `topic_fit`, or a second good post from them). Propose at most three, and only those whose `crm.author_follow` is `available`. After I agree, call `follow_engagement_author` with the `post_id`. When it is `full`, the watch already follows its maximum (30 accounts on LinkedIn, 60 on X): ask me which creator to drop, update the watch with `upsert_engagement_watch`, then follow.
   - **Subreddits (Reddit watches).** A Reddit card has no author to follow (`author_follow` is null), because Reddit cannot read a user's posts. Instead, `list_engagement_watches` gives each Reddit watch `subreddit_suggestions`: subreddits that gave it at least two retained posts and that it does not follow yet. Propose them. After I agree, call `follow_engagement_subreddit` with the `watch_id` and the subreddit. A watch follows at most 10 subreddits: when it is full, ask me which one to drop first.
9. **Report.** How many posts reviewed, kept and skipped per network (with the top skip reasons), the three best cards to open first, what `results` suggests changing (a watch that never converts, links that hurt replies, a network that brings nothing), how many authors entered my Engagement lists, and the follows you suggest, each with a one-line reason.

## Hard rules
- Never publish, like, dismiss or send anything: the user decides in Content › Engagement, and on X posts the reply from X.
- Never follow an author or a subreddit without the user's explicit yes for that author or subreddit.
- Never pretend to be a customer, invent a result, or claim we already spoke.
- No comment that would read the same under another post: if it fits anywhere, rewrite it.
- If my voice sheet and my recent edits disagree, follow the edits.
