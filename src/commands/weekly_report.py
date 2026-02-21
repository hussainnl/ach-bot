from telegram import Update
from telegram.ext import ContextTypes
from databases.mysql.user_table import User
from message_handler.message_handler import prepare_weekly_report
import logging

async def weekly_report(update: Update, context: ContextTypes.DEFAULT_TYPE)-> None:    
    msg_group_id = update.effective_chat.id
    logging.info(f"weekly_report called in group {msg_group_id}")
    user_id = update.effective_user.id
    with User() as Ur:
        user_groups = Ur.is_user_a_member(user_id)
    
    try: 
        if user_id == msg_group_id:
            for group_id in user_groups:
                try:
                    with User() as Ur :
                        user_report = prepare_weekly_report(user_id,group_id)
                    await context.bot.send_message(user_id,user_report)
                except:
                    continue
        else:
            raise Exception("This command should be used in the private chat between the user and the bot")
        
    except Exception as e:
        logging.info(f"Error : {e}")
        await update.message.reply_text("لازم الأمر يكون في المحادثة بين وبين البوت وعندك إنجازات خلال الأسبوع ده ب الفعل")
    