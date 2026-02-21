from telegram import Update
from telegram.ext import ContextTypes
from message_handler.messages import Messages as msg
from databases.mysql.user_table import User
from databases.mysql.group_table import Group
from databases.mongodb.ach_report import AchReport as AR






async def monitoring_topic(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    group_id = update.effective_chat.id 

    with Group() as Gp:
        study_topic_id = Gp.get_study_topic_id(group_id)
        weekly_topic_id = Gp.get_weekly_topic_id(group_id)
    monitoring_topic_id = update.message.message_thread_id
    
    if monitoring_topic_id == study_topic_id:
        points  = 7
        await submit_achievement(update, context,points)
    elif monitoring_topic_id == weekly_topic_id:
        with User() as Ur:
            user_mode = Ur.get_user_mode(user_id,group_id)
        if user_mode == 0 :
            points = 70
        elif user_mode == 1:
            points = 140
        await submit_achievement(update, context,points)




async def submit_achievement(update: Update, context: ContextTypes.DEFAULT_TYPE,points) -> None:
    user_id = update.effective_user.id
    group_id = update.effective_chat.id
    group_name = update.effective_chat.title
    text = update.message.text

    if msg().check_achievement(update.message.text,points):
        with User() as Ur:
            if  points < 70:
                """for the study achievements"""
                Ur.update_user_score(user_id, group_id, points)
                user_scor = Ur.get_user_score(user_id, group_id)
                parts = text.split(':', 1)
                achievement = parts[1].strip()
                user_study_achs = AR().get_user_study_achs(user_id,group_id)
                if  len(user_study_achs) >=3:
                     Ur.update_user_missed(user_id, group_id)
                AR().save_study_ach(user_id,group_id,group_name,achievement,points)
                message = msg().confirm_ach_msg(points,user_scor)
                await update.message.reply_text(message)

            elif Ur.get_ach_week_state(user_id, group_id) == 0:
                """for the weekly achievements"""
                Ur.update_user_score(user_id, group_id, points)
                user_scor = Ur.get_user_score(user_id, group_id)
                Ur.update_user_missed(user_id, group_id)
                Ur.update_user_ach_week(user_id, group_id)
                AR().save_weekly_ach(user_id,group_id,text,points)
                
                message = msg().confirm_ach_msg(points,user_scor)
                await update.message.reply_text(message)
            else:
                await update.message.reply_text(
                    msg().ach_limmit_msg()
                )
    elif points >= 70 :
        await update.message.reply_text(
            msg().weekly_warrning_msg()
        )
    else:
        await update.message.reply_text(
            msg().study_warrning_msg()
        )
        
