from telegram import Update
from telegram.ext import ContextTypes
from databases.mysql.user_table import User
from message_handler.message_handler import prepare_weekly_report
import logging

async def weekly_report(update: Update, context: ContextTypes.DEFAULT_TYPE)-> None:    

    user_id = update.effective_user.id
    with User() as Ur:
        user_groups = Ur.is_user_a_member(user_id)
    try:
        for group_id in user_groups:
            with User() as Ur :
                user_report = prepare_weekly_report(user_id,group_id)
                await context.bot.send_message(user_id,user_report)
    except Exception as e:
        logging.info(f"Error : {e}")
        await update.message.reply_text("لازم الأمر يكون في المحادثة بين وبين البوت وعندك إنجازات خلال الأسبوع ده ب الفعل")
    