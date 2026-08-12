# Lead Scorer Outreach plugin

This universal package connects the hosted Lead Scorer MCP and installs the
outreach Skills generated from the public Lead Scorer Skills catalog.

- Codex and ChatGPT use `.codex-plugin/plugin.json` and `.mcp.json`.
- Claude Code uses `.claude-plugin/plugin.json` and the same `.mcp.json`.
- Both clients authenticate in the browser through Lead Scorer OAuth. A new
  user can sign up during that flow; no API key or card data is copied into the
  plugin.
- Payments always use a hosted Stripe page. Outreach never sends without an
  explicit human approval.

After installation, ask: `Check my Lead Scorer onboarding status and help me
set up reviewed outreach.`

## Install from a fresh host

Claude Code:

```bash
claude plugin marketplace add nymphar-ai/lead-scorer-plugin
claude plugin install lead-scorer-outreach@lead-scorer
```

Codex:

```bash
git clone https://github.com/nymphar-ai/lead-scorer-plugin.git
codex plugin marketplace add ./lead-scorer-plugin
codex plugin add lead-scorer-outreach@lead-scorer
```

Approve `Lead Scorer Outreach`, authenticate in the browser, then start a new
conversation so the host loads the MCP and all 24 Skills.

Fallback without the plugin:

```bash
claude mcp add --transport http --scope user lead-scorer https://mcp.lead-scorer.com/mcp
```

Codex users can add the same Streamable HTTP URL as `lead_scorer` and run
`codex mcp login lead_scorer`. OAuth signup remains the only account-creation
flow; the plugin never contains a credential.
