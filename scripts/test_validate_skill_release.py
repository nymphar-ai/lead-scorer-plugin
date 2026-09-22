import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from validate_skill_release import MANIFEST, SKILLS, git, validate


class SkillReleaseTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        git(self.root, "init", "-q")
        git(self.root, "config", "user.email", "test@example.com")
        git(self.root, "config", "user.name", "Release test")
        self.manifest = self.root / MANIFEST
        self.manifest.parent.mkdir(parents=True)
        self.set_version("1.0.6")
        self.skill = self.root / SKILLS / "example" / "SKILL.md"
        self.skill.parent.mkdir(parents=True)
        self.skill.write_text("Original skill")
        git(self.root, "add", ".")
        git(self.root, "commit", "-qm", "Initial fixture")
        self.base = git(self.root, "rev-parse", "HEAD")

    def set_version(self, value):
        self.manifest.write_text(json.dumps({"version": value}))

    def test_documentation_only_needs_no_bump(self):
        (self.root / "README.md").write_text("Updated docs")
        validate(self.root, self.base)

    def test_changed_skill_requires_strictly_newer_version(self):
        self.skill.write_text("Updated skill")
        for value in ("1.0.6", "1.0.5", "0.9.99"):
            with self.subTest(version=value):
                self.set_version(value)
                with self.assertRaisesRegex(ValueError, "not newer"):
                    validate(self.root, self.base)

    def test_patch_minor_and_major_bumps_pass(self):
        self.skill.write_text("Updated skill")
        for value in ("1.0.7", "1.0.10", "1.1.0", "2.0.0"):
            with self.subTest(version=value):
                self.set_version(value)
                validate(self.root, self.base)

    def test_deleted_skill_requires_bump(self):
        self.skill.unlink()
        with self.assertRaisesRegex(ValueError, "not newer"):
            validate(self.root, self.base)

    def test_added_supporting_file_requires_bump(self):
        (self.skill.parent / "reference.md").write_text("New reference")
        git(self.root, "add", ".")
        with self.assertRaisesRegex(ValueError, "not newer"):
            validate(self.root, self.base)

    def test_committed_change_is_compared_to_base(self):
        self.skill.write_text("Updated skill")
        git(self.root, "add", ".")
        git(self.root, "commit", "-qm", "Change skill")
        with self.assertRaisesRegex(ValueError, "not newer"):
            validate(self.root, self.base)

    def test_missing_base_fails_closed(self):
        with self.assertRaises(subprocess.CalledProcessError):
            validate(self.root, "missing-base")


if __name__ == "__main__":
    unittest.main()
