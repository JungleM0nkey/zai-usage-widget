# Plasma Z.ai Usage

A Plasma 6 panel widget for z.ai GLM Coding Plan quotas. It shows weekly and 5-hour usage with reset times.

<img src="docs/widget-preview.png" alt="Z.ai Usage widget showing current quota usage" width="400">

## Requirements

- KDE Plasma 6
- Python 3 and a z.ai GLM Coding Plan API key

The widget picks up the key automatically if you are signed in to the Z.AI Coding
Plan in OpenCode (`~/.local/share/opencode/auth.json`). Alternatively set
`ZAI_API_KEY` in your environment profile.

## Install

```bash
git clone https://github.com/JungleM0nkey/zai-usage-widget.git
cd zai-usage-widget
kpackagetool6 --type Plasma/Applet --install .
```

Open **Add Widgets** and add **Z.ai Usage** to a panel.

The widget asks `api.z.ai/api/monitor/usage/quota/limit` for the quota state
(weekly `unit:6`, 5-hour `unit:3`; credit- and token-based plans both supported).

License: GPL-3.0-or-later.
