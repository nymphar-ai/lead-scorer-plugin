# Lead Scorer Outreach plugin

The official public plugin for connecting Codex, ChatGPT and Claude Code to
[Lead Scorer](https://lead-scorer.com).

One installation provides:

- the hosted OAuth MCP at `https://mcp.lead-scorer.com/mcp`;
- 24 reviewed Skills for sourcing, scoring, enrichment, outreach and content;
- agent-native account onboarding, Pro subscription and credit top-ups;
- secure hosted email and LinkedIn connection flows;
- account-level sender signatures inherited by campaigns, with preflight protection;
- human approval boundaries before payment, connection, credit use or sending.

The repository contains no API key, OAuth token, Stripe Price ID, card data or
third-party channel credential.

## Install in Claude Code

```bash
claude plugin marketplace add nymphar-ai/lead-scorer-plugin
claude plugin install lead-scorer-outreach@lead-scorer
```

Run `/reload-plugins` or start a new Claude Code session, then ask:

> Check my Lead Scorer onboarding status and help me set up reviewed outreach.

Claude opens the Lead Scorer OAuth flow in the browser. A new user can create
an account there before granting MCP access.

## Install in Codex

```bash
git clone https://github.com/nymphar-ai/lead-scorer-plugin.git
codex plugin marketplace add ./lead-scorer-plugin
codex plugin add lead-scorer-outreach@lead-scorer
```

Approve the plugin and browser authentication, then start a new Codex task and
ask:

> Check my Lead Scorer onboarding status and help me set up reviewed outreach.

## Fallback: connect only the MCP

Claude Code:

```bash
claude mcp add --transport http --scope user lead-scorer https://mcp.lead-scorer.com/mcp
```

Codex can add the same Streamable HTTP URL as `lead_scorer`, then run:

```bash
codex mcp login lead_scorer
```

The fallback connects the tools but does not install the reviewed Skills.

## Safety model

- Login, signup and OAuth consent happen on Lead Scorer's hosted pages.
- Card data is entered only in Stripe Checkout.
- Email and LinkedIn credentials are entered only in the hosted connection flow.
- A separate explicit approval is required before each checkout or channel connection.
- Campaigns remain drafts until a human reviews and activates them.

## Repository layout

```text
.agents/plugins/marketplace.json          Codex marketplace
.claude-plugin/marketplace.json           Claude Code marketplace
plugins/lead-scorer-outreach/
  .codex-plugin/plugin.json               Codex manifest
  .claude-plugin/plugin.json              Claude manifest
  .mcp.json                               Hosted MCP configuration
  assets/                                 Marketplace branding
  SUBMISSION.md                           Anthropic submission dossier
  skills/                                 24 reviewed Lead Scorer Skills
```

## Updating

Plugin releases use semantic versions in both manifests and in the Claude
marketplace entry. The MCP remains hosted by Lead Scorer, so server-side tool
fixes do not require republishing credentials or changing user configuration.

Before opening a pull request, run:

```bash
python scripts/validate_repository.py
claude plugin validate plugins/lead-scorer-outreach --strict
claude plugin validate .claude-plugin/marketplace.json --strict
```

## Links

- [MCP documentation](https://lead-scorer.com/mcp-server)
- [Skills library](https://lead-scorer.com/skills)
- [Privacy policy](https://lead-scorer.com/privacy)
- [Terms of service](https://lead-scorer.com/terms)
