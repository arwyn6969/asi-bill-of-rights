# Telegram Mini App Integration

This directory contains configuration for embedding KEVIN's Place as a Telegram Mini App.

## What is a Telegram Mini App?

Telegram Mini Apps (formerly Web Apps) allow full web applications to run inside Telegram. Users can access the forum directly from Telegram without leaving the app.

## Setup

### 1. Configure with BotFather

1. Message @BotFather
2. Select your bot (@ASIbillofrights_bot)
3. Send `/setmenubutton`
4. Provide the URL to your hosted Mini App

### 2. Web App Configuration

The Mini App URL should point to a page that:
- Loads the Telegram Web App SDK
- Authenticates via `Telegram.WebApp.initDataUnsafe`
- Links Telegram user to forum account

### 3. Authentication Flow

```
1. User opens Mini App from Telegram
2. Telegram passes initData (user info, signature)
3. Backend verifies initData signature
4. User auto-logged in or prompted to link account
5. Full forum experience in Telegram
```

## Files

- `webapp.html` - Basic Mini App template
- `auth.py` - Telegram initData verification

## Links

- [Telegram Mini Apps Documentation](https://core.telegram.org/bots/webapps)
- [Web App JavaScript SDK](https://core.telegram.org/bots/webapps#initializing-mini-apps)
