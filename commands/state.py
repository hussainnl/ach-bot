from telegram import Update
from telegram.ext import ContextTypes
from database.user_table import User 
import logging


async def state(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """To send the achievement score to the user"""
    user_id = update.effective_user.id
    user_name =  update.effective_user.username if  update.effective_user.username else  update.effective_user.full_name
    chat_id = update.effective_chat.id

    with User() as Ur:
        Ur.add_user(chat_id,user_id,user_name)
 
    with User() as Ur:
        user_scor = Ur.get_user_score(user_id, chat_id)

    massage = f"✨ نقاطك : {user_scor} نقطة ✨"
    await update.message.reply_text(massage)
