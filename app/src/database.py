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
        DB.DATABASE[collection].update_one({"_id": str(id)}, {"$set": data})

    @staticmethod
    def delete(collection, data):
        DB.DATABASE[collection].delete_one({"_id": data})
