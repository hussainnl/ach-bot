from telegram import Update
from telegram.ext import ContextTypes
from data_manager import Data_Manager as DM
import logging

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if args and args[0].startswith("join_"):
        group_id = args[0].split("_", 1)[1]  # هنا بجيب group_id من اللينك
        logging.info(type(group_id))
        user_id = update.effective_user.id

        # سجل في SQL إن الشخص ده اشترك من الجروب ده
        DM().update_user_subscription(user_id, int(group_id))

        await update.message.reply_text("✅ تم ربطك بالجروب بنجاح!")
    else:
        await update.message.reply_text("👋 أهلاً بيك في البوت!")
