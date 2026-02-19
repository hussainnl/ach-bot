import os



class Config :
    
    def __init__(self):
        self.data = {
        "host": os.getenv("MONGO_HOST"),
        "username": os.getenv("MONGO_USER"),
        "password": os.getenv("MONGO_PASSWORD")}   