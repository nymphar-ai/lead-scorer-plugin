import json
import tempfile
import unittest
from pathlib import Path
import zipfile

from build_openai_submission import build, OPENAI_MCP_URL


class OpenAiSubmissionTests(unittest.TestCase):
    def test_complete_archive_preserves_skills_and_uses_reviewed_endpoint(self):
        with tempfile.TemporaryDirectory() as directory:
            path = build(Path(directory))
            original = path.read_bytes()
            with zipfile.ZipFile(path) as archive:
                names = archive.namelist()
                self.assertEqual(len([n for n in names if n.endswith("/SKILL.md")]), 25)
                self.assertNotIn(".claude-plugin/plugin.json", names)
                self.assertNotIn("SUBMISSION.md", names)
                mcp = json.loads(archive.read(".mcp.json"))
                self.assertEqual(mcp["mcpServers"]["lead-scorer"]["url"], OPENAI_MCP_URL)
                manifest = json.loads(archive.read(".codex-plugin/plugin.json"))
                for key in ("logo", "composerIcon"):
                    self.assertIn(manifest["interface"][key].removeprefix("./"), names)
                review = manifest["extensions"]["com.openai"]["review"]
                self.assertEqual(len(review["test_cases"]["positive"]), 5)
                self.assertEqual(len(review["test_cases"]["negative"]), 3)
                self.assertFalse(review["commerce"])
                self.assertNotIn("demo_recording_url", review)
                self.assertNotIn("test_credentials", review)
            self.assertEqual(build(Path(directory)).read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
