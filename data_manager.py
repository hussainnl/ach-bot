import sqlite3
import os
import logging

DB = os.getenv("DB")
class Data_Manager:

    """
    This class is used to manage the data in the database.
    """
    def __init__(self,):
      
        self.con = sqlite3.connect(DB)
        self.cur = self.con.cursor()
    def make_new_table(self):
        logging.info(f"Data_Manager().make_new_table() start")
        self.cur.execute("CREATE TABLE IF NOT EXISTS  user_state(chat_id, user_id, score, missed, is_subscribed ,user_mode)")
        logging.info('Data_Manager().make_new_table() done')
        self.con.commit()

    def state_count(self,user_id,chat_id):
        """To get the user achievement score"""   
        logging.info(f"state_count start")  
        count = self.cur.execute("SELECT score FROM user_state WHERE user_id = ? AND chat_id = ?", (user_id,chat_id))       
        scorex = count.fetchone() 
        score = scorex[0]
        logging.info(f"state_count done")
        return score
    

        
    def add_new_user(self,user_id,chat_id):
        """To add a new user to the database"""
        logging.info(f"add_new_user start")
        score = 0
        missed = 1
        is_subscribed = 0
        user_mode = 0
        self.cur.execute("""INSERT INTO user_state(chat_id, user_id, score, missed, is_subscribed,user_mode)
                          VALUES(?, ?, ?, ?, ?, ?)""", (chat_id, user_id, score, missed, is_subscribed, user_mode))
        self.con.commit()  # Remember to commit the transaction after executing INSERT.
        logging.info(f"add_new_user done")

    def update_user_count(self,user_id, chat_id,points):
        """To add a new user to the database"""
        logging.info(f"update_user_count start")
        count = self.cur.execute("SELECT score FROM user_state WHERE user_id = ? AND chat_id = ?", (user_id,chat_id))
        self.con.commit()
        score = count.fetchone()[0]
        new_score = score + points 
        self.cur.execute("""
        UPDATE user_state
        SET score = ?
        WHERE user_id = ? AND chat_id = ?
        """, (new_score, user_id, chat_id))
        self.con.commit()
        logging.info(f"update_user_count done")

    def update_user_subscription(self,user_id, chat_id):
        """To add a new user to the database"""
        logging.info(f"update_user_subscription start")
        count = self.cur.execute("SELECT is_subscribed FROM user_state WHERE user_id = ? AND chat_id = ?", (user_id,chat_id))
        self.con.commit()
        is_subscribed = count.fetchone()[0] + 1 
        self.cur.execute("""
        UPDATE user_state
        SET is_subscribed = ?
        WHERE user_id = ? AND chat_id = ?
        """, (is_subscribed, user_id, chat_id))
        self.con.commit()
        logging.info(f"update_user_subscription done")

    def update_user_mode(self,user_id, chat_id,user_mode):
        """To add a new user to the database"""
        logging.info(f"update_user_mode start")
        self.cur.execute("""
        UPDATE user_state
        SET user_mode = ?
        WHERE user_id = ? AND chat_id = ?
        """, (user_mode, user_id, chat_id))
        self.con.commit()
        logging.info(f"update_user_mode done")

    def update_user_missed(self,user_id,chat_id,):
        """To update the user missed score"""
        logging.info(f"update_user_missed start")     
        self.cur.execute("""
        UPDATE user_state
        SET missed = ? 
        WHERE 
        user_id = ? AND chat_id = ?
        """, (0, user_id, chat_id))
        self.con.commit()
        logging.info(f"update_user_missed done")

    def weekly_missed_update(self,chat_id,):
        """To beggin a new week"""
        logging.info(f"weekly_missed_update start")
        res = self.cur.execute("SELECT missed, user_id FROM user_state WHERE chat_id = ?", (chat_id,))
        r = res.fetchall()
        for user in range(len(r)):
            new_missed = r[user][0] + 1
            user_id = r[user][1]
            self.cur.execute("""
            UPDATE user_state
            SET missed = ? 
            WHERE 
            user_id = ?
            """, (new_missed,user_id))
            self.con.commit()
        logging.info(f"weekly_missed_update done")

    def get_missed(self,user_id, chat_id):
        """To get the user missed score"""
        logging.info(f"get_missed start")
        missed = self.cur.execute("SELECT missed FROM user_state WHERE user_id = ? AND chat_id = ?", (user_id, chat_id,))
        user_missed = missed.fetchone()[0]
        logging.info(f"get_missed done")
        return user_missed
    
    def get_mode(self,user_id, chat_id):
        """To get the user mode status"""
        logging.info(f"get_missed start")
        mode = self.cur.execute("SELECT user_mode FROM user_state WHERE user_id = ? AND chat_id = ?", (user_id, chat_id,))
        user_mode = mode.fetchone()[0]
        logging.info(f"get_missed done")
        return user_mode
    
    def get_ban_users(self):
        """To get users to be banned"""
        res = self.cur.execute("SELECT missed FROM user_state WHERE ( user_mode = 1 AND missed = 2 ) OR missed = 4")
        banned_ids = []
        for id in res.fetchall():
            id[0]    
            banned_ids.append(id[0]) 
        return banned_ids

    def get_subscription_status(self, chat_id):
        """To get the subscription status of the users"""
        logging.info(f"get_subscription_status start")
        subscription_status = self.cur.execute("SELECT user_id FROM user_state WHERE is_subscribed != 0 AND chat_id = ?", (chat_id,))
        users_subscription_status = subscription_status.fetchall()
        logging.info(f"get_subscription_status done")
        return users_subscription_status 
          
    def check_user_id(self,user_id, chat_id):
        """To check if the user is in the database"""
        logging.info(f"check_user_id start")
        res = self.cur.execute("SELECT user_id FROM user_state WHERE chat_id = ?", (chat_id,))
        self.con.commit()
        user_ids = []
        for id in res.fetchall():
            id[0]    
            user_ids.append(id[0])            
        if user_id not in set(user_ids) or user_ids == []:   
            self.add_new_user(user_id, chat_id)
        logging.info(f"check_user_id done")

class Bot_Setting(Data_Manager):
    """to set the bot setting in a specific group"""

    def __init__(self,):
        super().__init__()
    
    def make_new_table(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS  bot_setting(chat_id, monitoring_topic, notification_topic, rules_topic)")
        logging.info('Bot_Setting().make_new_table() start')
        print('done')
        self.con.commit()
        logging.info(f"Bot_Setting().make_new_table() done")

        
    def add_new_group(self,chat_id):
        """To add a new group to the database"""
        logging.info(f"add_new_group start")
        monitoring_topic = str((0,0))
        notification_topic = 0
        rules_topic = 0
        self.cur.execute("""INSERT INTO bot_setting(chat_id, monitoring_topic, notification_topic, rules_topic)
                              VALUES(?, ?, ?, ?)""", 
                              (chat_id, monitoring_topic, notification_topic, rules_topic))
        self.con.commit()  
        logging.info(f"add_new_group done")

    def check_group_id(self, chat_id):
        """To check if the user is in the database"""
        logging.info(f"check_group_id start")
        res = self.cur.execute("SELECT chat_id FROM bot_setting")
        groups_ids = []
        for id in res.fetchall():
            id[0]    
            groups_ids.append(id[0])    
        if chat_id not in set(groups_ids) or groups_ids == []:   
            self.add_new_group(chat_id)
        logging.info(f"check_group_id done")

    def get_group_ids(self):
        """to get the group ids in which the bot is set"""   
        res = self.cur.execute("SELECT chat_id FROM bot_setting")
        groups_ids = []
        for id in res.fetchall():
            id[0]    
            groups_ids.append(id[0]) 
        return groups_ids

    def add_study_topic_id(self,monitoring_topic_id, chat_id,):
        """To add a new user to the database""" 
        logging.info(f"add_study_topic_id start")
        res = self.cur.execute("SELECT monitoring_topic FROM bot_setting WHERE chat_id = ?",(chat_id,)).fetchone()[0]
        srt_digit =  res.split(",")
        logging.info(f"study_topic_id {srt_digit}")


        weekly_id = int(srt_digit[1][:-1])
        digit = (int(monitoring_topic_id),int(weekly_id))
        study_id = str(digit)
        self.cur.execute("""
        UPDATE bot_setting
        SET monitoring_topic = ?
        WHERE chat_id = ?
        """, (study_id, chat_id))
        self.con.commit()
        logging.info(f"add_study_topic_id done")

    def add_weekly_topic_id(self,monitoring_topic_id, chat_id,):
        """To add a new user to the database"""  
        logging.info(f"add_weekly_topic_id start")
        res = self.cur.execute("SELECT monitoring_topic FROM bot_setting WHERE chat_id = ?",(chat_id,)).fetchone()[0]
        srt_digit =  res.split(",")
        study_id = int(srt_digit[0][1:])
        digit = (int(study_id),int(monitoring_topic_id))
        weekly_id = str(digit)
        self.cur.execute("""
        UPDATE bot_setting
        SET monitoring_topic = ?
        WHERE chat_id = ?
        """, (weekly_id, chat_id))
        self.con.commit()
        logging.info(f"add_weekly_topic_id done")

    def add_notification_topic_id(self,notification_topic_id, chat_id,):
        """To add a new user to the database"""  
        logging.info(f"add_notification_topic_id start")
        self.cur.execute("""
        UPDATE bot_setting
        SET notification_topic = ?
        WHERE chat_id = ?
        """, (notification_topic_id, chat_id))
        self.con.commit()     
        logging.info(f"add_notification_topic_id done")
   
    def add_rules_topic_id(self,rules_topic_id, chat_id,):
        """To add a new user to the database"""  
        logging.info(f"add_rules_topic_id start")
        self.cur.execute("""
        UPDATE bot_setting
        SET rules_topic = ?
        WHERE chat_id = ?
        """, (rules_topic_id, chat_id))
        self.con.commit()
        logging.info(f"add_rules_topic_id done")

    def get_study_topic_id(self, chat_id):
        """To get the monitoring topic id"""
        logging.info(f"get_study_topic_id start")
        res = self.cur.execute("SELECT monitoring_topic FROM bot_setting WHERE chat_id = ?", (chat_id,)).fetchone()[0]
        study_id = res.split(",")
        digit = int(study_id[0][1:])
        logging.info(f"get_study_topic_id done")
        return digit
    


    def get_weekly_topic_id(self, chat_id):
        """To get the monitoring topic id"""
        logging.info(f"get_weekly_topic_id start")
        res = self.cur.execute("SELECT monitoring_topic FROM bot_setting WHERE chat_id = ?", (chat_id,)).fetchone()[0]
        weekly_id =  res.split(",")
        digit = int(weekly_id[1][:-1])
        logging.info(f"get_weekly_topic_id done")
        return digit

    def get_notification_topic_id(self, chat_id):
        """To get the notification topic id"""
        logging.info(f"get_notification_topic_id start")
        notification_topic_id = self.cur.execute("SELECT notification_topic FROM bot_setting WHERE chat_id = ?", (chat_id,)).fetchone()[0]
        logging.info(f"get_notification_topic_id done")
        return notification_topic_id

    def get_rules_topic_id(self, chat_id):
        """To get the rules topic id"""
        logging.info(f"get_rules_topic_id start")
        rules_topic_id = self.cur.execute("SELECT rules_topic FROM bot_setting WHERE chat_id = ?", (chat_id,)).fetchone()[0]
        logging.info(f"get_rules_topic_id done")
        return rules_topic_id
