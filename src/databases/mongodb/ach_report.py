from databases.mongodb.mongo_config import Config
from pymongo import MongoClient
import os
import datetime
db_name = os.getenv("MONGO_NAME")
class AchReport:
    def __init__(self):
        self.config = Config().data
        self.client = MongoClient(**self.config)
        self.db = self.client[self.client[db_name]]
        self.weekly_ach = "لم تقم بإنجازات الأسبوعية في هذا الجروب"

        
    def save_study_ach(self,user_id,group_id,group_name,text):
        """To save the user achievment study message for the weekly report"""
        database = self.db
        database[f"ach_messages{""}"].update_one(
        {"user_id" : user_id,
        "group_id" : group_id,
        "group_name" : group_name,                
        "study_ach": [],
        "weekly_ach": self.weekly_ach,
        "timestamp": datetime.datetime.now(datetime.timezone.utc)
         },
         {"$push": {"messages": text}},
         upsert=True
        )  
    def save_weekly_ach(self,user_id,group_id,text):
        """To save the user weekly ach message for the weekly report"""
        database = self.db
        database[f"ach_messages{""}"].update_one(
        {"user_id" : user_id,
        "group_id" : group_id,
         },
         {"$set": {"weekly_ach": text}}
        )
