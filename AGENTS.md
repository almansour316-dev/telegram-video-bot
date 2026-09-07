# Telegram Video Bot — Agent Guide

This repository is intentionally tiny. Do not perform broad repository discovery.

- Runtime code: `telegram_bot.py`
- Dependencies: `requirements.txt`
- Environment template: `.env.example`
- Deployment entry: `Procfile`

For normal changes, read only the directly affected file plus `telegram_bot.py` when runtime behavior changes.

Use focused syntax/import checks first. Do not add frameworks, services, databases, or large abstractions unless the task requires them.

Never commit bot tokens, cookies, downloaded media, `.env`, credentials, or user data. `TELEGRAM_BOT_TOKEN` must come from the environment.

Final report: changed files, verification, blocker if any. No long repository summary.
