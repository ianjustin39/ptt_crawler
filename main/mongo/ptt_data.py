from main.mongo.mongo_conn import MongoConn
import os


class PttData(MongoConn):

    def __init__(self):
        super(PttData, self).__init__(os.getenv("MONGO_COL"))

    def select(self, _id):
        query = {'_id': _id}
        result = self.col.find_one(query)
        return result

    def insert(self, data):
        self.col.insert_one(data)

    def close(self):
        self.mongo_conn.close()
