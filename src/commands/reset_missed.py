from telegram import Update
from telegram.ext import ContextTypes
from databases.mysql.user_table import User
from utils import is_admin



async def reset_missed(update: Update, context: ContextTypes.DEFAULT_TYPE)-> None:
    """To reset the weekly missed in the testing time with the week achievement topic"""
    group_id = update.effective_chat.id
    user_id = update.effective_user.id        
    if await is_admin(update, context, user_id) :
        with User() as Ur  :
            Ur.weekly_missed_update(group_id)
    else:
        await update.message.reply_text("ليس لديك صلاحية")
    
    