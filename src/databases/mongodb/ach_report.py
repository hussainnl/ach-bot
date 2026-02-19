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
        collection_name = self.get_current_collection_name()
        if self.is_user_doc_exist(user_id,group_id) :
                database[f"ach_messages{collection_name}"].update_one(
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

    def save_weekly_ach(self,user_id,group_id,text,score)-> None:
        """To save the user weekly ach message for the weekly report"""
        database = self.db
        collection_name = self.get_current_collection_name()
        database[collection_name].update_one(
        {"user_id" : user_id,
        "group_id" : group_id,
         },
         {"$set": {"weekly_ach": text},"$inc":{"user_score": score}}
        )

    def create_new_collection(self,collection_name) -> None:
        """To create a new collection in the database"""
        database = self.db
        database.create_collection(collection_name)
        self.save_crunt_collection_name(collection_name)

    def save_crunt_collection_name(self,collection_name) -> None:
        """To save the name of the current collection for the new weekly report"""
        database = self.db
        database["current_collection"].update_one(
        {"name": "current_collection"},
        {"$set": {"name": collection_name}},
        upsert=True
        )
    def get_current_collection_name(self) -> str:
        """To get the name of the current collection for the new weekly report"""
        database = self.db
        doc = database["current_collection"].find_one({})
        return doc["name"]
