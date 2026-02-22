from telegram.ext import Application
from databases.mysql.group_table import Group
from timer.timer_jops import weekly_check,monday_remender,thursday_remender
from datetime import time
from zoneinfo import ZoneInfo
import logging


async def bot_timer(application:Application):
    """To set the timer for the bot to send the remender messages in the specific times """

    with Group() as Gp :
        group_ids = Gp.get_group_ids()
    for group_id in  group_ids :           
        application.job_queue.run_daily(                        
            weekly_check,            
            time= time(tzinfo=ZoneInfo("Africa/Cairo")),  
            days=(6,),  
            name=str(group_id),                   
            chat_id=group_id,
            data=group_id,          
            )  
        application.job_queue.run_daily(                        
            monday_remender,            
            time= time(hour=3,minute=11,tzinfo=ZoneInfo("Africa/Cairo")),  
            days=(0,),  
            name=str(group_id),                   
            chat_id=group_id,          
            data=group_id,   
            )
        application.job_queue.run_daily(                        
            thursday_remender,            
            time= time(hour=20,tzinfo=ZoneInfo("Africa/Cairo")),  
            days=(4,),  
            name=str(group_id),                   
            chat_id=group_id,
            data=group_id,            
            )  
        logging.info(f"set_timer done")
