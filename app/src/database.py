import pymongo


class DB(object):
    URI = "mongodb://127.0.0.1:27017"

    @staticmethod
    def init():
        client = pymongo.MongoClient(DB.URI)
        DB.DATABASE = client['rest-gen']


@staticmethod
def insert(collection, data):
    DB.DATABASE[collection].insert(data)