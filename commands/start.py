from telegram import Update ,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from databases.mysql.user_table import User
import logging

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    keyboard = [[
            InlineKeyboardButton("Self Growth – No Limit", url="https://t.me/+4qvieInOHHA3NzM0"),
            InlineKeyboardButton("Software Engineers | Nawah Project", url="https://t.me/+fquO7E9iWu85NzM0")
        ], ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    user_id = update.effective_user.id

    if args and args[0].startswith("join_"):
        group_id = args[0].split("_", 1)[1]  # هنا بجيب group_id من اللينك
        logging.info(type(group_id))
        with User() as Ur :
            Ur.update_user_subscription(user_id, int(group_id),1)

        await update.message.reply_text("✅ تم ربطك بالجروب بنجاح!")
    else:

        with User() as Ur:
            user_groups = Ur.is_user_a_member(user_id)
        if user_groups == [] :
                await update.message.reply_text(f"البوت ده تابع للجروبات اللي تحت دي"
        f"\nSelf Growth – No Limit""هو جروب للتطوير الذاتي"
        f"\nSoftware Engineers | Nawah Project"" هو جروب للأشخاص اللي بتتعلم برمجة"
        f"\n اختار الجروب اللي حابب تنضم ليه \n بعد تعال عيد اشتراك تاني ب البوت",
        reply_markup=reply_markup
    )
        else :
            for group_id in user_groups:
                with User() as Ur :
                    Ur.update_user_subscription(user_id, int(group_id),1)
            await update.message.reply_text("👋 أهلاً بيك في البوت!")