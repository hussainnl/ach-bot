from databases.mongodb.mongo_config import Config
from databases.mongodb.mongo_utils import DatabaseHandler as DH
from pymongo import MongoClient
from datetime import datetime
from zoneinfo import ZoneInfo
import os

db_name = os.getenv("MONGO_NAME")

class AchReport:
    def __init__(self) :
        self.config = Config().data
        self.client = MongoClient(**self.config)
        self.db = self.client[db_name]
        self.weekly_ach = "لم تقم بإنجازات الأسبوعية في هذا الجروب"


    def get_user_raw_report(self,user_id,group_id) -> str:
        """To get the user report for the weekly report"""
        database = self.db
        collection_name = DH().get_current_collection_name()
        raw_report = database[collection_name].find_one({"user_id": user_id, "group_id": group_id})
        return raw_report
           
    def save_study_ach(self,user_id,group_id,group_name,text,score) -> None:
        """To save the user achievment study message for the weekly report"""
        database = self.db
        collection_name = DH().get_current_collection_name()
        if self.is_user_doc_exist(user_id,group_id) :
                database[collection_name].update_one(
                {"user_id" : user_id,
                "group_id" : group_id,         
                },
                {"$push": {"study_ach": text},"$inc":  {"user_score": score}}
                )
        else :
            database[collection_name].insert_one(
            {"user_id" : user_id,
            "group_id" : group_id,
            "group_name" : group_name,                
            "study_ach": [text],
            "weekly_ach": self.weekly_ach,
            "user_score": score,
            "timestamp": datetime.now(ZoneInfo("Africa/Cairo"))
             })
          
    def is_user_doc_exist(self,user_id,group_id) -> bool :
        """To check if the user document exist in the database or not"""
        database = self.db
        collection_name = DH().get_current_collection_name()
        doc = database[collection_name].find_one({"user_id": user_id, "group_id": group_id})
        return doc is not None

    def save_weekly_ach(self,user_id,group_id,text,score)-> None:
        """To save the user weekly ach message for the weekly report"""
        database = self.db
        collection_name = DH().get_current_collection_name()
        database[collection_name].update_one(
        {"user_id" : user_id,
        "group_id" : group_id,
         },
         {"$set": {"weekly_ach": text},"$inc":{"user_score": score}}
        )




           
