from telegram import Update
from telegram.ext import ContextTypes
from databases.mysql.group_table import Group
from utils import is_admin
async def study_monitoring_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    group_id = update.effective_chat.id
    user_id = update.effective_user.id
    current_thread_id = update.message.message_thread_id
    if await is_admin(update, context, user_id) :
        with Group() as Gp:
            Gp.update_study_topic_id(current_thread_id, group_id)
        await update.message.reply_text("تم اعداد مكان المراقبة")
    else:
        await update.message.reply_text("ليس لديك صلاحية")
async def weekly_monitoring_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    group_id = update.effective_chat.id
    user_id = update.effective_user.id
    current_thread_id = update.message.message_thread_id
    if await is_admin(update, context, user_id) :
        with Group() as Gp:
            Gp.update_weekly_topic_id(current_thread_id, group_id)
        await update.message.reply_text("تم اعداد مكان المراقبة")
    else:
        await update.message.reply_text("ليس لديك صلاحية")
       