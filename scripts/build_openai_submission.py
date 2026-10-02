#!/usr/bin/env python3
"""Build a complete, reproducible OpenAI ZIP from the canonical plugin sources."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct
from urllib.parse import urlparse
import zipfile

from validate_repository import PLUGIN, ROOT, SECRET, main as validate_repository

OPENAI_MCP_URL = "https://mcp.lead-scorer.com/mcp/openai"


def json_bytes(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def build(output: Path, demo_url: str | None = None) -> Path:
    if validate_repository():
        raise ValueError("Repository checks failed")
    manifest = json.loads((PLUGIN / ".codex-plugin/plugin.json").read_text())
    interface = manifest["interface"]
    for key, limit in {"displayName": 30, "shortDescription": 30, "longDescription": 4000,
                       "developerName": 80}.items():
        if not 0 < len(interface[key]) <= limit:
            raise ValueError(f"interface.{key} must have 1–{limit} characters")
    for key in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
        url = urlparse(interface[key])
        if url.scheme != "https" or not url.netloc or url.username or url.password:
            raise ValueError(f"interface.{key} must be a public HTTPS URL")
    for key in ("logo", "composerIcon"):
        path = PLUGIN / interface[key]
        image = path.read_bytes()
        if image[:8] != b"\x89PNG\r\n\x1a\n" or len(image) > 5 * 1024 * 1024:
            raise ValueError(f"{key} must be a PNG of at most 5 MiB")
        width, height = struct.unpack(">II", image[16:24])
        if width != height or not 48 <= width <= 4096:
            raise ValueError(f"{key} must be square, 48–4096 pixels")
    prompts = interface.get("defaultPrompt", [])
    if len(prompts) > 3 or any(not 0 < len(prompt) <= 128 for prompt in prompts):
        raise ValueError("At most three starter prompts of 1–128 characters are allowed")

    submission = json.loads((ROOT / "submission/openai-review.json").read_text())
    cases = submission["review"]["test_cases"]
    for kind, count in (("positive", 5), ("negative", 3)):
        if len(cases[kind]) != count:
            raise ValueError(f"Expected {count} {kind} review cases")
        fields = ("description", "prompt", "expected_behavior")
        if kind == "positive":
            fields += ("tools_triggered",)
        for case in cases[kind]:
            if any(not isinstance(case.get(key), str) or not case[key].strip() for key in fields):
                raise ValueError(f"Incomplete {kind} review case")
    if demo_url:
        url = urlparse(demo_url)
        if url.scheme != "https" or not url.netloc or url.username or url.password:
            raise ValueError("Demo recording must have a reviewer-accessible HTTPS URL")
        submission["review"]["demo_recording_url"] = demo_url
    manifest["extensions"] = {"com.openai": submission}
    mcp = {"mcpServers": {"lead-scorer": {"url": OPENAI_MCP_URL}}}

    files = {
        ".codex-plugin/plugin.json": json_bytes(manifest),
        ".mcp.json": json_bytes(mcp),
    }
    for directory in ("skills", "assets"):
        for path in sorted((PLUGIN / directory).rglob("*")):
            if path.is_symlink():
                raise ValueError(f"Symlinks are not allowed: {path}")
            if not path.is_file():
                continue
            if path.suffix not in (".md", ".png", ".svg"):
                raise ValueError(f"Unexpected bundled file: {path}")
            files[path.relative_to(PLUGIN).as_posix()] = path.read_bytes()
    for name, data in files.items():
        if SECRET.search(data.decode("utf-8", errors="ignore")):
            raise ValueError(f"Secret-like value in {name}")
    output.mkdir(parents=True, exist_ok=True)
    destination = output / f"lead-scorer-outreach-{manifest['version']}-openai.zip"
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    with zipfile.ZipFile(destination) as archive:
        if archive.testzip() is not None:
            raise ValueError("ZIP integrity verification failed")
    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    destination.with_suffix(".zip.sha256").write_text(f"{digest}  {destination.name}\n")
    print(f"Built {destination} ({len(files)} files; SHA-256 {digest})")
    if not demo_url:
        print("DRAFT: demo recording, reviewer credentials, live test execution and portal checks remain required.")
    return destination


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist/openai")
    parser.add_argument("--demo-recording-url")
    args = parser.parse_args()
    build(args.output_dir, args.demo_recording_url)
