from telegram import Update
from telegram.ext import ContextTypes
from message_handler.messages import Messages as msg
from doc_register import doc_register
from databases.mysql.user_table import User
from databases.mysql.group_table import Group
import logging
import os


DOCUMENT_ID = os.getenv("DOCUMENT_ID")

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


async def new_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_full_name = "--" + update.effective_user.full_name
    username = update.effective_user.username if  update.effective_user.username else  user_full_name
    group_id = update.effective_chat.id

    with User() as Ur:
        Ur.add_user(group_id,user_id, username)


async def submit_achievement(update: Update, context: ContextTypes.DEFAULT_TYPE,points) -> None:
    user_id = update.effective_user.id
    group_id = update.effective_chat.id
    text = update.message.text
    separator = "\n___________________________________________\n"
    doc_message = text + separator

    if msg().check_achievement(update.message.text,points):
        with User() as Ur:
            if  points < 70:
                Ur.update_user_score(user_id, group_id, points)
                user_scor = Ur.get_user_score(user_id, group_id)

                doc_register(DOCUMENT_ID,doc_message )
                message = msg().confirm_ach_msg(points,user_scor)
                await update.message.reply_text(message)

            elif Ur.get_user_missed(user_id, group_id) > 0:
                Ur.update_user_score(user_id, group_id, points)
                user_scor = Ur.get_user_score(user_id, group_id)
                Ur.update_user_missed(user_id, group_id)

                doc_register(DOCUMENT_ID,doc_message )

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
        



