#!/usr/bin/env python3
"""Validate the public Lead Scorer plugin repository without third-party packages."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "lead-scorer-outreach"
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
SECRET = re.compile(
    "(?:"
    + "sk_" + "(?:live|test)_|"
    + "wh" + "sec_|"
    + "pri" + "ce_[A-Za-z0-9]|"
    + "BEGIN (?:RSA|OPENSSH|EC) PRIVATE KEY)"
)


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain a JSON object")
    return value


def main() -> int:
    errors: list[str] = []
    paths = {
        "codex_marketplace": ROOT / ".agents" / "plugins" / "marketplace.json",
        "claude_marketplace": ROOT / ".claude-plugin" / "marketplace.json",
        "codex_manifest": PLUGIN / ".codex-plugin" / "plugin.json",
        "claude_manifest": PLUGIN / ".claude-plugin" / "plugin.json",
        "mcp": PLUGIN / ".mcp.json",
    }

    try:
        payloads = {name: load_json(path) for name, path in paths.items()}
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1

    codex_version = payloads["codex_manifest"].get("version")
    versions = {
        codex_version,
        payloads["claude_manifest"].get("version"),
        payloads["claude_marketplace"]["plugins"][0].get("version"),
    }
    if len(versions) != 1 or not isinstance(codex_version, str) or not SEMVER.fullmatch(codex_version):
        errors.append("Codex, Claude, and marketplace versions must use the same strict semver")

    expected_source = "./plugins/lead-scorer-outreach"
    codex_source = payloads["codex_marketplace"]["plugins"][0]["source"].get("path")
    claude_source = payloads["claude_marketplace"]["plugins"][0].get("source")
    if codex_source != expected_source or claude_source != expected_source:
        errors.append(f"both marketplaces must reference {expected_source}")

    expected_repository = "https://github.com/nymphar-ai/lead-scorer-plugin"
    repository_values = {
        payloads["codex_manifest"].get("repository"),
        payloads["claude_manifest"].get("repository"),
        payloads["claude_marketplace"]["plugins"][0].get("repository"),
    }
    if repository_values != {expected_repository}:
        errors.append(f"all published metadata must reference {expected_repository}")

    interface = payloads["codex_manifest"].get("interface", {})
    for field in ("logo", "composerIcon"):
        asset_path = interface.get(field)
        if asset_path != "./assets/logo.png" or not (PLUGIN / "assets" / "logo.png").is_file():
            errors.append(f"Codex interface.{field} must reference ./assets/logo.png")

    mcp = payloads["mcp"].get("mcpServers", {}).get("lead-scorer", {})
    if mcp.get("type") != "http" or mcp.get("url") != "https://mcp.lead-scorer.com/mcp":
        errors.append("the plugin must use the production Lead Scorer Streamable HTTP MCP")
    oauth = mcp.get("oauth", {})
    if oauth.get("scopes") != "leads:read offline_access":
        errors.append("the plugin must request leads:read and offline_access OAuth scopes")

    skill_files = sorted((PLUGIN / "skills").glob("*/SKILL.md"))
    if len(skill_files) != 24:
        errors.append(f"expected 24 Skills, found {len(skill_files)}")
    for path in skill_files:
        content = path.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
        if not match or not re.search(r"(?m)^name:\s*\S+", match.group(1)):
            errors.append(f"{path.relative_to(ROOT)} has invalid or missing frontmatter name")
        if not match or not re.search(r"(?m)^description:\s*.+", match.group(1)):
            errors.append(f"{path.relative_to(ROOT)} has invalid or missing description")

    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if SECRET.search(content):
            errors.append(f"{path.relative_to(ROOT)} contains a forbidden secret-like value")

    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Repository validation passed: {len(skill_files)} Skills, version {codex_version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
