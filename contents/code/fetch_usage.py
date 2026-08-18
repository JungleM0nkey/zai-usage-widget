#!/usr/bin/env python3
"""Fetch z.ai GLM Coding Plan quota from /api/monitor/usage/quota/limit.

Reads the API key from ~/.local/share/opencode/auth.json ("zai-coding-plan").
Auth header carries the raw key (no Bearer prefix).
Emits preformatted display strings + percentages; QML just displays them.
Outputs {"ok":true,"data":{...}} or {"ok":false,"error":"..."} on stdout.
"""
import json
import os
import urllib.request

AUTH_FILE = os.path.expanduser("~/.local/share/opencode/auth.json")
API_URL = "https://api.z.ai/api/monitor/usage/quota/limit"
TIMEOUT = 15


def get_api_key():
    # 1. opencode auth.json (z.ai coding plan login)
    try:
        with open(AUTH_FILE) as f:
            auth = json.load(f)
    except (OSError, ValueError):
        auth = {}
    for provider in ("zai-coding-plan", "zai"):
        entry = auth.get(provider)
        if isinstance(entry, dict) and isinstance(entry.get("key"), str):
            return entry["key"]
        if isinstance(entry, str):
            return entry
    # 2. ZAI_API_KEY in the environment
    return os.environ.get("ZAI_API_KEY")


def fmt_num(n):
    if n is None:
        return "?"
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.0f}K"
    return str(n)


def main():
    key = get_api_key()
    if not key:
        print(json.dumps({"ok": False, "error": "API key not found in opencode auth.json"}))
        return
    try:
        req = urllib.request.Request(API_URL, headers={"Authorization": key})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            raw = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(json.dumps({"ok": False, "error": "HTTP " + str(e.code)}))
        return
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}))
        return

    if isinstance(raw.get("data"), dict):  # unwrap {code,msg,data} envelope
        raw = raw["data"]
    limits = raw.get("limits") or []

    # unit 3 = 5h window, unit 6 = weekly; type TOKENS_LIMIT or CREDIT_LIMIT depending on plan
    def find(unit):
        return next((l for l in limits if l.get("unit") == unit and l.get("type") in ("TOKENS_LIMIT", "CREDIT_LIMIT")), None)

    five_h, weekly = find(3), find(6)

    data = {
        "plan": ("GLM " + (raw.get("level") or "").capitalize()).strip(),
        "hasSecondary": five_h is not None,
    }

    if weekly is not None:
        data["primaryPercent"] = max(0.0, weekly.get("percentage") or 0)
        data["primaryResetTs"] = weekly.get("nextResetTime")
        remaining, total = weekly.get("remaining"), weekly.get("usage")
        if remaining is not None and total:
            data["credits"] = f"{fmt_num(remaining)} / {fmt_num(total)} credits"
    else:
        data["primaryPercent"] = 0

    if five_h is not None:
        data["secondaryPercent"] = max(0.0, five_h.get("percentage") or 0)
        data["secondaryResetTs"] = five_h.get("nextResetTime")

    print(json.dumps({"ok": True, "data": data}))


if __name__ == "__main__":
    main()
