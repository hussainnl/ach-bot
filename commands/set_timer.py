from telegram import Update
from telegram.ext import ContextTypes ,Application
from data_manager import Data_Manager as DM ,Bot_Setting as BS
from utils import is_admin
import  datetime
from zoneinfo import ZoneInfo
import logging
async def weekly_check(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.data
    
    DM().weekly_missed_update(chat_id)
    banned_ids = DM().get_ban_users()
    for user_id in banned_ids :
        await context.bot.ban_chat_member(chat_id, user_id)
    await weekly_remender(context)

async def weekly_remender(context : ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.data
    app_info = await context.bot.get_me()
    bot_link = f"https://t.me/{app_info.username}?start=join_{chat_id}"
    msgg = "مرحبًا يا أبطال! حبيت أفكركم إن أسبوع جديد بدء و الوقت حان عشان تشاركوا إنجازاتكم الأسبوعية 📝\n"
    msg = await context.bot.send_message(
    chat_id,
    text=msgg + f'👋 وعشان توصلك التنبيهات في الخاص اضغط <a href="{bot_link}">اشتراك</a>',
    parse_mode="HTML")
    await context.bot.pin_chat_message(chat_id,msg.id)
    subs = DM().get_subscription_status(chat_id)
    for sub in range(len(subs)) :
        user_id = subs[sub][0]
        msg_user = "مرحبًا يا بطل! حبيت أفكرك إن أسبوع جديد بدء و الوقت حان عشان تشارك إنجازاتك الأسبوعية 📝\n"
        await context.bot.send_message(user_id,msg_user)
    logging.info(f"weekly_check done")


async def check_1(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.data
    subs = DM().get_subscription_status(chat_id)
    for sub in range(len(subs)) :   
        user_id = subs[sub][0]
        msg_user = "مرحبًا يا بطل! حبيت أفكرك تاني إن أسبوع جديد بدء و الوقت حان عشان تشارك إنجازاتك الأسبوعية 📝\n"
        missed = DM().get_missed(user_id, chat_id)
        logging.info(f"missed {missed}")
        if missed != 0 :     
            await context.bot.send_message(user_id,msg_user)


async def check_2(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.data
    subs = DM().get_subscription_status(chat_id)
    for sub in range(len(subs)) :
        user_id = subs[sub][0]
        msg_user = "مرحبًا يا بطل! حبيت أفكرك إن ناقص يوم على بداية الأسبوع الجديد ف يلا سجل إنجازك ي  بطل 📝\n"
        missed = DM().get_missed(user_id, chat_id)
        logging.info(f"missed2 {missed}")
        if missed != 0 :     
            await context.bot.send_message(user_id,msg_user)

async def set_timer(application:Application):
    
    group_ids = BS().get_group_ids()  
    for chat_id in  group_ids :           
        application.job_queue.run_daily(                        
            weekly_check,            
            time=datetime.time(hour=20,tzinfo=ZoneInfo("Africa/Cairo")),  
            days=(5,),  
            name=str(chat_id),                   
            chat_id=chat_id,
            data=chat_id,          
            )  
        application.job_queue.run_daily(                        
            check_1,            
            time=datetime.time(hour=20,tzinfo=ZoneInfo("Africa/Cairo")),  
            days=(1,),  
            name=str(chat_id),                   
            chat_id=chat_id,          
            data=chat_id,   
            )
        application.job_queue.run_daily(                        
            check_2,            
            time=datetime.time(hour=20,tzinfo=ZoneInfo("Africa/Cairo")),  
            days=(4,),  
            name=str(chat_id),                   
            chat_id=chat_id,
            data=chat_id,            
            )  
        logging.info(f"set_timer done")
