import os
import logging
from fastapi import FastAPI, Request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# ===== إعدادات =====
TOKEN = os.getenv("6433743426:AAHYO2pUCSBJJf9nKPeVS7ponZj_SvcA90M")  # حط التوكن داخل Secrets في Render
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # رابط الخدمة من Render (مثل https://yourapp.onrender.com)

logging.basicConfig(level=logging.INFO)

# FastAPI App
app = FastAPI()

# Telegram Bot Application
application = Application.builder().token(TOKEN).build()


# ===== /start command =====
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
✦ المطور:💁 @E2E12
"""
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("➕ أضفني لمجموعتك", url="https://t.me/iDiXbot?startgroup=true")]]
    )
    await update.message.reply_text(text, reply_markup=keyboard)


# أضف الأمر للبوت
application.add_handler(CommandHandler("start", start))


# ===== Webhook =====
@app.on_event("startup")
async def startup_event():
    # إعداد Webhook عند تشغيل الخدمة
    await application.bot.set_webhook(f"{WEBHOOK_URL}/webhook")


@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return {"ok": True}
