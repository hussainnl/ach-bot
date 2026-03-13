
class Messages:
    def __init__(self,):
        self.study_keywords = ["دراسي", "دراسية", "الدراسى","الدراسي", "الدراسية",
                               "الدراسة", "دراسة", "للدراسة", "دراستي",
                                 "دراسيةً","مذاكرة", "مذاكرتي", "للمذاكرة"]
        self.week_keywords = ["الأسبوع", "الاسبوع", "أسبوع", "اسبوع",
                               "الأسبوعي", "الاسبوعي", "أسبوعي", "اسبوعي"]
        
    def check_achievement(self,massage,points) -> bool:
        if points >= 70:
            keywords = self.week_keywords
        else:
            keywords = self.study_keywords
        state = False
        for keyword in keywords :
            if keyword in massage :
                state = True
                break
        return state
    
    def study_warrning_msg(self) -> str :
        """ a message to warn the user if he send a message that doesn't contain the study keywords"""
        message = (
            "📝 تذكير مهم:\n\n"
            "المكان ده مخصص فقط لتسجيل *الإنجازات الدراسية* ✅\n"
            "عند إرسال الإنجاز لازم تحتوي الرسالة على:\n"
            "🔹 كلمة *الدراسي* أو\n"
            "🔹 كلمة *مذاكرتي* لوحدها."
        )
        return message
    
    def weekly_warrning_msg(self) -> str :
        """ a message to warn the user if he send a message that doesn't contain the weekly keywords"""
        message = (
            "📝 تذكير مهم:\n\n"
            "المكان ده مخصص فقط لتسجيل **الإنجازات الأسبوعية** ✅\n"
            "عند إرسال الإنجاز لازم تحتوي الرسالة على:\n"
            "🔹 كلمة *الأسبوعي* أو\n"
            "🔹 كلمة *اسبوعي* لوحدها."
        )
        return message

    def confirm_ach_msg(self,points,user_scor) -> str :
        """a message to confirm the user that his achievement has been recorded successfully and show him the points he got and his total score"""
        message = (
        f"تم تسجيل إنجازك بنجاح 🏆\n"
        f"حصلت على {points} نقاط جديدة!🌟\n\n"
        f"✨ إجمالي نقاطك الآن: {user_scor} ✨")
        return message
    
    def ach_limmit_msg(self) -> str :
        """a message to warn the user that he has reached the limit of weekly achievements for this week"""
        message = (
            "⚠️ لقد سجّلت إنجازك هذا الأسبوع بالفعل.\n"
            "⏳ لا يمكن تسجيل أكثر من مرة في نفس الأسبوع."
        )
        return message
    
    def get_rules_topic_link(self,group_id,rules_topic_id) -> str :
        """To get the link of the rules topic in the group"""
        group_id = str(group_id)[-10:]
        rules_topic_link = f"https://t.me/c/{group_id}/{rules_topic_id}"
        return rules_topic_link
    
    def rules_reminder_msg(self,group_id,rules_topic_id) -> str:
        """To prepare the rules reminder message"""
        rules_topic_link = self.get_rules_topic_link(group_id,rules_topic_id)
        message = (
            f"""📜 وعلشان تفهم وضع الجروب هنا ف ممكن تشوف <a href="{rules_topic_link}">النظام والقواعد</a>"""
  
        )
        return message

    def get_bot_link(self,bot_username) -> str:
        """To get the link of the group bot"""
        bot_link = f"https://t.me/{bot_username}"
        return bot_link
    
    def sub_msg(self,bot_username) -> str:
        """To prepare the subscription message"""
        bot_link = self.get_bot_link(bot_username)
        message = f"""وعشان توصلك التنبيهات في الخاص اضغط <a href="{bot_link}">اشتراك</a>\n"""
        return message
    
    def user_remender_msg(self,check_id,group_name)-> str:

        new_week_msg = f"مرحبًا يا بطل! حبيت أفكرك إن أسبوع جديد بدء و الوقت حان عشان تشارك إنجازاتك الأسبوعية 📝في جروب {group_name}"
        monday_msg = f"مرحبًا يا بطل! حبيت أفكرك تاني إن أسبوع جديد بدء و الوقت حان عشان تشارك إنجازاتك الأسبوعية 📝في جروب {group_name}"
        thursday_msg = f"مرحبًا يا بطل! حبيت أفكرك إن ناقص يوم على بداية الأسبوع الجديد ف يلا سجل إنجازك ي  بطل 📝في جروب {group_name}"
        if check_id == 0 :
            return new_week_msg
        elif check_id == 1 :
            return monday_msg
        elif check_id == 2 :
            return thursday_msg

    def group_remender_msg(self,check_id) -> str:

        new_week_msg = "مرحبًا يا أبطال! أسبوع جديد بدء و الوقت حان عشان تشاركوا إنجازاتكم الأسبوعية 📝\n"
        monday_msg = "مرحبًا يا أبطال! حبيت أفكركم ب الأشترك في البوت علشان يوصلكم تقرير أسبوعي ب إنجازتكم 📝\n"
        thursday_msg = "مرحبًا يا أبطال! حبيت أفكركم إن ناقص يوم على بداية أسبوع جديد ف شاركوا إنجازاتكم الأسبوعية 📝\n"
        if check_id == 0 :
            return new_week_msg
        elif check_id == 1 :
            return monday_msg
        elif check_id == 2 :
            return thursday_msg
   

