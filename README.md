# Lead Scorer Outreach plugin

The official public plugin for connecting Codex, ChatGPT and Claude Code to
[Lead Scorer](https://lead-scorer.com).

One installation provides:

- the hosted OAuth MCP at `https://mcp.lead-scorer.com/mcp`;
- 25 reviewed Skills for sourcing, scoring, enrichment, outreach and content;
- source-backed company website summaries and product/ICP-specific AI analysis;
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
codex plugin marketplace add nymphar-ai/lead-scorer-plugin --ref main
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
  skills/                                 25 reviewed Lead Scorer Skills
```

## Updating

Plugin releases use semantic versions in both manifests and in the Claude
marketplace entry. The MCP remains hosted by Lead Scorer, so server-side tool
fixes do not require republishing credentials or changing user configuration.

Every change under `plugins/lead-scorer-outreach/skills/` requires a version
increase in all three version fields, including changes to supporting files.
CI compares pull requests with their base commit and main pushes with their
previous commit. It rejects skill changes without a strictly newer version.
Publishing a Git tag alone does not update clients following `main`; merge the
skills and version bump into `main` together.

### Codex clients

Register the GitHub marketplace using the installation command above so Codex
can fetch new releases. The `source: local` entry inside our marketplace remains
correct: it points to the plugin within the fetched repository.

Existing users who registered a local clone should migrate once:

```bash
codex plugin marketplace remove lead-scorer
codex plugin marketplace add nymphar-ai/lead-scorer-plugin --ref main
codex plugin add lead-scorer-outreach@lead-scorer
```

Refresh the Git marketplace explicitly when needed:

```bash
codex plugin marketplace upgrade lead-scorer
```

Start a new task after updating; restart the desktop app if it still shows the
old skills. A remote registration makes releases fetchable, but does not promise
an automatic refresh schedule across all Codex clients.

For managed ChatGPT/Codex workspaces, administrators can import the GitHub
marketplace through workspace settings. OpenAI documents daily synchronization
and a **Sync now** control. See [OpenAI marketplace synchronization](https://help.openai.com/en/articles/20001256/).

### Claude Code clients

Third-party marketplaces default to auto-update disabled. Each user should open
`/plugin`, select **Marketplaces**, select **lead-scorer**, and choose
**Enable auto-update**. Organization administrators can instead set
`autoUpdate: true` on the marketplace's `extraKnownMarketplaces` entry in managed
settings. This is a client setting, not a field in our plugin manifest.

Claude updates the installed plugin in the background after startup. Run
`/reload-plugins` when prompted, or start a new session to load the updated skills.
For a manual update:

```bash
claude plugin marketplace update lead-scorer
claude plugin update lead-scorer-outreach@lead-scorer
```

See [Claude Code auto-update settings](https://code.claude.com/docs/en/discover-plugins#configure-auto-updates).

### Release checks

Before opening a pull request, run:

```bash
python scripts/validate_repository.py
python scripts/validate_skill_release.py --base origin/main
python -m unittest discover -s scripts -p 'test_*.py'
claude plugin validate plugins/lead-scorer-outreach --strict
claude plugin validate .claude-plugin/marketplace.json --strict
```

## Links

- [MCP documentation](https://lead-scorer.com/mcp-server)
- [Skills library](https://lead-scorer.com/skills)
- [Privacy policy](https://lead-scorer.com/privacy)
- [Terms of service](https://lead-scorer.com/terms)
