from telegram.ext import ContextTypes 
from databases.mysql.user_table import User
from databases.mongodb.mongo_utils import DatabaseHandler as DH
from databases.mongodb.ach_report import AchReport as AR
from message_handler.messages import Messages as msg
from message_handler.weekly_report import prepare_weekly_report
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import logging
from message_handler.timer import remender_sender



async def weekly_check(context: ContextTypes.DEFAULT_TYPE):
    group_id = context.job.data
    now = datetime.now(ZoneInfo("Africa/Cairo"))
    datetime_now = f"{now.year}-{now.month:02d}-{now.day:02d}"
    collection_name = f"weekly_report:{datetime_now}"
    DH().create_new_collection(collection_name)
    await ban_users(context,group_id)
    await weekly_remender(context)

async  def ban_users(context: ContextTypes.DEFAULT_TYPE,group_id):
    """To ban the users who didn't share their achievements in the week """
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

async def weekly_remender(context : ContextTypes.DEFAULT_TYPE):
    """To notificat the members of the groups about the new week """
    group_id = context.job.data
    check_id = 0
    await remender_sender(context,group_id,check_id)
    await user_remender(context,group_id,check_id)
    logging.info(f"weekly_check done")


async def user_remender(context : ContextTypes.DEFAULT_TYPE,group_id,check_id):
    """To send remender notification in user's inbox """
    with User() as Ur :
        subs = Ur.get_subscription_users(group_id)
        logging.info(f"subs : {subs}")
        missed_users_id = Ur.get_missed_users(group_id)
    group_name = AR().get_group_name(group_id)
    message = msg().user_remender_msg(check_id,group_name)
    if check_id == 0 :
        for sub in range(len(subs)):
            user_id = subs[sub]
            try:
                user_report = prepare_weekly_report(user_id,group_id)
                await context.bot.send_message(user_id,f"{message}\n {user_report}")
            except:
                await context.bot.send_message(user_id,f"{message}")
    else:
        for user_id in missed_users_id :
            await context.bot.send_message(user_id,message)

async def monday_remender(context: ContextTypes.DEFAULT_TYPE):
    """To notificat the members of the groups with missed point to shara there acheivements in Monday """
    group_id = context.job.data
    check_id = 1
    await user_remender(context,group_id,check_id)
    await remender_sender(context,group_id,check_id)

async def thursday_remender(context: ContextTypes.DEFAULT_TYPE):
    """To notificat the members of the groups with missed point to shara there acheivements in Thursday """
    group_id = context.job.data
    check_id = 2
    await remender_sender(context,group_id,check_id)
    await user_remender(context,group_id,check_id)
