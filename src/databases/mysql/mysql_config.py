import os



class Config :
    
    def __init__(self):
        self.data = {
        "host": os.getenv("MYSQL_HOST"),
        "user": os.getenv("MYSQL_USER"),
        "password": os.getenv("MYSQL_PASSWORD"),
        "database": os.getenv("MYSQL_NAME"),
        "charset": os.getenv("MYSQL_CHARSET")}   