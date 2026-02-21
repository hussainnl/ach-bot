from telegram import Update
from telegram.ext import ContextTypes
from databases.mysql.user_table import User


async def new_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_full_name = "--" + update.effective_user.full_name
    username = update.effective_user.username if  update.effective_user.username else  user_full_name
    group_id = update.effective_chat.id

    with User() as Ur:
        Ur.add_user(group_id,user_id, username)
