import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import regia


class PackageTests(unittest.TestCase):
    def test_valid_bundle(self):
        self.assertEqual(len(regia.bundle()), 12)

    def test_local_url_only(self):
        self.assertEqual(regia.validate_url("http://127.0.0.1:3188/"), "http://127.0.0.1:3188")
        for url in ["https://example.com", "http://localhost:3188", "http://127.0.0.1", "http://127.0.0.1:3188/x", "http://user@127.0.0.1:3188", "http://127.0.0.1:3188?q=x"]:
            with self.subTest(url=url), self.assertRaises(ValueError):
                regia.validate_url(url)

    def test_workspace_not_home(self):
        for directory in [Path.home(), Path("/")]:
            with self.assertRaises(ValueError):
                regia.request_body(directory)

    def test_portable_source_unchanged(self):
        before = regia.bundle()
        body = regia.request_body(regia.ROOT / "examples")
        self.assertTrue(body["pauseAutomations"])
        self.assertIn(str(regia.ROOT / "examples"), body["source"]["files"][".paperclip.yaml"])
        self.assertEqual(before, regia.bundle())

    def test_rejects_symlink_and_unknown_file(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(regia.ROOT / "company", root / "company")
            shutil.copy(regia.ROOT / "team.json", root)
            extra = root / "company" / "private.env"
            extra.write_text("test")
            with self.assertRaises(ValueError): regia.bundle(root)
            extra.unlink()
            extra.symlink_to(root / "team.json")
            with self.assertRaises(ValueError): regia.bundle(root)

    def test_rejects_unsafe_configuration(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(regia.ROOT / "company", root / "company")
            config = json.loads((regia.ROOT / "team.json").read_text())
            config["agents"]["engineer"]["adapter"]["config"]["dangerouslyBypassApprovalsAndSandbox"] = True
            (root / "team.json").write_text(json.dumps(config))
            (root / "company/.paperclip.yaml").write_text(regia.yaml_text(config))
            with self.assertRaises(ValueError): regia.bundle(root)

    @patch("regia.api")
    def test_preview_never_imports(self, api):
        api.side_effect = [{"status": "ok", "version": regia.VERSION, "deploymentMode": "local_trusted"}, [], {"errors": [], "plan": {}}]
        self.assertEqual(regia.import_team("http://127.0.0.1:3188", regia.ROOT / "examples")["mode"], "preview")
        self.assertNotIn("/api/companies/import", [x.args[1] for x in api.call_args_list])

    @patch("regia.api")
    def test_existing_company_no_duplicate(self, api):
        api.side_effect = [{"status": "ok", "version": regia.VERSION, "deploymentMode": "local_trusted"}, [{"name": "Codex Regia Demo"}]]
        with self.assertRaises(ValueError): regia.import_team("http://127.0.0.1:3188", regia.ROOT / "examples", True)
        self.assertEqual(api.call_count, 2)

    @patch("regia.api")
    def test_live_verification_rejects_unpaused_agents(self, api):
        api.side_effect = [{"status": "ok", "version": regia.VERSION, "deploymentMode": "local_trusted"}, [], {"errors": []}, {"company": {"id": "demo"}}, [{"status": "idle"}] * 5]
        with self.assertRaisesRegex(ValueError, "pause verification"):
            regia.import_team("http://127.0.0.1:3188", regia.ROOT / "examples", True)

    @patch("regia.api")
    def test_version_mismatch_fails_before_writes(self, api):
        api.return_value = {"status": "ok", "version": "other", "deploymentMode": "local_trusted"}
        with self.assertRaises(ValueError): regia.import_team("http://127.0.0.1:3188", regia.ROOT / "examples", True)
        self.assertEqual(api.call_count, 1)


if __name__ == "__main__":
    unittest.main()
