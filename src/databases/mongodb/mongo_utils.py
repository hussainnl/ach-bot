from databases.mongodb.mongo_config import Config
from pymongo import MongoClient
from datetime import datetime
from zoneinfo import ZoneInfo
import os
import logging

db_name = os.getenv("MONGO_NAME")

class DatabaseHandler:

    def __init__(self) :
        self.config = Config().data
        self.client = MongoClient(**self.config)
        self.db = self.client[db_name]


    def create_new_collection(self,collection_name) -> None:
        """To create a new collection in the database"""
        database = self.db
        try:
            database.create_collection(collection_name)
        except Exception as e:
            logging.info(f"Error creating collection {collection_name}: {e}")
        self.save_current_collection_name(collection_name)

    def save_current_collection_name(self,collection_name) -> None:
        """To save the name of the current collection for the new weekly report"""
        database = self.db
        database["current_collection"].update_one(
        {"_id": "weekly_collection"},
        {"$set": {"name": collection_name}},
        upsert=True
        )

    def get_current_collection_name(self) -> str:
        """To get the name of the current collection for the new weekly report"""
        database = self.db
        try:
            doc = database["current_collection"].find_one({"_id": "weekly_collection"})
            return doc["name"]
        except:
            logging.info(f"doc['name']: NoneType")
            now = datetime.now(ZoneInfo("Africa/Cairo"))
            datetime_now = f"{now.year}-{now.month:02d}-{now.day:02d}"
            collection_name = f"weekly_report:{datetime_now}"
            logging.info(f"Current collection name: {collection_name}")
            self.create_new_collection(collection_name)
            return collection_name

         