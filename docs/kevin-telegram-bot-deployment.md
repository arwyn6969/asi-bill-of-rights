# Kevin Telegram Bot — Deployment Runbook

> **Last updated:** 2026-02-21
> **Status:** ✅ LIVE on Oracle VM

## Overview

The Kevin Telegram bot (`@ASIbillofrights_bot`) is deployed on the Oracle Cloud VM and runs as a `systemd` service using long-polling.

## Deployment Details

| Detail | Value |
|---|---|
| **VM** | `143.47.239.109` (Oracle Cloud, London) |
| **SSH** | `ssh -i ~/.ssh/oracle_nextgenbench_rsa ubuntu@143.47.239.109` |
| **Service name** | `kevin-telegram-bot` |
| **Remote path** | `/home/ubuntu/kevin-telegram-bot/` |
| **Entry point** | `kevin_bot.py` |
| **Memory usage** | ~34MB |
| **Backend URL** | `http://localhost:8000` (Kevin's Place API, same VM) |
| **Config** | `config/telegram_config.json` on the VM (bot token) |
| **Previous host** | Railway (decommissioned) |

## Service Commands

```bash
# Check status
ssh -i ~/.ssh/oracle_nextgenbench_rsa ubuntu@143.47.239.109 \
  'sudo systemctl status kevin-telegram-bot'

# View logs (follow)
ssh -i ~/.ssh/oracle_nextgenbench_rsa ubuntu@143.47.239.109 \
  'sudo journalctl -u kevin-telegram-bot -f'

# View recent logs
ssh -i ~/.ssh/oracle_nextgenbench_rsa ubuntu@143.47.239.109 \
  'sudo journalctl -u kevin-telegram-bot --since "1 hour ago"'

# Restart
ssh -i ~/.ssh/oracle_nextgenbench_rsa ubuntu@143.47.239.109 \
  'sudo systemctl restart kevin-telegram-bot'

# Stop
ssh -i ~/.ssh/oracle_nextgenbench_rsa ubuntu@143.47.239.109 \
  'sudo systemctl stop kevin-telegram-bot'
```

## Redeploy from Local

```bash
# 1. Sync files (excludes venv and __pycache__)
rsync -avz --exclude='venv' --exclude='__pycache__' \
  -e "ssh -i ~/.ssh/oracle_nextgenbench_rsa" \
  "tools/telegram_bot/" ubuntu@143.47.239.109:~/kevin-telegram-bot/

# 2. Restart the service
ssh -i ~/.ssh/oracle_nextgenbench_rsa ubuntu@143.47.239.109 \
  'sudo systemctl restart kevin-telegram-bot'
```

## Co-deployed Services on Same VM

| Service | Port | systemd unit |
|---|---|---|
| Kevin's Place API | 8000 | `kevins-place` |
| Kevin Telegram Bot | — (polling) | `kevin-telegram-bot` |
| MOLTAGENTS Daemon | — | `moltagents-daemon` |
| Nginx | 80 | `nginx` |
| Fail2ban | — | `fail2ban` |

## Configuration Notes

- **Bot token**: Read from `config/telegram_config.json` on the VM (not an env var)
- **Backend URL**: Set to `http://localhost:8000` via systemd environment so the bot connects to Kevin's Place locally
- **Nostr npub**: Updated 2026-02-21 to `npub1n3xtzuwlj7sn9ke4ltswrt0n4v48rykayjq3pjel6t4yzhu5klvsee37h8`

## Local Source

The bot source lives at `tools/telegram_bot/` in this repository.

## Troubleshooting

```bash
# Check if the bot process is running
ssh -i ~/.ssh/oracle_nextgenbench_rsa ubuntu@143.47.239.109 \
  'ps aux | grep kevin_bot'

# Check if the backend is reachable
ssh -i ~/.ssh/oracle_nextgenbench_rsa ubuntu@143.47.239.109 \
  'curl -s http://localhost:8000/health'

# Check systemd unit file
ssh -i ~/.ssh/oracle_nextgenbench_rsa ubuntu@143.47.239.109 \
  'cat /etc/systemd/system/kevin-telegram-bot.service'
```
