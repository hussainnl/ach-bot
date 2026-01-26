from telegram import Update
from telegram.ext import ContextTypes
from utils import is_admin
from database.group_table import Group 



async def set_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    group_name = update.effective_chat.title
    user_id = update.effective_user.id
    if await is_admin(update, context, user_id) :
        with Group() as Gp:
            Gp.add_new_group(chat_id,group_name)
        await update.message.reply_text("تم اعداد المجموعة")
    else:
        await update.message.reply_text("ليس لديك صلاحية")
    