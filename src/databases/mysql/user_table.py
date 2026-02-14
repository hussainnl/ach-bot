import pymysql
from databases.mysql.config_db import Config
import logging

class User :

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
                        user_info(user_id BIGINT NOT NULL ,
                        group_id  BIGINT NOT NULL,
                        user_name VARCHAR(128) NOT NULL,
                        score INT
                        DEFAULT 0,
                        missed TINYINT(5)
                        DEFAULT 1 ,
                        is_subscribed  TINYINT(1)
                        DEFAULT 0,
                        mode TINYINT(1)
                        DEFAULT 0,
                        PRIMARY KEY (user_id),
                        UNIQUE INDEX  unq_username (user_name) ,
                        INDEX  idx_sorce (score),
                        INDEX  idx_missed (missed),
                        CONSTRAINT fk_group_id
                            FOREIGN KEY (group_id)
                            REFERENCES group_info (group_id)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE)""")   
            self.con.commit()
            
    def add_user(self,group_id,user_id,user_name):
        """To add a new user to the database"""
        logging.info(f"start add_user")
        try:
            with self.con.cursor() as cur:
                cur.execute("""INSERT INTO user_info(user_id,group_id, user_name)
                            VALUES(%s, %s, %s)""", (user_id, group_id,user_name))
                self.con.commit()
            logging.info(f"add_user done")
        except:
            logging.info(f"the user is alread there")

    def delete_user(self,group_id,user_id):
        """To delete a  user to the database"""
        with self.con.cursor() as cur:
            cur.execute("DELETE FROM user_info WHERE user_id = %s AND group_id = %s", (user_id,group_id)) 
            self.con.commit()      

    def is_user_a_member(self,user_id):
        """To check the userid if it in our groups for start command"""
        with self.con.cursor() as cur:
            cur.execute("SELECT group_id FROM user_info WHERE  user_id = ? ",(user_id,))
            user_groups = []
            for id in cur.fetchall():
                id[0]    
                user_groups.append(id[0]) 
            return user_groups
    
    def update_user_score(self,user_id, group_id,points):
        """To update the user achievement score"""
        with self.con.cursor() as cur:
            cur.execute("SELECT score FROM user_info WHERE user_id = %s AND group_id = %s", (user_id,group_id))
            score = cur.fetchone()[0]
            new_score = score + points 
            cur.execute("""
            UPDATE user_info
            SET score = %s
            WHERE user_id = %s AND group_id = %s
            """, (new_score, user_id, group_id))
            self.con.commit()


    def get_user_score(self,user_id,group_id):
        """To get the user achievement score"""
        with self.con.cursor() as cur:
            cur.execute("SELECT score FROM user_info WHERE user_id = %s AND group_id = %s", (user_id,group_id))       
            score = cur.fetchone()[0]
            return score
        
    def get_user_missed(self,user_id,group_id):
        """To get the user missed"""
        with self.con.cursor() as cur:
            cur.execute("SELECT missed FROM user_info WHERE user_id = %s AND group_id = %s", (user_id,group_id))       
            missed = cur.fetchone()[0]
            return missed
        
    def update_user_missed(self,user_id,group_id):
        """To update the user missed"""
        with self.con.cursor() as cur:
            new_missed = 0
            cur.execute("""
            UPDATE user_info
            SET missed = %s
            WHERE user_id = %s AND group_id = %s
            """, (new_missed, user_id, group_id))
            self.con.commit()


    def weekly_missed_update(self,group_id):
        """To beggin a new week"""

        with self.con.cursor() as cur:
            users_id = self.get_users_list(group_id)
            for user_id in users_id:
                user_missed = self.get_user_missed(user_id,group_id)
                new_missed = user_missed + 1
                cur.execute("""
                UPDATE user_info
                SET missed = %s
                WHERE user_id = %s AND group_id = %s
                """, (new_missed,user_id,group_id))
                self.con.commit()

    def get_users_list(self,group_id):
        """To get users list"""
        with self.con.cursor() as cur:
            cur.execute("SELECT  user_id FROM user_info WHERE group_id = %s", (group_id,))
            users_id =[ id[0] for id in cur.fetchall()]
            return users_id
                   
    def get_ban_users(self,group_id):
        """To get users to be banned"""
        with self.con.cursor() as cur:
            cur.execute("""SELECT user_id FROM user_info 
                        WHERE group_id = %s AND (
                        ( mode = 1 AND missed > 2 )  
                        OR missed > 4 )""", (group_id,))
            banned_ids =[ id[0] for id in cur.fetchall()]
            return banned_ids
        

    def update_user_subscription(self, user_id, group_id,sub_state):
        """To update the user subscription"""
        with self.con.cursor() as cur:
            sub_state = 0
            cur.execute("""
            UPDATE user_info
            SET is_subscribed = %s
            WHERE user_id = %s AND group_id = %s
            """, (sub_state, user_id, group_id))
            self.con.commit()

    def get_subscription_users(self):
        """To get subscription users"""
        with self.con.cursor() as cur:
            cur.execute("SELECT user_id FROM user_info WHERE is_subscribed = 1")
            subscription_users =[ id[0] for id in cur.fetchall()]
            return subscription_users
        
    def get_user_mode(self,user_id,group_id):
        """To get the user mode"""
        with self.con.cursor() as cur:
            cur.execute("SELECT mode FROM user_info WHERE user_id = %s AND group_id = %s", (user_id,group_id))       
            user_mode = cur.fetchone()[0]
            return user_mode
        
    def update_user_mode(self, user_id, group_id,new_mode):
        """To update the user mode"""
        with self.con.cursor() as cur:
            cur.execute("""
            UPDATE user_info
            SET mode = %s
            WHERE user_id = %s AND group_id = %s
            """, (new_mode, user_id, group_id))
            self.con.commit()
