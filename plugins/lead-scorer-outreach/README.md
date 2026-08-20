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
- Email campaigns inherit the signature configured on their sender account;
  campaign preflight blocks automatic appending when no effective signature exists.

After installation, ask: `Check my Lead Scorer onboarding status and help me
set up reviewed outreach.`

## What the plugin ships

| Component | Location | Discovery |
| :-------- | :------- | :-------- |
| Claude manifest | `.claude-plugin/plugin.json` | Read on install |
| Codex manifest | `.codex-plugin/plugin.json` | Read on install |
| MCP server | `.mcp.json` | Auto-discovered at plugin root |
| Skills | `skills/<name>/SKILL.md` | Auto-discovered at plugin root |

The MCP entry is a remote Streamable HTTP server at
`https://mcp.lead-scorer.com/mcp`. It carries no credential: the host runs the
OAuth 2.0 flow in the browser on first use and stores the token itself.

## Claude Code

Add the public marketplace and install the plugin:

```bash
claude plugin marketplace add nymphar-ai/lead-scorer-plugin
claude plugin install lead-scorer-outreach@lead-scorer
```

Authenticate the namespaced MCP server:

```bash
claude mcp login plugin:lead-scorer-outreach:lead-scorer
```

For a headless host, append `--no-browser`. Verify the install with:

```bash
claude plugin details lead-scorer-outreach
claude mcp list
```

Update or uninstall with:

```bash
claude plugin marketplace update lead-scorer
claude plugin update lead-scorer-outreach@lead-scorer
claude plugin uninstall lead-scorer-outreach
```

## Codex and ChatGPT Desktop

```bash
git clone https://github.com/nymphar-ai/lead-scorer-plugin.git
codex plugin marketplace add ./lead-scorer-plugin
codex plugin add lead-scorer-outreach@lead-scorer
```

Approve `Lead Scorer Outreach`, authenticate in the browser, then start a new
conversation so the host loads the MCP and all 24 Skills.

## Fallback without the plugin

Claude Code can connect the MCP without installing the Skills:

```bash
claude mcp add --transport http --scope user lead-scorer https://mcp.lead-scorer.com/mcp
```

Codex users can add the same Streamable HTTP URL as `lead_scorer` and run
`codex mcp login lead_scorer`. OAuth signup remains the only account-creation
flow; the plugin never contains a credential.

## Maintaining and publishing

The canonical public distribution source is
`https://github.com/nymphar-ai/lead-scorer-plugin`. Keep the version identical
in both plugin manifests and the Claude marketplace entry.

Run the repository checks before publishing:

```bash
python scripts/validate_repository.py
claude plugin validate plugins/lead-scorer-outreach --strict
claude plugin validate .claude-plugin/marketplace.json --strict
```

See `SUBMISSION.md` for the Anthropic community marketplace metadata and
reviewer checklist.
