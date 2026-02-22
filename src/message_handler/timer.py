from telegram.ext import ContextTypes
from message_handler.messages import Messages as msg
from databases.mysql.group_table import Group


async def timer_message(context : ContextTypes.DEFAULT_TYPE,group_id,check_id):
    """To prepare the remender message"""
    app_info = await context.bot.get_me()
    sub_msg = msg().sub_msg(app_info.username)
    group_remender_msg = msg().group_remender_msg(check_id)
    with Group() as Gp :
        rules_topic_id = Gp.get_rules_topic_id(group_id)
    rules_reminder_msg = msg().rules_reminder_msg(group_id,rules_topic_id)

    message = group_remender_msg + sub_msg + rules_reminder_msg

    return message

async def remender_sender(context : ContextTypes.DEFAULT_TYPE,group_id,check_id):
    """To send the remender message in the group notification topic"""

    with Group() as Gp :
        notification_topic_id = Gp.get_notification_topic_id(group_id)

    message = await timer_message(context,group_id,check_id)
    msg = await context.bot.send_message(
    group_id,
    text= message,
    parse_mode="HTML",message_thread_id=notification_topic_id)
    await context.bot.pin_chat_message(group_id,msg.id)
