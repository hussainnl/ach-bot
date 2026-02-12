import pymysql
from databases.mysql.config_db import Config
import logging

class Group :

    def __init__(self):
        self.config = Config().data
        self.con = None

    def __enter__(self):
        self.con =pymysql.connect(**self.config)
        return self
    
    def __exit__(self,exc_type, exc_val, exc_tb):
        if self.con :
            self.con.close()
    def table_check(self):
        """To check if the table exist""" 
        with self.con.cursor() as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS  
                        group_info (
                        group_id BIGINT NOT NULL,
                        group_name VARCHAR(128) NOT NULL,
                        study_topic_id SMALLINT
                        DEFAULT NULL,
                        weekly_topic_id SMALLINT
                        DEFAULT NULL,
                        notification_topic_id SMALLINT
                        DEFAULT NULL,
                        rules_topic_id SMALLINT
                        DEFAULT NULL,
                        PRIMARY KEY (group_id),
                        UNIQUE  unq_group_name (group_name))""")   
            print("btyhk")
            self.con.commit()
    def add_new_group(self,group_id,group_name):
        """To add a new group to the database"""
        logging.info(f"start add_new_group")
        try:
            with self.con.cursor() as cur:
                cur.execute("""INSERT INTO group_info(group_id, group_name)
                            VALUES( %s, %s)""", ( group_id,group_name))
                self.con.commit()
                logging.info(f"add_new_group done")
        except:
            logging.info(f"the group is alread there")
    
    def get_group_ids(self):
        """to get the group ids in which the bot is set"""   
        with self.con.cursor() as cur:
            cur.execute("SELECT group_id FROM group_info")
            groups_ids = []
            for id in cur.fetchall():
                id[0]    
                groups_ids.append(id[0]) 
            return groups_ids

    def update_study_topic_id(self,study_topic_id,group_id):
        """To update the study topic id"""
        with self.con.cursor() as cur:
            cur.execute("""
            UPDATE group_info
            SET study_topic_id = %s
            WHERE group_id = %s
            """, (study_topic_id,group_id))
            self.con.commit()

    def get_study_topic_id(self,group_id):
        """To get the study_topic_id"""
        with self.con.cursor() as cur:
            cur.execute("SELECT study_topic_id FROM group_info WHERE group_id = %s", (group_id,))       
            study_topic_id = cur.fetchone()[0]
            return study_topic_id
        
    def update_weekly_topic_id(self,weekly_topic_id,group_id):
        """To update the weekly topic id"""
        with self.con.cursor() as cur:
            cur.execute("""
            UPDATE group_info
            SET weekly_topic_id = %s
            WHERE group_id = %s
            """, (weekly_topic_id,group_id))
            self.con.commit()

    def get_weekly_topic_id(self,group_id):
        """To get the weekly_topic_id"""
        with self.con.cursor() as cur:
            cur.execute("SELECT weekly_topic_id FROM group_info WHERE group_id = %s", (group_id,))       
            weekly_topic_id = cur.fetchone()[0]
            return weekly_topic_id
        
    def update_notification_topic_id(self,notification_topic_id,group_id):
        """To update the notification topic id"""
        with self.con.cursor() as cur:
            cur.execute("""
            UPDATE group_info
            SET notification_topic_id = %s
            WHERE group_id = %s
            """, (notification_topic_id,group_id))
            self.con.commit()
    def get_notification_topic_id(self,group_id):
        """To get the notification_topic_id"""
        with self.con.cursor() as cur:
            cur.execute("SELECT notification_topic_id FROM group_info WHERE group_id = %s", (group_id,))       
            notification_topic_id = cur.fetchone()[0]
            return notification_topic_id
        
    def update_rules_topic_id(self,rules_topic_id,group_id):
        """To update the rules topic id"""
        with self.con.cursor() as cur:
            cur.execute("""
            UPDATE group_info
            SET rules_topic_id = %s
            WHERE group_id = %s
            """, (rules_topic_id,group_id))
            self.con.commit()
    def get_rules_topic_id(self,group_id):
        """To get the rules_topic_id"""
        with self.con.cursor() as cur:
            cur.execute("SELECT rules_topic_id FROM group_info WHERE group_id = %s", (group_id,))       
            rules_topic_id = cur.fetchone()[0]
            return rules_topic_id
