from databases.mongodb.mongo_config import Config
from pymongo import MongoClient
import os
import datetime
db_name = os.getenv("MONGO_NAME")
class AchReport:
    def __init__(self) :
        self.config = Config().data
        self.client = MongoClient(**self.config)
        self.db = self.client[db_name]
        self.weekly_ach = "لم تقم بإنجازات الأسبوعية في هذا الجروب"


    def save_study_ach(self,user_id,group_id,group_name,text,score) -> None:
        """To save the user achievment study message for the weekly report"""
        database = self.db

        if self.is_user_doc_exist(user_id,group_id) :
                database[f"ach_messages{""}"].update_one(
                {"user_id" : user_id,
                "group_id" : group_id,         
                },
                {"$push": {"study_ach": text},"$inc":  {"user_score": score}}
                )
        else :
            database[f"ach_messages{""}"].insert_one(
            {"user_id" : user_id,
            "group_id" : group_id,
            "group_name" : group_name,                
            "study_ach": [],
            "weekly_ach": self.weekly_ach,
            "user_score": 0,
            "timestamp": datetime.datetime.now(datetime.timezone.utc)
             })
          
    def is_user_doc_exist(self,user_id,group_id) -> bool :
        """To check if the user document exist in the database or not"""
        database = self.db
        doc = database[f"ach_messages{""}"].find_one({"user_id": user_id, "group_id": group_id})
        return doc is not None

    def save_weekly_ach(self,user_id,group_id,text)-> None:
        """To save the user weekly ach message for the weekly report"""
        database = self.db
        database[f"ach_messages{""}"].update_one(
        {"user_id" : user_id,
        "group_id" : group_id,
         },
         {"$set": {"weekly_ach": text}}
        )
