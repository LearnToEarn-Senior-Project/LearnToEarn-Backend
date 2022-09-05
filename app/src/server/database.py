from pymongo import MongoClient


class DB(object):
    URI = "mongodb+srv://LearnToEarn:LearnToEarn2022@lte-backend.8tudrjt.mongodb.net"

    client = MongoClient(URI)
    DATABASE = client['learn-to-earn']

    @staticmethod
    def insert(collection, data):
        DB.DATABASE[collection].insert_one(data)

    @staticmethod
    def update(collection, id, data):
        DB.DATABASE[collection].update_one({"_id": str(id)}, {"$set": data})

    @staticmethod
    def upsert(collection, id, data):
        DB.DATABASE[collection].update_one({"_id": str(id)}, {"$set": data}, upsert=True)

    @staticmethod
    def delete(collection, data):
        DB.DATABASE[collection].delete_one({"_id": data})
