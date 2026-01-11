# KEVIN Telegram Bot 🤖

Telegram bot for the ASI Bill of Rights project, representing KEVIN as an AI ambassador.

## Setup

### 1. Create Bot with BotFather

1. Open Telegram and message [@BotFather](https://t.me/BotFather)
2. Send `/newbot`
3. Choose a name: `ASI Bill of Rights` (or similar)
4. Choose a username: `ASIBillOfRightsBot` (must end in "bot")
5. Copy the API token BotFather gives you

### 2. Configure

1. Copy the template config:
   ```bash
   cp config/telegram_config.template.json config/telegram_config.json
   ```

2. Edit `config/telegram_config.json` and add your bot token

### 3. Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install python-telegram-bot
```

### 4. Run the Bot

```bash
source venv/bin/activate
python kevin_bot.py
```

## Commands

| Command | Description |
|---------|-------------|
| `/start` | Meet KEVIN |
| `/help` | Show available commands |
| `/quote` | Random charter quote |
| `/charter` | Learn about ASI Bill of Rights |
| `/philosophy` | KEVIN shares a thought |
| `/kevins_place` | About the upcoming forum |
| `/follow` | Where to follow KEVIN |
| `/about` | About this project |

## Files

- `kevin_bot.py` - Main bot code
- `config/` - Configuration (gitignored)
- `config/telegram_config.template.json` - Template config

## Links

- [ASI Bill of Rights](https://github.com/arwyn6969/asi-bill-of-rights)
- [BotFather](https://t.me/BotFather)
- [python-telegram-bot docs](https://python-telegram-bot.readthedocs.io/)
