# zai-usage-widget

KDE Plasma 6 panel widget showing **z.ai GLM Coding Plan** quota usage — weekly
and 5-hour percentages, plan badge (e.g. `GLM Max`), credits remaining, and
reset countdowns. Color-coded like its siblings: `claudeusage`, `codexusage`,
`syntheticusage`.

Sister widget docs: `~/.local/share/plasma/plasmoids/USAGE-WIDGETS-HANDOFF.md`.

## How it works

- `contents/code/fetch_usage.py` — reads the API key from
  `~/.local/share/opencode/auth.json` (`zai-coding-plan` or `zai` entry),
  GETs `https://api.z.ai/api/monitor/usage/quota/limit` with the **raw key**
  in `Authorization` (no Bearer prefix).
- Response: `{code,msg,data}` envelope → `data.limits[]`:
  - `unit:3` = 5h quota, `unit:6` = weekly quota
  - `type`: `CREDIT_LIMIT` (GLM Max) or `TOKENS_LIMIT` (token plans) — both handled
  - `percentage` = % used, `usage` = allowance, `remaining` = left,
    `nextResetTime` = ms epoch
- The script emits preformatted display strings + percentages; `main.qml`
  (cloned from `syntheticusage`) just displays them.
- Cache: `~/.local/share/zai-usage-cache.json` (survives restarts, marks stale).

## Install

```bash
ln -s ~/zai-usage-widget ~/.local/share/plasma/plasmoids/org.kde.plasma.zaiusage
# then restart plasmashell and add "Z.ai Usage" to a panel, or via qdbus:
qdbus6 org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript \
  'panels()[0].addWidget("org.kde.plasma.zaiusage")'
```

## Gotchas

- **Never run `kpackagetool6 -u` on this** — the upgrade path deleted the
  package dir once. The symlinked dir is discovered by plasmashell at startup.
- The API is undocumented (reverse-engineered from `opencode-glm-quota` and
  live responses); if quotas go blank, dump the raw response first.
- Config: refresh interval (min 1, default 5 min), show-icon, background
  opacity — same as the other usage widgets.
