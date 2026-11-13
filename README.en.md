# Codex Regia

**A small, tested Paperclip starter team for OpenAI Codex — with bridges to Codex Engineering Kit and Codex SEO.**

Five roles, three workflow skills, a fictional project and a local-only importer. Agents arrive **paused**: importing a team does not start an autonomous company.

[Italian guide](docs/GUIDA-IT.md) · [Interactive demo](examples/index.html) · [Verification](docs/VERIFICATION.md) · [Paperclip upstream](https://github.com/paperclipai/paperclip)

## What you get

| Role | Responsibility |
|---|---|
| Coordinator | Scope, acceptance criteria and evidence |
| Engineer | Small changes and reproducible tests |
| Quality reviewer | Independent checks and regressions |
| Security reviewer | Review inside the authorized project |
| SEO specialist | Content and technical SEO, with explicit evidence limits |

Included skills: `regia-workflow`, `ecc-bridge`, `seo-bridge`. The bridges **do not vendor or automatically install** the full ECC/SEO catalogs. They ask the agent to verify availability before using them and clearly report missing dependencies. Install the kits separately from [Codex Engineering Kit](https://github.com/DennisResponsa/codex-engineering-kit) and [Codex SEO](https://github.com/DennisResponsa/codex-seo).

## Quick start

Requirements: Node.js >=24.11, Python >=3.10, Codex CLI installed and signed in. Paperclip is pinned to **2026.1106.0**. No API key or credential belongs in this repository.

```sh
git clone https://github.com/DennisResponsa/codex-regia.git
cd codex-regia
python3 scripts/regia.py check
python3 -m unittest discover -s tests -v
```

Open `examples/index.html` directly for an offline, interactive explanation. It is a **configuration demo**, not a live dashboard or a fabricated execution trace.

Start the actual Paperclip app in a terminal, without installing a background service:

```sh
PORT=3188 npx --yes paperclipai@2026.1106.0 onboard \
  --data-dir "$HOME/.local/share/codex-regia/instance" \
  --bind loopback --yes --no-install-service
```

In another terminal, from this repository:

```sh
python3 scripts/regia.py preview --workspace examples
python3 scripts/regia.py import --workspace examples
```

Open **http://127.0.0.1:3188**. You should see `Codex Regia Demo`, five paused agents, three skills, one project and one unassigned backlog task. The importer verifies the effective configuration after import. Re-importing a company with the same name is refused.

Stop the server with Ctrl+C. To reopen an initialized instance:

```sh
npx --yes paperclipai@2026.1106.0 run \
  --data-dir "$HOME/.local/share/codex-regia/instance"
```

## First real task

Choose the demo workspace first. In Paperclip, configure the selected agent, resume **only that agent**, and enable its manual/on-demand wake setting. Timers, assignment wakeups and automation wakeups remain disabled in the starter. Assign a bounded task such as reading `site.html` and reporting its title, H1 count and description. After the run, check its output and restore the paused state. Do not use “Resume all” as a substitute for configuring permissions and scope.

The imported `legacy` runner is intentional: this tested version rejects the explicit `dangerouslyBypassApprovalsAndSandbox: false` configuration on the native-runner import path. The legacy adapter keeps the bypass disabled. Paperclip remains responsible for execution; this package does not replace its runtime.

## Limits and resource use

- Local web app, not an offline model: running Codex normally communicates with OpenAI.
- Loopback binding limits access to the web app; it does **not** isolate an agent from every file or network resource. The actual runtime permissions matter.
- 180-second adapter timeout; one concurrent run **per agent**, not a global concurrency cap.
- Starter budget: 500 cents per agent/month. This is Paperclip's reported-spend budget, not an OpenAI billing cap or subscription-quota guarantee; in-flight usage can overshoot.
- No hard disk quota is implemented. The measured Mac runtime is documented in the verification report. Database, logs and package caches need monitoring.
- No background service, recurring routine or client project is installed by this importer. The app itself runs while its terminal is open.
- Upstream imports are not fully transactional. An upstream failure can leave a partial company; inspect/archive it before retrying. The importer does not retry automatically.
- Schema 6 intentionally omits advanced task history; the upstream preview may warn that timestamps and parent links are not transferred. The starter has neither.

## Development

`team.json` is the machine-readable adapter configuration; `company/.paperclip.yaml` is the matching Paperclip format. The check rejects differences. Markdown files use Paperclip's supported YAML subset. Run tests after editing.

This is an independent **integration package**, not a fork, model, replacement for ChatGPT, or official OpenAI/Paperclip distribution. Original company instructions and demo are MIT-licensed. See [NOTICE](NOTICE.md). No private Centro Codex catalog, customer files, chat IDs or credentials are included.
