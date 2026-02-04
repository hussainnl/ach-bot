from telegram import Update
from telegram.ext import ContextTypes
from databases.mysql.user_table import User
from databases.mysql.group_table import Group
from utils import is_admin



async def restart_missed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group_id = update.effective_chat.id
    user_id = update.effective_user.id
    with Group() as Gp :
        notification_topic_id = Gp.get_notification_topic_id(group_id)
    if await is_admin(update, context, user_id) :
        with User() as Ur :
            Ur.weekly_missed_update()
        await context.bot.send_message(group_id, text="تم عمل التشيك الأسبوعي ✅",message_thread_id=notification_topic_id)
    else:
        await update.message.reply_text("ليس لديك صلاحية")
    
    