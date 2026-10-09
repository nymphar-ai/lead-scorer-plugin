# OpenAI directory submission

The release package is built from the canonical skills and branding. It uses
the stable OpenAI distribution endpoint `/mcp/openai`, which omits digital-service
commerce for all users. The Git marketplace continues to use `/mcp`.
OpenAI accepts the Codex manifest format with `extensions.com.openai`.

## Build

```bash
python3 scripts/build_openai_submission.py
```

The complete ZIP and SHA-256 are written to `dist/openai/`. The archive contains
the manifest, one HTTPS MCP endpoint, all 28 skills and the referenced branding.
It excludes the Claude manifest, repository configuration and private credentials.

## Live review preparation

The eight cases in `openai-review.json` are **review scripts, not recorded passing
test results**. Before submission, run them using a dedicated account with
synthetic data and record observed outputs, including the final draft state.
Execute the five positive cases in order; they establish shared demo fixtures.
Retain that account and data for subsequent reviews. It must be accessible to
reviewers without private-network access, email/SMS verification or MFA approval.

Record a walkthrough of the actual connected plugin and the cases. Upload it to
an approved reviewer-accessible location, then rebuild with its real URL:

```bash
python3 scripts/build_openai_submission.py --demo-recording-url '<recording HTTPS URL>'
```

Do not add credentials or reviewer login instructions to this public repository
or ZIP. Enter them only in the portal's secure Review details form.

## Portal

1. Use a verified developer identity in the owning OpenAI organization and a
   project eligible for MCP submission.
2. Open <https://platform.openai.com/plugins> and upload the complete ZIP.
3. Connect `https://mcp.lead-scorer.com/mcp/openai`, complete OAuth and the domain
   challenge shown by the portal, and inspect all skill and tool scan findings.
4. Enter the dedicated review account details. Check the imported eight cases,
   real video URL, public listing URLs and release notes.
5. Resolve required findings, submit for review, and publish the approved version.

The domain challenge token is supplied by the portal; do not invent one. Serve
it as plain text at the exact permitted `/.well-known/openai-apps-challenge` URL.
Do not replace a challenge used by another plugin.

## Submission status

Preparing this repository or building the ZIP does not submit or publish it.
The portal is authoritative for ownership verification, scan results, review
status and publication. Record the plugin ID and listing URL after creation.

Sources: [submission workflow](https://developers.openai.com/plugins/deploy/submission),
[commerce policy](https://developers.openai.com/plugins/plugin-guidelines#commerce-and-monetization).
