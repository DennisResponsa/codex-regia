#!/usr/bin/env python3
"""Small, dependency-free importer for a paused Paperclip Codex team."""
import argparse
import json
from pathlib import Path
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
VERSION = "2026.1106.0"


def yaml_text(value, depth=0):
    """Emit the small YAML subset used by Paperclip's portable format."""
    lines = []
    prefix = "  " * depth
    entries = value.items() if isinstance(value, dict) else enumerate(value)
    for key, item in entries:
        label = f"{key}:" if isinstance(value, dict) else "-"
        if isinstance(item, (dict, list)) and item:
            lines.extend([prefix + label, yaml_text(item, depth + 1).rstrip()])
        else:
            lines.append(prefix + label + " " + json.dumps(item, ensure_ascii=False))
    return "\n".join(lines) + "\n"


def bundle(root=ROOT):
    """Read only package files, never the user's Codex configuration."""
    base = root / "company"
    files = {}
    for path in sorted(base.rglob("*")):
        if path.is_symlink():
            raise ValueError("Package symlinks are not allowed")
        if path.is_file():
            name = path.relative_to(base).as_posix()
            if path.suffix != ".md" and name != ".paperclip.yaml":
                raise ValueError("Unexpected package file: " + name)
            files[name] = path.read_text(encoding="utf-8")
    if "COMPANY.md" not in files or ".paperclip.yaml" not in files:
        raise ValueError("Incomplete company package")
    if len(json.dumps(files).encode()) > 500_000:
        raise ValueError("Package exceeds the 500 KB starter limit")
    config = json.loads((root / "team.json").read_text())
    if files[".paperclip.yaml"] != yaml_text(config):
        raise ValueError("Portable YAML differs from team.json")
    if len(config["agents"]) != 5:
        raise ValueError("Expected five starter roles")
    for slug, agent in config["agents"].items():
        if f"agents/{slug}/AGENTS.md" not in files:
            raise ValueError("Missing instructions for " + slug)
        adapter = agent["adapter"]
        if adapter["type"] != "codex_local":
            raise ValueError("Only the Codex local adapter is allowed")
        if adapter.get("runner") != "legacy":
            raise ValueError("The tested adapter requires an explicit legacy runner")
        if adapter["config"].get("dangerouslyBypassApprovalsAndSandbox") is not False:
            raise ValueError("Approval bypass must be explicitly disabled")
        if "env" in adapter["config"] or "cwd" in adapter["config"]:
            raise ValueError("Portable package must not contain local environment or paths")
        hb = agent["runtime"]["heartbeat"]
        if hb.get("enabled") is not False or hb.get("maxConcurrentRuns") != 1:
            raise ValueError("Starter must be dormant and sequential per agent")
        for flag in ("wakeOnAssignment", "wakeOnOnDemand", "wakeOnAutomation", "wakeOnDemand"):
            if hb.get(flag) is not False:
                raise ValueError("Automatic wakeups must be disabled")
        if not 0 < agent["budgetMonthlyCents"] <= 500:
            raise ValueError("Starter budget must be between 1 and 500 cents")
    return files


def request_body(workspace, root=ROOT):
    folder = Path(workspace).expanduser().resolve(strict=True)
    if not folder.is_dir() or folder in (Path.home(), Path("/")):
        raise ValueError("Choose a dedicated project directory")
    files = bundle(root)
    config = json.loads((root / "team.json").read_text())
    for agent in config["agents"].values():
        agent["adapter"]["config"]["cwd"] = str(folder)
    files[".paperclip.yaml"] = yaml_text(config)
    return {
        "source": {"type": "inline", "files": files, "expectedFileCount": len(files)},
        "target": {"mode": "new_company", "newCompanyName": "Codex Regia Demo"},
        "include": {"company": True, "agents": True, "skills": True, "projects": True, "issues": True},
        "agents": "all", "collisionStrategy": "rename", "pauseAutomations": True,
    }


def validate_url(url):
    parsed = urllib.parse.urlsplit(url)
    if (parsed.scheme != "http" or parsed.hostname != "127.0.0.1"
            or parsed.username or parsed.password or parsed.query or parsed.fragment
            or parsed.path not in ("", "/") or not parsed.port):
        raise ValueError("Use an explicit local URL, e.g. http://127.0.0.1:3188")
    return url.rstrip("/")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("Redirect refused: local-only operation")


def api(base, path, data=None):
    base = validate_url(base)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    raw = None if data is None else json.dumps(data).encode()
    req = urllib.request.Request(base + path, data=raw, headers={"Content-Type": "application/json"})
    with opener.open(req, timeout=90) as response:
        return json.load(response)


def import_team(base, workspace, apply=False):
    health = api(base, "/api/health")
    if health.get("status") != "ok" or health.get("deploymentMode") != "local_trusted":
        raise ValueError("A healthy local_trusted Paperclip instance is required")
    if health.get("version") != VERSION:
        raise ValueError("This release is tested against Paperclip " + VERSION)
    body = request_body(workspace)
    companies = api(base, "/api/companies")
    if any(c.get("name") == body["target"]["newCompanyName"] for c in companies):
        raise ValueError("Codex Regia Demo already exists; no duplicate imported")
    preview = api(base, "/api/companies/import/preview", body)
    if preview.get("errors"):
        raise ValueError("Import preview failed: " + json.dumps(preview["errors"]))
    if not apply:
        return {"mode": "preview", "plan": preview.get("plan"), "warnings": preview.get("warnings", [])}
    try:
        result = api(base, "/api/companies/import", body)
    except (ValueError, OSError) as exc:
        raise ValueError("Import failed and may have left a partial company. Inspect Paperclip before retrying. " + str(exc)) from exc
    cid = result["company"]["id"]
    agents = api(base, "/api/companies/" + urllib.parse.quote(cid, safe="") + "/agents")
    if len(agents) != 5 or any(a.get("status") != "paused" for a in agents):
        raise ValueError("Import created a company but pause verification failed. Stop and inspect it in Paperclip.")
    expected = json.loads((ROOT / "team.json").read_text())["agents"]["engineer"]
    for agent in agents:
        config = agent.get("adapterConfig", {})
        heartbeat = agent.get("runtimeConfig", {}).get("heartbeat", {})
        if (agent.get("adapterType") != "codex_local"
                or config.get("cwd") != str(Path(workspace).expanduser().resolve())
                or config.get("dangerouslyBypassApprovalsAndSandbox") is not False
                or config.get("timeoutSec") != 180
                or agent.get("budgetMonthlyCents") != 500
                or any(heartbeat.get(k) != v for k, v in expected["runtime"]["heartbeat"].items())):
            raise ValueError("Imported configuration differs from the starter. Agents remain paused; inspect Paperclip.")
    return {"mode": "imported", "company": result["company"], "pausedAgents": len(agents),
            "warnings": result.get("warnings", [])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["check", "preview", "import"])
    parser.add_argument("--url", default="http://127.0.0.1:3188")
    parser.add_argument("--workspace", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "check":
            print(json.dumps({"valid": True, "files": len(bundle()), "roles": 5}))
        else:
            if args.workspace is None:
                parser.error("--workspace is required for preview/import")
            print(json.dumps(import_team(args.url, args.workspace, args.command == "import"), ensure_ascii=False, indent=2))
    except (ValueError, KeyError, OSError, urllib.error.URLError) as exc:
        print("ERROR: " + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
