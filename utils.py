# utils.py
from telegram.ext import ContextTypes
from telegram import Update


async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int ) -> bool:
    chat_id = update.effective_chat.id
    
    
    member = await context.bot.get_chat_member(chat_id, user_id)
    try:  
        if member.status in ['administrator', 'creator']:
            return True
    
    except Exception as e:
        print(f"Error in is_admin: {e}")
        return False

   