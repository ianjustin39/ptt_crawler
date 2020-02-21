import pymongo
import os
from dotenv import load_dotenv
load_dotenv()


class MongoConn:

    def __init__(self, collection):
        username = os.getenv("MONGO_USERNAME")
        password = os.getenv("MONGO_PWD")
        database = os.getenv("MONGO_DB")

        self.mongo_conn = pymongo.MongoClient(os.getenv("MONGO_HOST"), username=username, password=password)
        self.db = self.mongo_conn[database]
        self.col = self.db[collection]
