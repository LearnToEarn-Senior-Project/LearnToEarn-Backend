from json import dumps

from bson import ObjectId

from app.src.database import DB


class GoogleUser(object):
    def __init__(self, access_token, firstname, lastname, email, image_url):
        self.access_token = access_token
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.image_url = image_url

    def addJson(self):
        return {
            '_id': ObjectId().__str__(),
            'access_token': self.access_token,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'image_url': self.image_url
        }

    def addGoogleUser(self):
        DB.insert(collection='google_user', data=self.addJson())

    @staticmethod
    def getGoogleUserById(id):
        cursor = DB.DATABASE['google_user'].find({"_id": "628932ad2a35ae0449d53c21"})
        googleUser = list(cursor)
        json_data = dumps(googleUser, indent=2)
        return json_data
