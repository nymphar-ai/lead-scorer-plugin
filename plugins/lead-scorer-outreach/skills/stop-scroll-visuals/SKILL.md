---
name: stop-scroll-visuals
description: >-
  Design and attach one branded typographic poster per approved content post, rotating
  visual archetypes so the feed stays varied. Use when the user mentions post visuals,
  images for LinkedIn, posters or graphics, branded visuals, or wants their feed to look
  consistent.
---

# Stop-scroll visuals for approved posts

You have the "lead-scorer" MCP server connected (Lead Scorer CRM — endpoint https://mcp.lead-scorer.com/mcp, authenticated with Lead Scorer OAuth). Use its tools for every read and write. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

## Goal
Give every approved post ONE typographic poster (1080×1350) that makes the feed recognizable and stops the scroll — never decorative stock imagery.

## Brand kit (edit once, then never per-run)
- Canvas <bg color>, accent <accent color>, ink <text color>; serif display + sans body (loaded via Google Fonts); a thin double frame; brand wordmark top-left; site URL bottom-left.
- Red-ish tone reserved for NEGATIVE numbers only.

## Steps
1. **Queue.** `list_content_posts` status "approved" — keep those without image_url.
2. **Pick the pivot** in each post: the one number, comparison, or sentence the whole post hangs on.
3. **Choose an archetype — VARIETY IS A RULE.** Rotate: hero number · two-bar comparison (claimed vs real) · before/after · two columns · 3-step framework · big quote · proportion dots. Never two consecutive posts with the same archetype.
4. **Compose as SVG/HTML**, render to PNG at exactly 1080×1350 (headless Chrome: --headless=new --window-size=1080,1350 --screenshot). QA the PNG yourself: readable as a thumbnail? one idea? nothing overlapping?
5. **Attach.** `upload_content_media` with the PNG base64, post_id, attach:true — it sets the post's image_url.
6. **Report.** Post → archetype chosen, so the next run can keep rotating.

## Hard rules
- One idea per poster. If it needs explaining, it failed.
- Real numbers from the post only. No emoji. Typography, not photography.
