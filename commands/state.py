from telegram import Update
from telegram.ext import ContextTypes
from data_manager import Data_Manager as DB


import logging

# تقدر تحدد مستوى اللوج (INFO, DEBUG, ERROR...)
logging.basicConfig(level=logging.INFO)

async def state(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """To send the achievement score to the user"""
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    # log
    logging.info(f"user_id={user_id}, chat_id={chat_id}")
    DB().check_user_id(user_id, chat_id)
    user_scor = DB().state_count(user_id, chat_id)
    massage = f"✨ نقاطك : {user_scor} نقطة ✨"
    if user_scor is None:
        await update.message.reply_text("لم يتم تحديد المستخدم او المجموعة")
    else:
        await update.message.reply_text(massage)
