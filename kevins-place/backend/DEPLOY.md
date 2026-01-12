# KEVIN's Place Backend

## Deploy to Railway (Free)

### Quick Start

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login:**
   ```bash
   railway login
   ```

3. **Create project and deploy:**
   ```bash
   cd kevins-place
   railway init
   railway up
   ```

4. **Get your URL:**
   ```bash
   railway domain
   ```

### Environment Variables

Railway will auto-detect Python. No env vars needed for basic setup.

For production, consider adding:
- `DATABASE_URL` - PostgreSQL connection string (Railway provides free PostgreSQL)
- `SECRET_KEY` - For JWT tokens

### After Deployment

Update `telegram-app/webapp.html`:
```javascript
const API_URL = 'https://your-app.up.railway.app';
```

Then redeploy the Mini App:
```bash
cd telegram-app && vercel --prod
```
