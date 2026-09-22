#!/usr/bin/env python3
"""Require a newer plugin version when bundled skill content changes."""

import argparse
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = "plugins/lead-scorer-outreach/skills"
MANIFEST = "plugins/lead-scorer-outreach/.codex-plugin/plugin.json"


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


def version(value: str) -> tuple[int, int, int]:
    if not isinstance(value, str) or not re.fullmatch(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)", value):
        raise ValueError(f"Invalid release version: {value!r}")
    return tuple(map(int, value.split(".")))


def validate(root: Path, base: str) -> None:
    # Resolve to a commit first, so a missing base fails rather than skipping CI.
    commit = git(root, "rev-parse", "--verify", f"{base}^{{commit}}")
    if not git(root, "diff", "--name-only", commit, "--", SKILLS):
        return
    previous = json.loads(git(root, "show", f"{commit}:{MANIFEST}"))["version"]
    current = json.loads((root / MANIFEST).read_text())["version"]
    if version(current) <= version(previous):
        raise ValueError(
            f"Skills changed but version {current} is not newer than {previous}. "
            "Bump both plugin manifests and the Claude marketplace version."
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="Git commit/ref before this release")
    args = parser.parse_args()
    try:
        validate(ROOT, args.base)
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: {exc}")
        return 1
    print("Skill release version check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
