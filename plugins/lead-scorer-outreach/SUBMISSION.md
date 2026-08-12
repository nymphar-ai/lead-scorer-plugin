# Community marketplace submission dossier

Prepared material for submitting **Lead Scorer Outreach** to Anthropic's
community marketplace. Nothing has been submitted from this repository.

## Public source

- Repository: <https://github.com/nymphar-ai/lead-scorer-plugin>
- Marketplace manifest: `.claude-plugin/marketplace.json`
- Plugin source: `plugins/lead-scorer-outreach/`
- Install name from this marketplace: `lead-scorer-outreach@lead-scorer`

The repository is public and contains no credential. The plugin connects to the
hosted Lead Scorer MCP over OAuth.

## Submission forms

- Console: <https://platform.claude.com/plugins/submit>
- Claude admin directory: <https://claude.ai/admin-settings/directory/submissions/plugins/new>
- Community shortcut: <https://clau.de/plugin-directory-submission>

## Metadata

| Field | Value |
| :---- | :---- |
| Plugin name | `lead-scorer-outreach` |
| Display name | Lead Scorer Outreach |
| Version | 1.0.1 |
| Category | Productivity |
| Author | Lead Scorer |
| Author URL | <https://lead-scorer.com> |
| Support email | support@lead-scorer.com |
| Homepage | <https://lead-scorer.com/mcp-server> |
| Repository | <https://github.com/nymphar-ai/lead-scorer-plugin> |
| Privacy policy | <https://lead-scorer.com/privacy> |
| Terms of service | <https://lead-scorer.com/terms> |
| License | UNLICENSED |
| Keywords | outreach, sales, crm, mcp, lead-generation |

### Short description

> Lead Scorer OAuth MCP and reviewed outreach skills for Claude Code.

### Long description

> Lead Scorer Outreach connects Claude Code to the hosted Lead Scorer MCP over
> OAuth and installs 24 outreach playbooks covering sourcing, enrichment,
> scoring, cold email, LinkedIn, reply triage, and CRM hygiene.
>
> The plugin ships no credential. On first use, Claude Code runs the OAuth 2.0
> flow in the browser against `https://mcp.lead-scorer.com/mcp`; new users can
> create an account during that flow. Payments always go through a hosted Stripe
> page, and no card data reaches the plugin or the agent.
>
> Outreach is review-first by design: the skills draft messages into a campaign
> and never send. Activating or sending requires an explicit human approval step.

### Suggested first prompts

- "Check my Lead Scorer onboarding status and help me set up reviewed outreach."
- "Help me set up a reviewed outbound campaign with Lead Scorer."

## Reviewer checklist

- Claude and Codex manifests declare the same semantic version.
- The marketplace source resolves to `./plugins/lead-scorer-outreach`.
- The bundle contains 24 reviewed skills and one remote Streamable HTTP MCP.
- OAuth scope is pinned to `leads:read`.
- The plugin contains no hooks, bundled executables, or credentials.
- `assets/logo.png` and `assets/logo.svg` contain the marketplace branding.

Run before submission:

```bash
python scripts/validate_repository.py
claude plugin validate plugins/lead-scorer-outreach --strict
claude plugin validate .claude-plugin/marketplace.json --strict
```

## Branding note

`assets/logo.png` and `assets/logo.svg` are consumed by the Codex/ChatGPT
manifest through `interface.logo` and `interface.composerIcon`. The current
Claude Code plugin manifest schema has no logo field, so the Claude manifest
deliberately does not reference the assets.
