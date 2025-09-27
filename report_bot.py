from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
SUPPORT_GROUP_ID = int(os.getenv("SUPPORT_GROUP_ID"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 أهلاً بك!\nأرسل بلاغك (نص، رابط أو صورة)، وسيتم تحويله مباشرة إلى فريق الدعم الداخلي."
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text
    report = f"📢 بلاغ جديد\n👤 من: {user.first_name} (@{user.username or 'بدون اسم'})\n📝 المحتوى: {text}"
    await context.bot.send_message(chat_id=SUPPORT_GROUP_ID, text=report)
    await update.message.reply_text("✅ تم إرسال بلاغك إلى فريق الدعم.")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    caption = update.message.caption or "بدون وصف"
    photo = update.message.photo[-1].file_id
    await context.bot.send_photo(
        chat_id=SUPPORT_GROUP_ID,
        photo=photo,
        caption=f"📢 بلاغ جديد (صورة)\n👤 من: {user.first_name} (@{user.username or 'بدون اسم'})\n📝 الوصف: {caption}"
    )
    await update.message.reply_text("✅ تم إرسال بلاغك (صورة) إلى فريق الدعم.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.run_polling()

if __name__ == "__main__":
    main()
