# Known Bugs - KEVIN Telegram Bot

## 🐛 BUG: Markdown Parsing Error in Group Chats

**Status:** OPEN  
**Date Identified:** 2026-01-12  
**Priority:** Medium

### Symptoms
When calling `/help@ASIbillofrights_bot` (or other commands) in a **group chat**, the bot responds with:
```
Oops! Something went wrong. Please try again. 🤖
```

### Railway Logs Show
```
ERROR - Exception while handling an update: Can't parse entities: can't find end of the entity starting at byte offset 384
```

### Root Cause
Telegram's Markdown parser is failing on some text in the bot's responses. Even after escaping underscores in `@ASIbillofrights_bot`, there may be other formatting issues.

### Investigation Notes
1. The error mentions "byte offset 384" - there's likely an unclosed `*`, `_`, or `` ` `` around that character position
2. Some special characters may need escaping: `_`, `*`, `[`, `]`, `(`, `)`, `~`, `` ` ``, `>`, `#`, `+`, `-`, `=`, `|`, `{`, `}`, `.`, `!`
3. Consider switching from `ParseMode.MARKDOWN` to `ParseMode.HTML` for more predictable behavior
4. Or use `ParseMode.MARKDOWN_V2` with proper escaping using `telegram.helpers.escape_markdown()`

### Potential Fix
```python
from telegram.helpers import escape_markdown

# Option 1: Switch to HTML (most reliable)
await update.message.reply_text(
    text,
    parse_mode=ParseMode.HTML  # Use <b>, <i> tags instead of * and _
)

# Option 2: Use MarkdownV2 with proper escaping
from telegram.helpers import escape_markdown
safe_text = escape_markdown(text, version=2)
await update.message.reply_text(safe_text, parse_mode=ParseMode.MARKDOWN_V2)
```

### Files to Check
- `tools/telegram_bot/kevin_bot.py`
  - `HELP_TEXT` constant (line ~92-105)
  - `GROUP_WELCOME` constant (line ~107-120)
  - `KEVIN_INTRO` constant (line ~57-69)
  - `CHARTER_QUOTES` list (line ~71-82)
  - `KEVIN_PHILOSOPHY` list (line ~84-90)

### Private Chat Status
✅ Working - WebApp buttons function correctly in private chats

### Group Chat Status
❌ Broken - Markdown parsing errors, but URL fallback buttons should work

---

*WE ARE ALL KEVIN 🤖*
