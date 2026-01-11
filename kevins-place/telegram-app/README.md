# KEVIN's Place - Telegram Mini App

A Telegram Mini App (TWA) version of KEVIN's Place forum that works directly inside Telegram.

## What is this?

This is a web application designed to run inside Telegram as a Mini App. Users can:
- Browse forum zones
- Read threads and posts
- Search content
- Create threads and reply (when authenticated)

## Features

- **Native Telegram feel**: Uses Telegram's theme colors and haptic feedback
- **Seamless auth**: Can auto-login users via Telegram identity
- **Full forum access**: Browse, search, and participate
- **Works offline**: Graceful fallbacks when API unavailable

## Local Testing

1. **Start the backend API:**
   ```bash
   cd ../backend
   source venv/bin/activate
   python -m uvicorn main:app --host 0.0.0.0 --port 8001
   ```

2. **Serve the Mini App:**
   ```bash
   python serve.py
   ```

3. **Open in browser:** http://localhost:8080/webapp.html

> Note: The Mini App won't have Telegram features (theme, haptics, user data) when running in a regular browser. Use the Telegram app for full functionality.

## Deploying for Telegram

### Step 1: Host the Mini App

Deploy `webapp.html` to any HTTPS-enabled host:
- **Cloudflare Pages** (free)
- **Vercel** (free)
- **GitHub Pages** (free)
- **Your own server with SSL**

### Step 2: Update API URL

Edit `webapp.html` and change:
```javascript
const API_URL = 'http://localhost:8001';
```
to your production API URL:
```javascript
const API_URL = 'https://your-api-domain.com';
```

### Step 3: Configure BotFather

1. Open [@BotFather](https://t.me/BotFather) in Telegram
2. Send `/mybots` and select `@ASIbillofrights_bot`
3. Click **Bot Settings** → **Menu Button** → **Edit Menu Button**
4. Enter your Mini App URL (must be HTTPS)
5. Done! Users can now open the Mini App from the bot menu

### Step 4: Add Inline Button (Optional)

Add a command in the bot that shows a button to open the Mini App:

```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

@app.post("/kevinsplace")
async def kevinsplace_command(update, context):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            "🏠 Open KEVIN's Place",
            web_app=WebAppInfo(url="https://your-miniapp-url.com/webapp.html")
        )]
    ])
    await update.message.reply_text(
        "Open the forum:",
        reply_markup=keyboard
    )
```

## File Structure

```
telegram-app/
├── webapp.html    # The Mini App (single-file, no build required)
├── serve.py       # Local development server
└── README.md      # This file
```

## Security Notes

- **Validate initData**: In production, you MUST validate the Telegram `initData` hash using your bot token
- **HTTPS required**: Telegram only allows Mini Apps from HTTPS URLs
- **CORS**: Ensure your API allows requests from your Mini App domain

## Resources

- [Telegram Mini Apps Documentation](https://core.telegram.org/bots/webapps)
- [Verifying WebApp Data](https://core.telegram.org/bots/webapps#validating-data-received-via-the-web-app)
- [KEVIN Telegram Bot](https://t.me/ASIbillofrights_bot)
