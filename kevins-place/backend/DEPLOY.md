# KEVIN's Place Backend Deployment

## 🚀 Overview

This backend is built with **FastAPI** and supports both **SQLite** (development) and **PostgreSQL** (production).

---

## 🛠️ Deployment on Railway

### 1. Prerequisites
- **Railway CLI**: `npm i -g @railway/cli`
- **Railway Account**: [railway.app](https://railway.app)

### 2. Quick Deploy
1. **Login & Init**:
   ```bash
   railway login
   cd kevins-place
   railway init
   ```

2. **Add PostgreSQL Database**:
   - Run `railway add`
   - Select **PostgreSQL**
   - Railway will automatically inject `DATABASE_URL` into your environment variables.

3. **Deploy**:
   ```bash
   railway up
   ```

### 3. Environment Variables (Production)
Ensure these variables are set in your Railway project settings:

| Variable | Description | Example |
| :--- | :--- | :--- |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `SECRET_KEY` | Secret for JWT & signing | `openssl rand -hex 32` |
| `CORS_ORIGINS` | Allowed frontend domains | `https://your-frontend.vercel.app` |
| `TELEGRAM_BOT_TOKEN` | Token for the KEVIN bot | `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11` |

### 4. Verification
- Visit `https://your-app.up.railway.app/docs` inside your browser.
- You should see the Swagger UI.
- Try the `/api/health` or `/` endpoint to confirm it's running.

---

## 🤖 Telegram Bot Worker
To keep the bot running 24/7, deploy it as a separate **Worker** service sharing the same Repo/Env.

1. Create a new Service in Railway.
2. Link to the same GitHub Repo.
3. Set **Start Command**:
   ```bash
   python tools/telegram_bot/kevin_bot.py
   ```
   *(Ensure PYTHONPATH includes the backend root if sharing code)*

