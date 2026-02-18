from telegram import Update
from telegram.ext import ContextTypes ,Application
from databases.mysql.group_table import Group
from databases.mysql.user_table import User
from message_handler.messages import Messages as msg
from datetime import datetime, timedelta,time
from zoneinfo import ZoneInfo
import logging


async def weekly_check(context: ContextTypes.DEFAULT_TYPE):
    group_id = context.job.data
    with User() as Ur :
        unban_at = datetime.now() + timedelta(seconds=30)
        Ur.weekly_missed_update(group_id)
        banned_ids = Ur.get_ban_users(group_id)
        
        for user_id in banned_ids :
            try:
                await context.bot.ban_chat_member(group_id, user_id,until_date=unban_at)
                Ur.delete_user(user_id,group_id)
            except Exception as e:
                    logging.info(f"error {e}")
                    continue
    await weekly_remender(context)


async def weekly_remender(context : ContextTypes.DEFAULT_TYPE):
    """To notificat the members of the groups about the new week """
    group_id = context.job.data
    message_id = 1
    check_id = 0
    await remender_sender(context,group_id,message_id)
    await user_remender(context,group_id,check_id)
    logging.info(f"weekly_check done")

async def remender_sender(context : ContextTypes.DEFAULT_TYPE,group_id,message_id):
    """To send the remender message"""
    with Group() as Gp :
        notification_topic_id = Gp.get_notification_topic_id(group_id)
    message = await remender_message(context,group_id,message_id)
    msg = await context.bot.send_message(
    group_id,
    text= message,
    parse_mode="HTML",message_thread_id=notification_topic_id)
    await context.bot.pin_chat_message(group_id,msg.id)


async def remender_message(context : ContextTypes.DEFAULT_TYPE,group_id,message_id):
    """To prepare the remender message"""
    app_info = await context.bot.get_me()
    bot_link = f"https://t.me/{app_info.username}?start=join_{group_id}"

    message_id = message_id
    if message_id == 1 :
        #New week message id = 1
        msgg = "مرحبًا يا أبطال! أسبوع جديد بدء و الوقت حان عشان تشاركوا إنجازاتكم الأسبوعية 📝\n"
    else:
        #Besfore new week message id = 2
        msgg = "مرحبًا يا أبطال! حبيت أفكركم إن ناقص يوم على بداية أسبوع جديد ف شاركوا إنجازاتكم الأسبوعية 📝\n"
    message = msgg + f"👋 وعشان توصلك التنبيهات في الخاص اضغط <a href={bot_link}>اشتراك</a>"
    with Group() as Gp :
        rules_topic_id = Gp.get_rules_topic_id(group_id)
    rules_reminder_msg = msg().rules_reminder_msg(group_id,rules_topic_id)
    return message + rules_reminder_msg


async def user_remender(context : ContextTypes.DEFAULT_TYPE,group_id,check_id):
    """To send remender notification in user's inbox """
    with User() as Ur :
        subs = Ur.get_subscription_users()

    msg_user_0 = "مرحبًا يا بطل! حبيت أفكرك إن أسبوع جديد بدء و الوقت حان عشان تشارك إنجازاتك الأسبوعية 📝\n"
    msg_user_1 = "مرحبًا يا بطل! حبيت أفكرك تاني إن أسبوع جديد بدء و الوقت حان عشان تشارك إنجازاتك الأسبوعية 📝\n"
    msg_user_2 = "مرحبًا يا بطل! حبيت أفكرك إن ناقص يوم على بداية الأسبوع الجديد ف يلا سجل إنجازك ي  بطل 📝\n"

    for sub in subs :
        user_id = subs[sub][0] 
        if check_id == 0 :
            await context.bot.send_message(user_id,msg_user_0)
        elif check_id == 1 :
            with User() as Ur :
                missed = Ur.get_user_missed(user_id, group_id)
            if missed != 0 :     
                await context.bot.send_message(user_id,msg_user_1)
        elif check_id == 2 :
            with User() as Ur :
                missed = Ur.get_user_missed(user_id, group_id)
            if missed != 0 :     
                await context.bot.send_message(user_id,msg_user_2)

async def check_1(context: ContextTypes.DEFAULT_TYPE):
    """To notificat the members of the groups with missed point to shara there acheivements in Monday """
    group_id = context.job.data
    check_id = 1
    await user_remender(context,group_id,check_id)
     

async def check_2(context: ContextTypes.DEFAULT_TYPE):
    """To notificat the members of the groups with missed point to shara there acheivements in Thursday """
    group_id = context.job.data
    check_id = 2
    message_id = 2
    msg =await remender_sender(context,group_id,message_id)
    await context.bot.pin_chat_message(group_id,msg.id)
    await user_remender(context,group_id,check_id)





async def set_timer(application:Application):

    with Group() as Gp :
        group_ids = Gp.get_group_ids()
    for group_id in  group_ids :           
        application.job_queue.run_daily(                        
            weekly_check,            
            time= time(hour=21,minute=27,tzinfo=ZoneInfo("Africa/Cairo")),  
            days=(2,),  
            name=str(group_id),                   
            chat_id=group_id,
            data=group_id,          
            )  
        application.job_queue.run_daily(                        
            check_1,            
            time= time(hour=20,tzinfo=ZoneInfo("Africa/Cairo")),  
            days=(1,),  
            name=str(group_id),                   
            chat_id=group_id,          
            data=group_id,   
            )
        application.job_queue.run_daily(                        
            check_2,            
            time= time(hour=20,tzinfo=ZoneInfo("Africa/Cairo")),  
            days=(4,),  
            name=str(group_id),                   
            chat_id=group_id,
            data=group_id,            
            )  
        logging.info(f"set_timer done")
