from telegram import Update
from telegram.ext import ContextTypes
from data_manager import Data_Manager as DB , Bot_Setting as BS
from check_ach import CheckAchievement
from doc_register import doc_register
import logging
import os
from dotenv import load_dotenv

load_dotenv()
DOCUMENT_ID = os.getenv("DOCUMENT_ID")

async def monitoring_topic(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id    
    DB().check_user_id(user_id,chat_id)
    study_topic_id = [BS().get_study_topic_id(chat_id)]
    weekly_topic_id = BS().get_weekly_topic_id(chat_id)
    monitoring_topic_id = update.message.message_thread_id
    
    if monitoring_topic_id in study_topic_id:
        logging.info(f"study_topic_id start")
        points  = 7
        await submit_achievement(update, context,points)
    elif monitoring_topic_id is weekly_topic_id:
        logging.info(f"weekly_topic_id start")
        user_mode = DB().get_mode(user_id,chat_id)
        if user_mode == 0 :
            points = 70
        elif user_mode == 1:
            points = 140
        await submit_achievement(update, context,points)


async def new_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    DB().check_user_id(user_id, chat_id)


async def submit_achievement(update: Update, context: ContextTypes.DEFAULT_TYPE,points) -> None:
    logging.info(f"submit_achievement start")
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    text = update.message.text
    if CheckAchievement().check_achievement(update.message.text,points):
        DB().check_user_id(user_id, chat_id)
        logging.info(f"CheckAchievement start")
        if DB().get_missed(user_id, chat_id) > 0 or points < 70:
            DB().update_user_count(user_id, chat_id, points)
            user_scor = DB().state_count(user_id, chat_id)
            DB().update_user_missed(user_id, chat_id)
           
            message = (
            f"اي تغيير في الكود بيتم فعلاً بعد البوش"
            f"تم تسجيل إنجازك بنجاح 🏆\n"
            f"حصلت على {points} نقاط جديدة!🌟\n\n"
            f"✨ إجمالي نقاطك الآن: {user_scor} ✨")
            # f"🔥 استمر في جمع النقاط… كل خطوة بتقربك من القمة 🏆") #When I create the promotion ladder
            separator = "\n___________________________________________\n"
            doc_message = text + separator
            doc_register(DOCUMENT_ID,doc_message )
            await update.message.reply_text(message)
        else:
            await update.message.reply_text(
                "اي تغيير في الكود بيتم فعلاً بعد البوش"
                "⚠️ لقد سجّلت إنجازك هذا الأسبوع بالفعل.\n"
                "⏳ لا يمكن تسجيل أكثر من مرة في نفس الأسبوع."
            )
    elif points == 70 :
        await update.message.reply_text(
            "📝 تذكير مهم:\n\n"
            "المكان ده مخصص فقط لتسجيل **الإنجازات الأسبوعية** ✅\n"
            "عند إرسال الإنجاز لازم تحتوي الرسالة على:\n"
            "🔹 كلمة *الإنجاز الأسبوعي* أو\n"
            "🔹 كلمة *الإنجاز* لوحدها."
        )
    else:
        await update.message.reply_text(
            "📝 تذكير مهم:\n\n"
            "المكان ده مخصص فقط لتسجيل *الإنجازات الدراسية* ✅\n"
            "عند إرسال الإنجاز لازم تحتوي الرسالة على:\n"
            "🔹 كلمة *الدراسي* أو\n"
            "🔹 كلمة *دراسي* لوحدها."
        )


