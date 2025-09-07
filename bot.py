import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ===== إعدادات =====
TOKEN = "6433743426:AAHYO2pUCSBJJf9nKPeVS7ponZj_SvcA90M"
CHANNEL = "@qd3qd"   # القناة المطلوبة للاشتراك
ADMIN_ID = 5581457665      # الآيدي الخاص بك

# ===== Logs =====
logging.basicConfig(level=logging.INFO)

# ===== أوامر /start =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
✨ أهلاً بك في بوت الحماية ✨
━━━━━━━━━━━━━
✦ اختصاص البوت: حماية المجموعات  
✦ لتفعيل البوت اتبع التالي:  
━━━━━━━━━━━━━
1️⃣ أضف البوت إلى مجموعتك  
2️⃣ ارفعه "مشرف"  
3️⃣ أرسل كلمة { تفعيل } ليبدأ البوت بالعمل  
━━━━━━━━━━━━━
✦ معرف البوت: @iDiXbot
✦ المطور: @E2E12
"""
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("➕✅ أضفني لمجموعتك", url="https://t.me/iDiXbot?startgroup=true")]]
    )
    await update.message.reply_text(text, reply_markup=keyboard)


# ===== أمر التفعيل داخل المجموعات =====
async def activate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type in ["group", "supergroup"]:
        await update.message.reply_text(
            f"👍✅ تم تفعيل البوت بنجاح في المجموعة: {chat.title}"
        )
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📶😂 تم تفعيل البوت في مجموعة جديدة:\n\n• الاسم: {chat.title}\n• الآيدي: {chat.id}"
        )
    else:
        await update.message.reply_text("!❌ هذا الأمر يعمل فقط داخل المجموعات")


# ===== تحقق من الاشتراك =====
async def is_subscribed(user_id, context: ContextTypes.DEFAULT_TYPE):
    try:
        member = await context.bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


# ===== منع الرسائل لغير المشتركين =====
async def restrict_unsubscribed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id

    if await is_subscribed(user.id, context):
        await context.bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user.id,
            permissions=ChatPermissions(can_send_messages=True)
        )
        return

    try:
        await update.message.delete()
    except:
        pass

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("📢 مَـدار", url=f"https://t.me/{CHANNEL.strip('@')}")]]
    )
    text = f"""
• عذراً عزيزي {user.first_name} ⚠️
• لا يمكنك ارسال الرسائل هنا الا بعد الاشتراك في قناة المجموعة 👮‍♂
- قناة المجموعة | {CHANNEL}
• اشترك لكي تستطيع إرسال الرسائل ❤️‍🔥.
"""
    await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)


# ===== تشغيل البوت =====
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^(تفعيل)$"), activate))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, restrict_unsubscribed))

    app.run_polling()


if __name__ == "__main__":
    main()
