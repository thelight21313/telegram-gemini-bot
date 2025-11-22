import asyncio
import aiohttp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
import sys

import requests
# === CONFIGURATION - REPLACE WITH YOUR KEYS ===
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"  # Get from @BotFather
api_key = "YOUR_GEMINI_API_KEY_HERE"  # Get from https://aistudio.google.com/app/apikey
# === END CONFIGURATION ===



async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE): # This function help command
    start_text = """ 
    GOD can help you, not me
    """ # Change start_text, this text will send to user, when he will use command /help
    await update.message.reply_text(start_text)
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE): # This function start command
    start_text = """
    hello, I'm Gemini in telegram. You can send me your quest and I give you response
    """ # Change start_text, this text will send to user, when he will use command /start
    await update.message.reply_text(start_text)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE): # This function for everythink users message, his message will send to Gemini and return response
    text = update.message.text
    hilo = text
    result = await send(prompt=hilo)

    await update.message.reply_text(result)
async def send(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={api_key}"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers = headers, json =data) as response:
            if response.status == 200:
                result = await response.json()
                joko = (result['candidates'][0]['content']['parts'][0]['text'])
                return joko
            else:
                error = "Try again please, maybe requests per minute very much"
                print(f"Error: {response.status}")
                return error




def main():
    # Check if keys are still placeholder values
    if "YOUR_" in BOT_TOKEN or "YOUR_" in api_key:
        print("""
    ⚠️  CONFIGURATION REQUIRED!

    Please replace in bot.py:
    - YOUR_TELEGRAM_BOT_TOKEN_HERE with your bot token from @BotFather
    - YOUR_GEMINI_API_KEY_HERE with your API key from https://aistudio.google.com/app/apikey

    Then run the bot again.
            """)
        return

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()



if __name__ == "__main__":
    main()