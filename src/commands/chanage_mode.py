from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from databases.mysql.user_table import User
import logging


# /start command
async def chanage_mode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[
            InlineKeyboardButton("🔥 سهل", callback_data="option_1"),
            InlineKeyboardButton("⚡ صعب", callback_data="option_2")
        ],]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "اختار وضع من الاختيارات 👇",
        reply_markup=reply_markup
    )

# Handle button press
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = update.effective_user.id
    group_id = update.effective_chat.id
    await query.answer()  # لازم عشان تيليجرام

    selected_value = query.data  # دي القيمة اللي رجعت
    # مثال تعامل مع القيمة
    if selected_value == "option_1":
        text = "انت اخترت الوضع السهل 🌙"
        with User() as Ur :
            Ur.update_user_mode(user_id,group_id,0)
    elif selected_value == "option_2":
        with User() as Ur :
            Ur.update_user_mode(user_id,group_id,1)
        text = "انت اخترت الوضع الصعب 💪"
    else:
        text = "اختيار غير معروف"
    await query.edit_message_text(text=text)


