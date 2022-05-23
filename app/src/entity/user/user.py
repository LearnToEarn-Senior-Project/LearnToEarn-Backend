from json import dumps

from bson import ObjectId

from app.src.database import DB


class User(object):
    def __init__(self, firstname, lastname, email, google_token, role):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.google_token = google_token
        self.role = role

    def addJson(self):
        return {
            '_id': ObjectId().__str__(),
            'firstname': self.reward_name,
            'lastname': self.detail,
            'email': self.amount,
            'google_token': self.price,
            'role': self.image
        }

    @staticmethod
    def getAllRewards():
        cursor = DB.DATABASE['user'].find()
        rewardList = list(cursor)
        json_data = dumps(rewardList, indent=2)
        return json_data

    def addReward(self):
        DB.insert(collection='user', data=self.addJson())
