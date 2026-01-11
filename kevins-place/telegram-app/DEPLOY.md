# KEVIN's Place - Telegram Mini App

Deploy this folder to host the Telegram Mini App.

## Quick Deploy

### Option 1: Vercel (Recommended)
1. Install Vercel CLI: `npm i -g vercel`
2. From this folder: `vercel`
3. Follow prompts, get your URL
4. Update the `API_URL` in webapp.html

### Option 2: Cloudflare Pages
1. Go to https://pages.cloudflare.com
2. Connect your GitHub repo
3. Set root directory to `kevins-place/telegram-app`
4. Deploy!

### Option 3: GitHub Pages
1. Copy `webapp.html` to a `/docs` folder
2. Enable GitHub Pages in repo settings
3. Point to your custom domain or `.github.io`

## After Deployment

1. Get your deployed URL (e.g., `https://kevins-place.vercel.app`)
2. Update `API_URL` in webapp.html to your backend
3. Update `webapp_url` in `tools/telegram_bot/kevin_bot.py`
4. Configure BotFather with the URL

## Files

- `webapp.html` - The Mini App (single file, no build needed)
- `vercel.json` - Vercel deployment config
- `serve.py` - Local testing server
