# Verification — v0.1.0

Date: 13 November 2026. This records observed tests, not a general autonomy or security certification.

## Runtime and import

- macOS Apple Silicon, Node 24.22.1.
- Published Paperclip runtime **2026.1106.0**, server commit `d69631b01b9c658f80bf8bed389863dce82643e1`.
- Loopback server on port 3188; health endpoint reports `ok`, `local_trusted`, `private`.
- Import preview recognizes five named Codex roles, three workflow/bridge skills, one fictional project and one backlog task.
- Import completed with all five agents paused. Effective adapter, workspace, timeout, disabled bypass, wake settings and per-agent budgets inspected.
- Portable schema 6 produces an informational upstream warning about advanced task timestamps and parent links. The package does not contain that history.
- Two early imports using automatic runner selection failed upstream and left partial companies. Those empty attempts were archived. The package now explicitly selects the legacy adapter and documents that imports can be partial.

## Actual Codex execution

The environment probe passed. A separate manual heartbeat for the development agent then read **only the fictional `site.html` fixture** and returned:

```text
Title: Officina Aurora — laboratorio dimostrativo
Numero di H1: 1
Meta description: presente
REGIA_DEMO_OK
```

The run finished with server status `succeeded`. Its answer matches an independent inspection of the fixture. The agent was paused afterward, its temporary test prompt removed, and manual wake settings disabled again. The final UI shows **0 running, 5 paused, 0 errors**.

This proves one bounded Paperclip → Codex → local-file → result execution. It does not prove an autonomous multi-agent delivery workflow, full ECC/SEO catalog availability in every managed agent home, or a complete SEO/security audit. Those are separate acceptance tests.

## Package and UI checks

- 10 Python tests pass: portable files, forbidden symlinks/files, URL restrictions, workspace validation, preview without writes, duplicate protection, version mismatch, unsafe config rejection and post-import pause verification.
- Independent code review found no high/critical issues in the reviewed package.
- Demo opened in Chrome; selecting SEO changes its detail and pressed state correctly. Visual inspection passed at the tested desktop size. Mobile viewport not separately tested.
- Centro Codex regenerated: dedicated kit card, three existing kit entries total, personal regia skill, demo/guide/repository/release links and localhost link.
- Actual click from the private catalog opened the live Paperclip dashboard. Existing chat-link encoding and no-destination checks pass. The new integration does not auto-submit a message or transfer a chat to Paperclip.
- Personal catalog contents and local screenshots are excluded from the public package.

## Resource observations

At the end of the local trial, `du` reported about **2.3 GiB** for the Paperclip runtime and **404 MiB** for its instance data. Package-manager cache is additional and may be shared with other packages. The starter sources are about 100 KiB before Git history.

These are observations, not disk quotas or future growth guarantees. No model weights were downloaded. No login/background service was installed. A foreground Paperclip process is needed to use the local dashboard; stop it with Ctrl+C when no longer needed.

## Known limits

Budgets rely on reported spend; a subscription-backed run can show zero dollar spend while still consuming account quota. Per-agent concurrency does not cap the entire company. Loopback HTTP does not isolate files accessible to the runtime. The release is an initial integration, not a hardened multi-user deployment.
