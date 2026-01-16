from telegram import Update
from telegram.ext import ContextTypes
from data_manager import Bot_Setting as BS
from utils import is_admin
async def set_notification_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    current_thread_id = update.message.message_thread_id
    if await is_admin(update, context, user_id) :
        BS().add_notification_topic_id(current_thread_id, chat_id)
        await update.message.reply_text("تم اعداد الإشعارات")
    else:
        await update.message.reply_text("ليس لديك صلاحية")
    