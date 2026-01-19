from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters , CallbackQueryHandler 
from data_manager import Data_Manager as DB , Bot_Setting as BS
import os
from commands.set_group import set_group
from commands.set_monitoring_topics import study_monitoring_topic , weekly_monitoring_topic
from commands.set_notification_topic import set_notification_topic
from commands.set_rules_topic import set_rules_topic
from commands.massage_handler import monitoring_topic , new_user
from commands.state import state
from commands.set_timer import set_timer
from commands.restart_missed import restart_missed
from commands.start import start 
from commands.chanage_mode import chanage_mode , button_handler
BOT_TOKEN = os.getenv("BOT_TOKEN")
import logging

logging.basicConfig(
    level=logging.DEBUG, 
    format="%(asctime)s - %(levelname)s - %(message)s",  
    datefmt="%Y-%m-%d %H:%M:%S"  
)

logging.getLogger("httpx").setLevel(logging.WARNING)

DB().make_new_table()
BS().make_new_table()
group_ids = BS().get_group_ids()



app = ApplicationBuilder().token(BOT_TOKEN).post_init(set_timer).build()


app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("set_group", set_group))
app.add_handler(CommandHandler("study_monitoring_topic", study_monitoring_topic))
app.add_handler(CommandHandler("weekly_monitoring_topic", weekly_monitoring_topic))
app.add_handler(CommandHandler("set_notification_topic", set_notification_topic))
app.add_handler(CommandHandler('set_rules_topic', set_rules_topic))
app.add_handler(CommandHandler('restart_missed', restart_missed))
app.add_handler(CommandHandler('chanage_mode', chanage_mode))
app.add_handler(CommandHandler('state', state))
app.add_handler(MessageHandler(filters.ChatType.GROUPS & filters.StatusUpdate.NEW_CHAT_MEMBERS, new_user))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, monitoring_topic))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(CommandHandler('set_timer', set_timer))


app.run_polling()