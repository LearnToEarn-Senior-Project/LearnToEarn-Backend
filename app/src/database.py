import pymongo
from bson.objectid import ObjectId

class DB(object):
    URI = "mongodb://127.0.0.1:27017"

    client = pymongo.MongoClient(URI)
    DATABASE = client['learn-to-earn']

    @staticmethod
    def insert(collection, data):
        DB.DATABASE[collection].insert_one(data)

    @staticmethod
    def update(collection, id, data):
        DB.filter = {'_id': id}
        DB.newValues = {"$set": data}
        DB.DATABASE[collection].update_one(DB.filter, DB.newValues)

    @staticmethod
    def delete(collection, data):
        myquery = {"_id": str(data)}
        DB.DATABASE[collection].delete_one(myquery)
