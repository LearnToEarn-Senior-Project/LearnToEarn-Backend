from pymongo import MongoClient


class DB(object):
    URI = "mongodb://127.0.0.1:27017"

    client = MongoClient(URI)
    DATABASE = client['learn-to-earn']

    @staticmethod
    def insert(collection, data):
        DB.DATABASE[collection].insert_one(data)

    @staticmethod
    def update(collection, id, data):
        DB.filter = {"_id": str(id)}
        DB.newValues = {"$set": data}
        DB.DATABASE[collection].update_one(DB.filter, DB.newValues)

    @staticmethod
    def delete(collection, data):
        myquery = {"_id": data}
        DB.DATABASE[collection].delete_one(myquery)
