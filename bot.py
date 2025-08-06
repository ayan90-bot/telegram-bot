import logging
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)
from keep_alive import keep_alive

BOT_TOKEN = "8227539259:AAFFqyoMK9SBdGJIJP8K4-_chmcL4PW-RWc"  # <-- Apna bot token yahan daal
ADMIN_ID = 6324825537
UPI_IMAGE_PATH = "payment.jpg"  # ← yeh photo tumhare Replit/Render project me hona chahiye

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

user_list = set()

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_list.add(user.id)
    if user.id == ADMIN_ID:
        await update.message.reply_text("👋 Hello Admin! Use /cast or /reply.")
    else:
        await update.message.reply_text("Welcome! Send your 2-line message or use /premium.")

# handle text from user
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id != ADMIN_ID:
        await update.message.reply_text("📬 Your order is processing...")
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"New message from {user.id}:\n{update.message.text}"
        )

# handle photo from user
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    file = await update.message.photo[-1].get_file()
    await context.bot.send_photo(chat_id=ADMIN_ID, photo=file.file_id, caption=f"Photo from {user.id}")

# /premium command
async def premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("🚫 You are not authorized.")
        return
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open(UPI_IMAGE_PATH, "rb"),
        caption="🪙 Send payment and reply with screenshot to upgrade to Premium."
    )

# /cast broadcast message to all users
async def cast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("🚫 You are not authorized.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /cast Your message here")
        return

    msg = "📢 Broadcast:\n" + " ".join(context.args)
    count = 0
    for uid in user_list:
        try:
            await context.bot.send_message(chat_id=uid, text=msg)
            count += 1
        except:
            pass

    await update.message.reply_text(f"✅ Sent to {count} users.")

# MAIN
async def main():
    keep_alive()
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("premium", premium))
    app.add_handler(CommandHandler("cast", cast))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("✅ Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
    
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot chal raha hai!")

app = ApplicationBuilder().token("8227539259:AAFFqyoMK9SBdGJIJP8K4-_chmcL4PW-RWc").build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
