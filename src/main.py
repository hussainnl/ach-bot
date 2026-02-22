from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters , CallbackQueryHandler 

from databases.mysql.group_table import Group
from databases.mysql.user_table import User

from commands.set_group import set_group
from commands.set_monitoring_topics import study_monitoring_topic , weekly_monitoring_topic
from commands.set_notification_topic import set_notification_topic
from commands.set_rules_topic import set_rules_topic
from commands.state import state
from commands.reset_missed import reset_missed
from commands.start import start 
from commands.chanage_mode import chanage_mode , button_handler
from commands.weekly_report import weekly_report

from timer.timer_handler import bot_timer

from message_handler.achievements import monitoring_topic 
from message_handler.new_user import new_user

import logging
import os
BOT_TOKEN = os.getenv("BOT_TOKEN")


logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s",  
    datefmt="%Y-%m-%d %H:%M:%S"  
)

logging.getLogger("httpx").setLevel(logging.WARNING)

with Group()as Gp,User() as Ur:
    Ur.table_check()
    Gp.table_check()

app = ApplicationBuilder().token(BOT_TOKEN).post_init(bot_timer).build()


app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("set_group", set_group))
app.add_handler(CommandHandler("study_monitoring_topic", study_monitoring_topic))
app.add_handler(CommandHandler("weekly_monitoring_topic", weekly_monitoring_topic))
app.add_handler(CommandHandler("set_notification_topic", set_notification_topic))
app.add_handler(CommandHandler('set_rules_topic', set_rules_topic))
app.add_handler(CommandHandler('restart_missed', reset_missed))
app.add_handler(CommandHandler('chanage_mode', chanage_mode))
app.add_handler(CommandHandler('state', state))
app.add_handler(CommandHandler('weekly_report', weekly_report))
app.add_handler(MessageHandler(filters.ChatType.GROUPS & filters.StatusUpdate.NEW_CHAT_MEMBERS, new_user))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, monitoring_topic))
app.add_handler(CallbackQueryHandler(button_handler))


app.run_polling()