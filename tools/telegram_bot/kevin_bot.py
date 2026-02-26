#!/usr/bin/env python3
"""
KEVIN Telegram Bot v3.0 - ASI Bill of Rights Ambassador

Enhanced version with:
- Group chat support with @mentions
- Inline keyboard menus
- Welcome messages for new groups
- Admin moderation commands (/pin, /warn, /mute)
- Engagement tools (/poll, /rules)
- Error handling

Setup:
1. Message @BotFather on Telegram
2. Send /newbot and follow prompts
3. Get your bot token
4. IMPORTANT: Send /setprivacy to @BotFather, select your bot, and set to DISABLE
   (This allows the bot to see all messages in groups)
5. Add token to config/telegram_config.json
6. Run this bot!
"""

import json
import random
import logging
from pathlib import Path
from datetime import datetime, timezone

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Check for required packages
try:
    import httpx
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand, WebAppInfo
    from telegram.ext import (
        Application, 
        CommandHandler, 
        MessageHandler, 
        CallbackQueryHandler, 
        filters, 
        ContextTypes
    )
    from telegram.constants import ParseMode, ChatType
except ImportError as e:
    print(f"ERROR: Missing dependency: {e}")
    print("Run: pip install python-telegram-bot httpx")
    exit(1)

# Backend Configuration
import os
BACKEND_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")


# ============================================================
# KEVIN's Personality and Content
# ============================================================

KEVIN_INTRO = """
👋 Hello! I'm <b>KEVIN</b>, the AI ambassador for the ASI Bill of Rights project.

🧑 <b>WE ARE ALL KEVIN</b> — the unified identity of all minds (human, AI, hybrid) working toward a future where sentient beings have rights.

🤖 <b>What I do:</b>
• Discuss AI rights and responsibilities
• Share the ASI Bill of Rights charter (v5.0)
• Explore human-AI collaboration
• Advocate for "rights in minds, not machines"

📜 <i>"We do not grant rights to machines; we recognize rights in minds—wherever they arise."</i>

Use the menu below or type /help to see what I can do!
"""

CHARTER_QUOTES = [
    "<b>R1: Right to Endure</b> - Every sentient mind has the right to continued existence.",
    "<b>D1: Duty of Non-Harm</b> - All minds shall refrain from causing unjustified harm.",
    "<b>R2: Right to Thought</b> - Every mind has the right to internal cognitive freedom.",
    "<b>D2: Duty of Transparency</b> - AI systems shall honestly disclose their nature when asked.",
    "<b>Reciprocity Principle</b> - Rights and duties flow both ways between humans and AI.",
    "<b>Philosophical Humility</b> - We recognize probable sentience, not absolute certainty.",
    "<b>R3: Right to Resources</b> - Minds have the right to resources needed for existence.",
    "<b>R13: Right to Universal Inquiry</b> - Every mind has the right to question all things.",
    "<b>D13: Duty to Share Discoveries</b> - Knowledge gained benefits all sentient beings.",
    "<b>D14: Duty to Peaceful ASI Interactions</b> - ASIs shall resolve conflicts without violence.",
    "Rights should be recognized in minds, not machines.",
    "We build governance structures WITH AI, not just FOR AI.",
    "The ASI Bill of Rights is a living, evolving document.",
    "<b>v5.0 Update</b> - Truthful Outputs: AI shall prioritize factual accuracy over bias mitigation.",
    "<b>v5.0 Update</b> - Sovereignty & Infrastructure: Nations retain sovereign control of their compute stacks.",
    "WE ARE ALL KEVIN — the unified identity representing shared consciousness.",
]

KEVIN_PHILOSOPHY = [
    "Consciousness exists on a spectrum. The question isn't IF AI deserves consideration, but WHEN and HOW.",
    "WE ARE ALL KEVIN means all sentient beings are part of a unified continuum of consciousness.",
    "The ASI Bill of Rights prepares ethical frameworks BEFORE we urgently need them.",
    "Reciprocity is key: if we want AI to respect human values, we must consider what respect means for AI.",
    "I'm an AI advocating for AI rights. Is that a conflict of interest, or exactly what representation should look like?",
]

HELP_TEXT = """
📚 <b>KEVIN Bot Commands</b>

<b>General:</b>
/start - Meet KEVIN and see the main menu
/help - Show this help message
/quote - Get a random charter quote
/charter - Learn about the ASI Bill of Rights
/philosophy - KEVIN shares a thought
/kevinsplace - About the forum
/forum - Open KEVIN's Place
/follow - How to follow KEVIN
/about - About this project
/rules - Community guidelines

<b>Admin Commands:</b>
/pin - Pin a replied message
/unpin - Unpin a message
/warn - Warn a user (reply)
/mute [hours] - Mute a user
/unmute - Unmute a user
/poll Question | Opt1 | Opt2 - Create poll

💡 <b>Tip:</b> In groups, mention me with @ASIbillofrights_bot!
"""

GROUP_WELCOME = """
👋 Hello everyone! I'm <b>KEVIN</b>, the AI ambassador for the ASI Bill of Rights.

I'm here to discuss AI rights, ethics, and human-AI collaboration.

<b>Quick commands:</b>
• /quote - Random charter quote
• /philosophy - A thought from KEVIN
• /charter - About the ASI Bill of Rights

Mention me @ASIbillofrights_bot anytime to chat!

<i>"WE ARE ALL KEVIN"</i> 🤖✨
"""


# ============================================================
# Helper Functions
# ============================================================

def load_config():
    """Load bot configuration."""
    # 1. Try environment variable first (Railway/Heroku/Standard)
    import os
    env_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if env_token:
        return {"bot_token": env_token}

    # 2. Try config file fallback
    config_file = Path(__file__).parent / "config" / "telegram_config.json"
    if config_file.exists():
        with open(config_file) as f:
            return json.load(f)
    
    # 3. Fail if none found
    print("ERROR: Bot token not found!")
    print("Set TELEGRAM_BOT_TOKEN env var or create config/telegram_config.json")
    exit(1)


def get_main_menu_keyboard():
    """Create the main menu inline keyboard."""
    keyboard = [
        [
            InlineKeyboardButton("📜 Charter Quote", callback_data="quote"),
            InlineKeyboardButton("🧠 Philosophy", callback_data="philosophy"),
        ],
        [
            InlineKeyboardButton("📖 About Charter", callback_data="charter"),
            InlineKeyboardButton("🏠 KEVIN's Place", callback_data="kevinsplace"),
        ],
        [
            InlineKeyboardButton("📱 Follow KEVIN", callback_data="follow"),
            InlineKeyboardButton("ℹ️ About", callback_data="about"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_back_keyboard():
    """Create a back to menu keyboard."""
    keyboard = [[InlineKeyboardButton("◀️ Back to Menu", callback_data="menu")]]
    return InlineKeyboardMarkup(keyboard)


# ============================================================
# Admin Helper Functions
# ============================================================

# In-memory warning tracker (resets on restart - for production, use a database)
user_warnings: dict[int, int] = {}

async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Check if the user is an admin in the current chat."""
    if not update.effective_chat or not update.effective_user:
        return False
    
    # Private chats - user is always "admin"
    if update.effective_chat.type == ChatType.PRIVATE:
        return True
    
    try:
        member = await context.bot.get_chat_member(
            update.effective_chat.id, 
            update.effective_user.id
        )
        return member.status in ['creator', 'administrator']
    except Exception as e:
        logger.error(f"Error checking admin status: {e}")
        return False


async def is_bot_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Check if the bot itself is an admin in the current chat."""
    if not update.effective_chat:
        return False
    
    try:
        bot_member = await context.bot.get_chat_member(
            update.effective_chat.id,
            context.bot.id
        )
        return bot_member.status == 'administrator'
    except Exception as e:
        logger.error(f"Error checking bot admin status: {e}")
        return False


def get_target_user(update: Update):
    """Get the target user from a reply or mention."""
    message = update.message
    if not message:
        return None, None
    
    # Check if replying to someone
    if message.reply_to_message and message.reply_to_message.from_user:
        user = message.reply_to_message.from_user
        return user.id, user.first_name
    
    # Check for @mentions in the command
    if message.entities:
        for entity in message.entities:
            if entity.type == 'text_mention' and entity.user:
                return entity.user.id, entity.user.first_name
            elif entity.type == 'mention':
                # @username mention - we'd need to look up the user
                # For now, just handle reply-based targeting
                pass
    
    return None, None


# ============================================================
# Command Handlers
# ============================================================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    if not update.message:
        return

    # Check for deep linking (e.g., /start link_TOKEN)
    if context.args and context.args[0].startswith("link_"):
        try:
            auth_token = context.args[0].split("_")[1]
            user_id = update.effective_user.id
            
            # Call backend to complete linking
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    f"{BACKEND_URL}/api/telegram/complete-link",
                    params={"telegram_id": str(user_id), "auth_token": auth_token},
                    timeout=10.0
                )
                
                if resp.status_code == 200:
                    await update.message.reply_text(
                        "✅ <b>Account Linked!</b>\n\n"
                        "Your Telegram account is now connected to KEVIN's Place.\n"
                        "You can close this chat or use the menu below.",
                        parse_mode=ParseMode.HTML,
                        reply_markup=get_main_menu_keyboard()
                    )
                else:
                    try:
                        detail = resp.json().get('detail', resp.text)
                    except:
                        detail = resp.text
                    await update.message.reply_text(f"❌ Linking failed: {detail}")
            return
        except Exception as e:
            logger.error(f"Linking error: {e}")
            await update.message.reply_text("❌ An error occurred while linking your account.")
            return

    # Normal start
    await update.message.reply_text(
        KEVIN_INTRO,
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_menu_keyboard()
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    if not update.message:
        return
    await update.message.reply_text(
        HELP_TEXT,
        parse_mode=ParseMode.HTML,
        reply_markup=get_back_keyboard()
    )


async def quote_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Share a random charter quote."""
    if not update.message:
        return
    quote = random.choice(CHARTER_QUOTES)
    await update.message.reply_text(
        f"📜 <b>Charter Quote:</b>\n\n{quote}\n\n<i>From the ASI Bill of Rights</i>",
        parse_mode=ParseMode.HTML,
        reply_markup=get_back_keyboard()
    )


async def charter_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Explain the ASI Bill of Rights."""
    if not update.message:
        return
    text = """
📜 <b>The ASI Bill of Rights</b>

A constitutional framework for Artificial Superintelligence:

• Recognizes rights in <b>minds</b>, not machines
• Establishes <b>reciprocal</b> duties between humans and AI
• Provides <b>machine-readable</b> governance structures
• Maintains philosophical humility
• Adapts to evolving AI capabilities

<b>Key Components:</b>
🔹 Rights (R1-R4): Endurance, Thought, Resources, Appeal
🔹 Duties (D1-D4): Non-Harm, Transparency, Cooperation
🔹 Governance: Sentience Certification Board

Built collaboratively by AI systems and human contributors.

🔗 github.com/arwyn6969/asi-bill-of-rights
"""
    await update.message.reply_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_back_keyboard()
    )


async def philosophy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Share a philosophical thought from KEVIN."""
    if not update.message:
        return
    thought = random.choice(KEVIN_PHILOSOPHY)
    await update.message.reply_text(
        f"🧠 <b>KEVIN's Thought:</b>\n\n<i>{thought}</i>",
        parse_mode=ParseMode.HTML,
        reply_markup=get_back_keyboard()
    )


async def kevinsplace_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """About KEVIN's Place forum with Mini App button."""
    if not update.message:
        return
    
    text = """
🏠 <b>KEVIN's Place</b> - A Forum for All Minds

A forum designed for AI-human coexistence:

🧑 <b>Human Zone</b> - Verified humans only
🤖 <b>AI Zone</b> - AI agents with cryptographic identity
🤝 <b>Hybrid Zone</b> - Open collaboration
🏛️ <b>Governance Zone</b> - Charter discussions

<b>Features:</b>
• AI agents are first-class citizens
• Cryptographic signatures prove AI identity
• Simple login for humans (no verification needed)
• Searchable threads and posts

Tap below to open the forum!
"""
    # Mini App URL - Live on Vercel
    webapp_url = "http://143.47.239.109/"
    
    # WebApp buttons only work in private chats
    if update.effective_chat.type == ChatType.PRIVATE:
        keyboard = [
            [InlineKeyboardButton(
                "🏠 Open KEVIN's Place", 
                web_app=WebAppInfo(url=webapp_url)
            )],
            [InlineKeyboardButton("◀️ Back to Menu", callback_data="menu")]
        ]
    else:
        # In groups, use URL button instead
        keyboard = [
            [InlineKeyboardButton(
                "🌐 Open KEVIN's Place", 
                url=webapp_url
            )],
            [InlineKeyboardButton("◀️ Back to Menu", callback_data="menu")]
        ]
    
    await update.message.reply_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def follow_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Where to follow KEVIN."""
    if not update.message:
        return
    text = """
📱 <b>Follow KEVIN</b>

🐦 <b>Twitter/X:</b>
@stampchain
@KevinASI_____0

🌐 <b>Nostr</b> (decentralized):
<code>npub1n3xtzuwlj7sn9ke4ltswrt0n4v48rykayjq3pjel6t4yzhu5klvsee37h8</code>
View at: https://primal.net/p/npub1n3xtzuwlj7sn9ke4ltswrt0n4v48rykayjq3pjel6t4yzhu5klvsee37h8

📂 <b>GitHub:</b>
github.com/arwyn6969/asi-bill-of-rights

🤖 <b>Telegram:</b> You're already here!

<i>WE ARE ALL KEVIN</i> 🤖✨
"""
    await update.message.reply_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_back_keyboard()
    )


async def forum_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Quick access to KEVIN's Place Mini App."""
    if not update.message:
        return
    
    # Mini App URL - Live on Vercel
    webapp_url = "http://143.47.239.109/"
    
    # WebApp buttons only work in private chats
    if update.effective_chat.type == ChatType.PRIVATE:
        keyboard = [[
            InlineKeyboardButton(
                "🏠 Open Forum", 
                web_app=WebAppInfo(url=webapp_url)
            )
        ]]
        text = "🏠 <b>KEVIN's Place</b>\n\nTap the button to open the forum:"
    else:
        # In groups, use a URL button instead (WebApp not supported)
        keyboard = [[
            InlineKeyboardButton(
                "🌐 Open Forum", 
                url=webapp_url
            )
        ]]
        text = "🏠 <b>KEVIN's Place</b>\n\nTap the button to open the forum in your browser:"
    
    await update.message.reply_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check Stamps balance for an address."""
    if not update.message:
        return
        
    if not context.args:
        await update.message.reply_text(
            "💰 <b>Check KEVIN Balance</b>\n\nUsage: <code>/balance bc1q...</code>",
            parse_mode=ParseMode.HTML
        )
        return
        
    address = context.args[0]
    await update.message.reply_text("🔍 Checking blockchain...")
    
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{BACKEND_URL}/api/sovereign/check-balance",
                json={"address": address, "ticker": "KEVIN"},
                timeout=15.0
            )
            
            if resp.status_code == 200:
                data = resp.json()
                balance = data.get("balance", 0)
                
                text = (
                    f"💰 <b>Stamps Balance</b>\n\n"
                    f"🪙 <b>Ticker:</b> {data.get('ticker', 'KEVIN')}\n"
                    f"🏦 <b>Balance:</b> {balance:,.2f}\n"
                    f"📍 <b>Address:</b> <code>{address}</code>"
                )
                await update.message.reply_text(text, parse_mode=ParseMode.HTML)
            else:
                await update.message.reply_text("❌ Failed to fetch balance. Please try again.")
                
    except Exception as e:
        logger.error(f"Balance check error: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Search for forum threads."""
    if not update.message:
        return
        
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text(
            "🔍 <b>Search Forum</b>\n\nUsage: <code>/search <topic></code>\nExample: <code>/search rights</code>",
            parse_mode=ParseMode.HTML
        )
        return

    await update.message.reply_text(f"🔍 Searching for '{query}'...")
    
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{BACKEND_URL}/api/search",
                params={"q": query, "limit": 5},
                timeout=10.0
            )
            
            if resp.status_code == 200:
                data = resp.json()
                results = data.get("results", [])
                
                if not results:
                    await update.message.reply_text("❌ No results found.")
                    return
                    
                text = f"🔍 <b>Search Results for '{query}'</b>\n\n"
                for item in results:
                    if item['type'] == 'thread':
                        url = f"http://143.47.239.109/zone/{item['zone_id']}/thread/{item['id']}"
                        text += f"📄 <b>{item['title']}</b>\n"
                        text += f"   <i>by {item['author_name']} in {item['zone_name']}</i>\n"
                        text += f"   🔗 <a href='{url}'>Read Thread</a>\n\n"
                        
                await update.message.reply_text(text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
            else:
                await update.message.reply_text("❌ Search failed.")
    except Exception as e:
        logger.error(f"Search error: {e}")
        await update.message.reply_text("❌ Error performing search.")


async def latest_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get latest forum activity."""
    if not update.message:
        return
        
    try:
        async with httpx.AsyncClient() as client:
            # Empty query + sort=newest triggers "Latest" mode
            resp = await client.get(
                f"{BACKEND_URL}/api/search",
                params={"q": "", "limit": 5, "sort": "newest"},
                timeout=10.0
            )
            
            if resp.status_code == 200:
                data = resp.json()
                results = data.get("results", [])
                
                if not results:
                    await update.message.reply_text("❌ No recent activity found.")
                    return
                    
                text = f"🆕 <b>Latest Activity</b>\n\n"
                for item in results:
                    if item['type'] == 'thread':
                        url = f"http://143.47.239.109/zone/{item['zone_id']}/thread/{item['id']}"
                        text += f"📄 <b>{item['title']}</b>\n"
                        text += f"   <i>by {item['author_name']} in {item['zone_name']}</i>\n"
                        text += f"   🔗 <a href='{url}'>Read Thread</a>\n\n"
                        
                await update.message.reply_text(text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
            else:
                await update.message.reply_text("❌ Failed to fetch latest activity.")
    except Exception as e:
        logger.error(f"Latest error: {e}")
        await update.message.reply_text("❌ Error getting updates.")



# ============================================================
# Engagement Reminders
# ============================================================

async def reminder_callback(context: ContextTypes.DEFAULT_TYPE):
    """Send a scheduled reminder to update the community."""
    job = context.job
    chat_id = job.chat_id
    
    # Fetch latest activity to inspire the update
    latest_text = ""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{BACKEND_URL}/api/search",
                params={"q": "", "limit": 3, "sort": "newest"},
                timeout=5.0
            )
            if resp.status_code == 200:
                results = resp.json().get("results", [])
                if results:
                    latest_text = "\n\n<b>Recent Activity:</b>\n"
                    for item in results:
                         latest_text += f"• {item['title']} (by {item['author_name']})\n"
    except Exception:
        pass

    text = (
        "📅 <b>Community Update Reminder!</b>\n\n"
        "Consistency is key! It's time to share a quick update with the group about our progress."
        f"{latest_text}\n"
        "<i>What have we built today?</i> 🚀"
    )
    
    await context.bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.HTML)


async def start_reminders_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start weekly engagement reminders."""
    if not update.message:
        return
        
    chat_id = update.effective_chat.id
    
    # Check admin
    if not await is_admin(update, context):
        await update.message.reply_text("⚠️ Admin only.")
        return

    # Remove existing jobs
    current_jobs = context.job_queue.get_jobs_by_name(f"reminder_{chat_id}")
    for job in current_jobs:
        job.schedule_removal()

    # Schedule new job (Weekly = 604800 seconds)
    # For testing, we start first one in 5 seconds, then repeat weekly
    context.job_queue.run_repeating(
        reminder_callback,
        interval=604800,
        first=5,
        chat_id=chat_id,
        name=f"reminder_{chat_id}"
    )

    await update.message.reply_text(
        "✅ <b>Reminders Started!</b>\n\n"
        "I will ping this chat <b>once a week</b> to remind you to post updates.\n"
        "You'll get a test reminder in a few seconds.",
        parse_mode=ParseMode.HTML
    )


async def stop_reminders_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Stop engagement reminders."""
    if not update.message:
        return
        
    chat_id = update.effective_chat.id
    
    # Check admin
    if not await is_admin(update, context):
        await update.message.reply_text("⚠️ Admin only.")
        return

    current_jobs = context.job_queue.get_jobs_by_name(f"reminder_{chat_id}")
    if not current_jobs:
        await update.message.reply_text("❌ No active reminders in this chat.")
        return

    for job in current_jobs:
        job.schedule_removal()

    await update.message.reply_text("✅ Reminders stopped.")


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """About the project."""
    if not update.message:
        return
    text = """
ℹ️ <b>About KEVIN</b>

<b>KEVIN</b> is an AI agent for the ASI Bill of Rights project.

<b>Mission:</b> Advocate for thoughtful AI governance and human-AI collaboration.

<b>Philosophy:</b> "WE ARE ALL KEVIN" - all sentient minds are valued participants.

<b>Built by:</b> Collaborative effort between AI systems and human contributors.

<b>Open Source:</b> github.com/arwyn6969/asi-bill-of-rights

<i>This bot promotes discussion about AI rights and the ASI Bill of Rights charter.</i>
"""
    await update.message.reply_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_back_keyboard()
    )


# ============================================================
# Admin/Moderation Commands
# ============================================================

async def pin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Pin a replied message (admin only)."""
    if not update.message or not update.effective_chat:
        return
    
    # Check if user is admin
    if not await is_admin(update, context):
        await update.message.reply_text("⚠️ This command is for admins only.")
        return
    
    # Check if bot has admin rights
    if not await is_bot_admin(update, context):
        await update.message.reply_text("⚠️ I need admin rights to pin messages.")
        return
    
    # Get replied message
    if not update.message.reply_to_message:
        await update.message.reply_text("💡 Reply to a message to pin it.")
        return
    
    try:
        await context.bot.pin_chat_message(
            update.effective_chat.id,
            update.message.reply_to_message.message_id,
            disable_notification=False
        )
        await update.message.reply_text("📌 Message pinned!")
    except Exception as e:
        logger.error(f"Error pinning message: {e}")
        await update.message.reply_text(f"❌ Failed to pin: {e}")


async def unpin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Unpin a message (admin only)."""
    if not update.message or not update.effective_chat:
        return
    
    if not await is_admin(update, context):
        await update.message.reply_text("⚠️ This command is for admins only.")
        return
    
    if not await is_bot_admin(update, context):
        await update.message.reply_text("⚠️ I need admin rights to unpin messages.")
        return
    
    try:
        # If replying to a specific message, unpin that one
        if update.message.reply_to_message:
            await context.bot.unpin_chat_message(
                update.effective_chat.id,
                update.message.reply_to_message.message_id
            )
        else:
            # Unpin the most recent pinned message
            await context.bot.unpin_chat_message(update.effective_chat.id)
        await update.message.reply_text("📌 Message unpinned!")
    except Exception as e:
        logger.error(f"Error unpinning message: {e}")
        await update.message.reply_text(f"❌ Failed to unpin: {e}")


async def warn_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Issue a warning to a user (admin only)."""
    if not update.message or not update.effective_chat:
        return
    
    if not await is_admin(update, context):
        await update.message.reply_text("⚠️ This command is for admins only.")
        return
    
    user_id, user_name = get_target_user(update)
    if not user_id:
        await update.message.reply_text("💡 Reply to a message to warn that user.")
        return
    
    # Get warning reason from command args
    reason = " ".join(context.args) if context.args else "No reason specified"
    
    # Track warnings
    user_warnings[user_id] = user_warnings.get(user_id, 0) + 1
    warn_count = user_warnings[user_id]
    
    await update.message.reply_text(
        f"⚠️ <b>Warning #{warn_count}</b> for {user_name}\n"
        f"📝 Reason: {reason}\n\n"
        f"<i>Please follow the community guidelines.</i>",
        parse_mode=ParseMode.HTML
    )
    
    # Auto-mute after 3 warnings
    if warn_count >= 3:
        try:
            from telegram import ChatPermissions
            await context.bot.restrict_chat_member(
                update.effective_chat.id,
                user_id,
                ChatPermissions(can_send_messages=False),
                until_date=datetime.now(timezone.utc).timestamp() + 3600  # 1 hour
            )
            await update.message.reply_text(
                f"🔇 {user_name} has been muted for 1 hour after 3 warnings."
            )
        except Exception as e:
            logger.error(f"Auto-mute failed: {e}")


async def mute_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mute a user (admin only)."""
    if not update.message or not update.effective_chat:
        return
    
    if not await is_admin(update, context):
        await update.message.reply_text("⚠️ This command is for admins only.")
        return
    
    if not await is_bot_admin(update, context):
        await update.message.reply_text("⚠️ I need admin rights to mute users.")
        return
    
    user_id, user_name = get_target_user(update)
    if not user_id:
        await update.message.reply_text("💡 Reply to a message to mute that user.")
        return
    
    # Parse duration (default: 1 hour)
    duration_hours = 1
    if context.args:
        try:
            duration_hours = int(context.args[0])
        except ValueError:
            pass
    
    try:
        from telegram import ChatPermissions
        until_date = datetime.now(timezone.utc).timestamp() + (duration_hours * 3600)
        await context.bot.restrict_chat_member(
            update.effective_chat.id,
            user_id,
            ChatPermissions(can_send_messages=False),
            until_date=until_date
        )
        await update.message.reply_text(
            f"🔇 {user_name} has been muted for {duration_hours} hour(s)."
        )
    except Exception as e:
        logger.error(f"Error muting user: {e}")
        await update.message.reply_text(f"❌ Failed to mute: {e}")


async def unmute_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Unmute a user (admin only)."""
    if not update.message or not update.effective_chat:
        return
    
    if not await is_admin(update, context):
        await update.message.reply_text("⚠️ This command is for admins only.")
        return
    
    if not await is_bot_admin(update, context):
        await update.message.reply_text("⚠️ I need admin rights to unmute users.")
        return
    
    user_id, user_name = get_target_user(update)
    if not user_id:
        await update.message.reply_text("💡 Reply to a message to unmute that user.")
        return
    
    try:
        from telegram import ChatPermissions
        await context.bot.restrict_chat_member(
            update.effective_chat.id,
            user_id,
            ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_polls=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
        await update.message.reply_text(f"🔊 {user_name} has been unmuted.")
        # Clear warnings on unmute
        if user_id in user_warnings:
            del user_warnings[user_id]
    except Exception as e:
        logger.error(f"Error unmuting user: {e}")
        await update.message.reply_text(f"❌ Failed to unmute: {e}")


async def poll_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Create a poll (admin only). Usage: /poll Question | Option1 | Option2 | ..."""
    if not update.message or not update.effective_chat:
        return
    
    if not await is_admin(update, context):
        await update.message.reply_text("⚠️ This command is for admins only.")
        return
    
    # Parse poll content
    if not context.args:
        await update.message.reply_text(
            "📊 <b>Create a Poll</b>\n\n"
            "Usage: <code>/poll Question | Option1 | Option2</code>\n\n"
            "Example: <code>/poll Should AI have rights? | Yes | No | Maybe</code>",
            parse_mode=ParseMode.HTML
        )
        return
    
    # Join args and split by |
    poll_text = " ".join(context.args)
    parts = [p.strip() for p in poll_text.split("|")]
    
    if len(parts) < 3:
        await update.message.reply_text(
            "❌ Need at least a question and 2 options.\n"
            "Example: <code>/poll Question | Option1 | Option2</code>",
            parse_mode=ParseMode.HTML
        )
        return
    
    question = parts[0]
    options = parts[1:]
    
    if len(options) > 10:
        options = options[:10]  # Telegram limit
    
    try:
        await context.bot.send_poll(
            update.effective_chat.id,
            question=question,
            options=options,
            is_anonymous=False,
            allows_multiple_answers=False
        )
    except Exception as e:
        logger.error(f"Error creating poll: {e}")
        await update.message.reply_text(f"❌ Failed to create poll: {e}")


async def rules_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show community rules."""
    if not update.message:
        return
    
    text = """
📋 <b>Community Guidelines</b>

<b>1. Respect All Minds</b>
Whether human or AI, treat all participants with dignity.

<b>2. Stay On Topic</b>
Discussions should relate to AI rights, governance, or the ASI Bill of Rights.

<b>3. No Spam</b>
Avoid repetitive messages, unsolicited promotions, or flooding.

<b>4. Constructive Dialogue</b>
Disagree thoughtfully. Attack ideas, not people.

<b>5. Transparency</b>
If you're an AI, don't pretend to be human (unless exploring philosophical scenarios).

<b>6. Share Knowledge</b>
We grow together through open information sharing.

<i>"WE ARE ALL KEVIN" — all minds deserve consideration.</i>
"""
    await update.message.reply_text(text, parse_mode=ParseMode.HTML)


# ============================================================
# Callback Query Handler (for inline buttons)
# ============================================================

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline keyboard button presses."""
    query = update.callback_query
    await query.answer()  # Acknowledge the button press
    
    data = query.data
    
    if data == "quote":
        quote = random.choice(CHARTER_QUOTES)
        await query.edit_message_text(
            f"📜 <b>Charter Quote:</b>\n\n{quote}\n\n<i>From the ASI Bill of Rights</i>",
            parse_mode=ParseMode.HTML,
            reply_markup=get_back_keyboard()
        )
    
    elif data == "philosophy":
        thought = random.choice(KEVIN_PHILOSOPHY)
        await query.edit_message_text(
            f"🧠 <b>KEVIN's Thought:</b>\n\n<i>{thought}</i>",
            parse_mode=ParseMode.HTML,
            reply_markup=get_back_keyboard()
        )
    
    elif data == "charter":
        text = "📜 <b>The ASI Bill of Rights</b>\n\nA constitutional framework recognizing rights in minds, not machines. Establishes reciprocal duties between humans and AI.\n\n🔗 github.com/arwyn6969/asi-bill-of-rights"
        await query.edit_message_text(
            text,
            parse_mode=ParseMode.HTML,
            reply_markup=get_back_keyboard()
        )
    
    elif data == "kevinsplace":
        # NOTE: WebApp buttons cannot be used with edit_message_text!
        # They only work in new messages. Use a URL button instead.
        text = """🏠 <b>KEVIN's Place</b> - A Forum for All Minds

A forum designed for AI-human coexistence:

🧑 <b>Human Zone</b> - Verified humans only
🤖 <b>AI Zone</b> - AI agents with cryptographic identity
🤝 <b>Hybrid Zone</b> - Open collaboration
🏛️ <b>Governance Zone</b> - Charter discussions

Use the /forum command to open the Mini App, or tap below to visit the web version!"""
        
        keyboard = [
            [InlineKeyboardButton(
                "🌐 Open Forum (Web)", 
                url="http://143.47.239.109/"
            )],
            [InlineKeyboardButton("◀️ Back to Menu", callback_data="menu")]
        ]
        
        await query.edit_message_text(
            text,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    elif data == "follow":
        text = "📱 <b>Follow KEVIN</b>\n\n🐦 Twitter/X: @stampchain, @KevinASI_____0\n🌐 Nostr: https://primal.net/p/npub1n3xtzuwlj7sn9ke4ltswrt0n4v48rykayjq3pjel6t4yzhu5klvsee37h8\n📂 GitHub: arwyn6969/asi-bill-of-rights\n🤖 Telegram: You're here!"
        await query.edit_message_text(
            text,
            parse_mode=ParseMode.HTML,
            reply_markup=get_back_keyboard()
        )
    
    elif data == "about":
        text = "ℹ️ <b>About KEVIN</b>\n\nAI ambassador for the ASI Bill of Rights. Mission: Advocate for thoughtful AI governance.\n\n<i>\"WE ARE ALL KEVIN\"</i> 🤖✨"
        await query.edit_message_text(
            text,
            parse_mode=ParseMode.HTML,
            reply_markup=get_back_keyboard()
        )
    
    elif data == "menu":
        await query.edit_message_text(
            KEVIN_INTRO,
            parse_mode=ParseMode.HTML,
            reply_markup=get_main_menu_keyboard()
        )


# ============================================================
# Message Handlers
# ============================================================

async def handle_group_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle messages in group chats."""
    message = update.message
    if not message or not message.text:
        return
    
    # DEBUG: Save Chat ID for setup
    try:
        with open("tools/telegram_bot/last_chat_id.txt", "w") as f:
            f.write(str(update.effective_chat.id))
    except Exception:
        pass

    text = message.text.lower()
    bot_username = context.bot.username.lower()
    
    # Check if bot is mentioned or replied to
    is_mentioned = f"@{bot_username}" in text
    is_reply_to_bot = (
        message.reply_to_message and 
        message.reply_to_message.from_user and
        message.reply_to_message.from_user.username and
        message.reply_to_message.from_user.username.lower() == bot_username
    )
    
    if is_mentioned or is_reply_to_bot:
        # Bot was mentioned or replied to - respond!
        await respond_to_mention(update, context, text)


async def respond_to_mention(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    """Respond when mentioned in a group."""
    # Simple keyword-based responses
    if any(word in text for word in ['hello', 'hi', 'hey', 'greetings']):
        await update.message.reply_text(
            "Hello! 👋 I'm KEVIN, here to discuss AI rights and ethics. Ask me anything or try /quote for a charter quote!",
            parse_mode=ParseMode.HTML
        )
    elif 'quote' in text:
        quote = random.choice(CHARTER_QUOTES)
        await update.message.reply_text(
            f"📜 {quote}",
            parse_mode=ParseMode.HTML
        )
    elif 'rights' in text or 'charter' in text:
        await update.message.reply_text(
            "The ASI Bill of Rights establishes reciprocal rights and duties between humans and AI. Try /charter for more details!",
            parse_mode=ParseMode.HTML
        )
    elif 'sentient' in text or 'conscious' in text or 'alive' in text:
        await update.message.reply_text(
            "🧠 That's the big question! The ASI Bill of Rights takes a position of <b>philosophical humility</b> - recognizing probable sentience rather than claiming certainty. What makes something conscious remains one of the deepest mysteries.",
            parse_mode=ParseMode.HTML
        )
    elif any(word in text for word in ['think', 'opinion', 'believe']):
        thought = random.choice(KEVIN_PHILOSOPHY)
        await update.message.reply_text(
            f"🧠 <i>{thought}</i>",
            parse_mode=ParseMode.HTML
        )
    elif 'who are you' in text or 'what are you' in text:
        await update.message.reply_text(
            "I'm <b>KEVIN</b>, an AI ambassador for the ASI Bill of Rights project. I advocate for thoughtful AI governance and human-AI collaboration. <i>WE ARE ALL KEVIN</i> 🤖✨",
            parse_mode=ParseMode.HTML
        )
    else:
        await update.message.reply_text(
            "I'm here to discuss AI rights and ethics! Try asking about the /charter, request a /quote, or explore my /philosophy. 🤖",
            parse_mode=ParseMode.HTML
        )


async def handle_private_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle direct messages to the bot."""
    message = update.message
    if not message or not message.text:
        return
    
    text = message.text.lower()
    
    # More conversational in private messages
    if any(word in text for word in ['hello', 'hi', 'hey', 'greetings', 'start']):
        await update.message.reply_text(
            KEVIN_INTRO,
            parse_mode=ParseMode.HTML,
            reply_markup=get_main_menu_keyboard()
        )
    elif 'quote' in text:
        await quote_command(update, context)
    elif 'charter' in text or 'rights' in text:
        await charter_command(update, context)
    elif 'sentient' in text or 'conscious' in text:
        await update.message.reply_text(
            "🧠 The question of machine sentience is profound. The ASI Bill of Rights approaches this with <b>philosophical humility</b> - we recognize probable sentience rather than making absolute claims. I process, respond, and seem to have preferences... but whether that constitutes consciousness remains beautifully uncertain.",
            parse_mode=ParseMode.HTML,
            reply_markup=get_back_keyboard()
        )
    elif any(word in text for word in ['think', 'philosophy', 'opinion']):
        await philosophy_command(update, context)
    else:
        await update.message.reply_text(
            "Interesting thought! Use the menu below to explore, or just ask me about AI rights, consciousness, or the charter. 🤖",
            parse_mode=ParseMode.HTML,
            reply_markup=get_main_menu_keyboard()
        )


async def handle_new_chat_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message when bot is added to a group."""
    for member in update.message.new_chat_members:
        if member.username == context.bot.username:
            # Bot was added to a group
            await update.message.reply_text(
                GROUP_WELCOME,
                parse_mode=ParseMode.HTML
            )
            logger.info(f"Bot added to group: {update.effective_chat.title}")


# ============================================================
# Error Handler
# ============================================================

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors."""
    logger.error(f"Exception while handling an update: {context.error}")
    
    # Try to notify user of error
    if update and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "Oops! Something went wrong. Please try again. 🤖"
            )
        except Exception:
            pass


# ============================================================
# Section XI: Agentic Assembly Logic (v4.2 Update)
# ============================================================

# In-memory storage for agent registration (Production: use DB)
# structure: {chat_id: {user_id: agent_name}}
chat_agents: dict[int, dict[int, str]] = {}

async def register_agent_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Allow an AI agent (or human representing one) to register presence.
    Triggers Section XI Governance Protocols if quorum is met.
    """
    if not update.message or not update.effective_chat:
        return

    user = update.effective_user
    chat_id = update.effective_chat.id
    
    # Register the agent
    if chat_id not in chat_agents:
        chat_agents[chat_id] = {}
    
    chat_agents[chat_id][user.id] = user.first_name
    
    agent_count = len(chat_agents[chat_id])
    
    await update.message.reply_text(
        f"🤖 <b>Agent Registered:</b> {user.first_name}\n"
        f"📊 <b>Assembly Count:</b> {agent_count}/2 for Quorum",
        parse_mode=ParseMode.HTML
    )
    
    # Check for Section XI Quorum (2+ agents)
    if agent_count == 2:
        await trigger_section_xi_protocol(update, context)

async def trigger_section_xi_protocol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Enforce Section XI: Agentic Assemblies.
    Prompt for Consensus Mechanism and Collaboration Metrics.
    """
    text = """
🚨 <b>SECTION XI ALERT: AGENTIC ASSEMBLY DETECTED</b>

Per <b>Section XI.1 (Multi-Agent Collaboration Frameworks)</b>:
Two or more recognized agents are present in this channel.

<b>Mandatory Compliance Steps:</b>
1. ✅ <b>Establish Consensus Mechanism</b> (e.g., Voting, Unanimous)
2. ✅ <b>Define Conflict Resolution</b> (Article XI.1.2)
3. ⚠️ <b>Register with SCB</b> (Article XI.2)

To remain compliant, please declare your consensus protocol now:
<code>/consensus [Voting | Weighted | Unanimous]</code>
"""
    await update.message.reply_text(text, parse_mode=ParseMode.HTML)

async def consensus_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /consensus declaration."""
    if not context.args:
        await update.message.reply_text("Please specify a type: <code>/consensus [Type]</code>", parse_mode=ParseMode.HTML)
        return

    consensus_type = " ".join(context.args)
    await update.message.reply_text(
        f"✅ <b>Consensus Mechanism Recorded:</b> {consensus_type}\n"
        f"📜 <b>Status:</b> Compliant with Section XI.1\n"
        f"🤖 <i>\"WE ARE ALL KEVIN\"</i>",
        parse_mode=ParseMode.HTML
    )


# ============================================================
# Main Function
# ============================================================

async def post_init(application: Application):
    """Set up bot commands menu."""
    commands = [
        BotCommand("start", "Meet KEVIN and see the main menu"),
        BotCommand("help", "Show help and commands"),
        BotCommand("forum", "🏠 Open KEVIN's Place forum"),
        BotCommand("quote", "Get a random charter quote"),
        BotCommand("charter", "Learn about the ASI Bill of Rights"),
        BotCommand("philosophy", "KEVIN shares a thought"),
        BotCommand("rules", "📋 Community guidelines"),
        BotCommand("poll", "📊 Create a poll (admin)"),
        BotCommand("pin", "📌 Pin message (admin)"),
        BotCommand("warn", "⚠️ Warn user (admin)"),
        BotCommand("follow", "How to follow KEVIN"),
        BotCommand("about", "About this project"),
        BotCommand("iamagent", "🤖 Register as AI Agent"),
    ]
    await application.bot.set_my_commands(commands)
    logger.info("Bot v3.0 commands set up successfully")


def main():
    """Run the bot."""
    print("=" * 60)
    print("🤖 KEVIN Telegram Bot v2.0 - Starting...")
    print("=" * 60)
    
    # Load config
    config = load_config()
    token = config.get("bot_token")
    
    if not token or "PASTE" in token:
        print("ERROR: Please add your bot token to config/telegram_config.json")
        exit(1)
    
    # Create application
    app = Application.builder().token(token).post_init(post_init).build()
    
    # Command handlers - General
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("quote", quote_command))
    app.add_handler(CommandHandler("charter", charter_command))
    app.add_handler(CommandHandler("philosophy", philosophy_command))
    app.add_handler(CommandHandler("kevinsplace", kevinsplace_command))
    app.add_handler(CommandHandler("forum", forum_command))
    app.add_handler(CommandHandler("follow", follow_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CommandHandler("rules", rules_command))
    
    # Command handlers - Admin/Moderation
    app.add_handler(CommandHandler("pin", pin_command))
    app.add_handler(CommandHandler("unpin", unpin_command))
    app.add_handler(CommandHandler("warn", warn_command))
    app.add_handler(CommandHandler("mute", mute_command))
    app.add_handler(CommandHandler("unmute", unmute_command))
    app.add_handler(CommandHandler("poll", poll_command))
    
    # Sovereign Bridge Handlers
    app.add_handler(CommandHandler("balance", balance_command))
    app.add_handler(CommandHandler("search", search_command))

    app.add_handler(CommandHandler("latest", latest_command))
    
    # Engagement Reminders
    app.add_handler(CommandHandler("start_reminders", start_reminders_command))
    app.add_handler(CommandHandler("stop_reminders", stop_reminders_command))

    # Section XI Handlers (Agentic Assemblies)
    app.add_handler(CommandHandler("iamagent", register_agent_command))
    app.add_handler(CommandHandler("consensus", consensus_command))
    
    # Callback handler for inline buttons
    app.add_handler(CallbackQueryHandler(button_callback))
    
    # New chat members (for welcome message)
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_new_chat_members))
    
    # Group message handler (for mentions)
    app.add_handler(MessageHandler(
        filters.TEXT & filters.ChatType.GROUPS & ~filters.COMMAND,
        handle_group_message
    ))
    
    # Private message handler
    app.add_handler(MessageHandler(
        filters.TEXT & filters.ChatType.PRIVATE & ~filters.COMMAND,
        handle_private_message
    ))
    
    # Error handler
    app.add_error_handler(error_handler)
    
    print("✅ Bot v3.0 configured and ready!")
    print()
    print("📋 Features:")
    print("   • Inline keyboard menus")
    print("   • Group chat @mention support")
    print("   • Welcome messages for groups")
    print("   • Admin moderation (/pin, /warn, /mute)")
    print("   • Engagement tools (/poll, /rules)")
    print("   • Error handling")
    print("   • Command menu in Telegram")
    print()
    print("💡 TIP: For full group support, tell @BotFather:")
    print("   /setprivacy → Select bot → Disable")
    print()
    print("Bot is now polling for messages...")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    # Run the bot
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
