import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = "@helaltehhhelp"
CHANNEL_LINK = "https://t.me/helaltehhhelp"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 চ্যানেলে Join করুন", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✅ আমি Join করেছি", callback_data="check_join")]
    ]

    await update.message.reply_text(
        "👋 স্বাগতম!\n\n"
        "বট ব্যবহার করার আগে আমাদের Telegram চ্যানেলে Join করুন।\n"
        "Join করার পর নিচের **আমি Join করেছি** বাটনে চাপুন।",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        member = await context.bot.get_chat_member(
            chat_id=CHANNEL,
            user_id=query.from_user.id
        )

        if member.status in ["member", "administrator", "creator"]:
            await query.edit_message_text(
                "🎉 Join সফল হয়েছে!\n\n"
                "✅ এখন আপনি বট ব্যবহার করতে পারবেন।"
            )
        else:
            await query.answer(
                "❌ আগে চ্যানেলে Join করুন।",
                show_alert=True
            )

    except Exception:
        await query.answer(
            "❌ Join যাচাই করা যাচ্ছে না। একটু পরে আবার চেষ্টা করুন।",
            show_alert=True
        )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_join, pattern="^check_join$"))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
