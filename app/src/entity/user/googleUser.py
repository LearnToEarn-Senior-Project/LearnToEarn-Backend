from json import dumps

from bson import ObjectId

from app.src.database import DB


class GoogleUser(object):
    def __init__(self, id, access_token, firstname, lastname, email, image_url):
        self.id = id
        self.access_token = access_token
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.image_url = image_url

    def addGoogleJson(self):
        return {
            '_id': ObjectId().__str__(),
            'access_token': self.access_token,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'image_url': self.image_url
        }

    @staticmethod
    def unbindGoogleAccount(id):
        DB.update(collection='user', id=id, data={"google_object": None})

    def bindGoogleAccount(self):
        DB.update(collection='user', id=self.id, data={"google_object": self.addGoogleJson()})

    @staticmethod
    def getUserGoogleData(id):
        cursor = DB.DATABASE['user'].find({"_id": id})
        googleUser = list(cursor)
        googleUser = googleUser[0]["google_object"]
        if googleUser is not None:
            del googleUser["_id"]
            del googleUser["access_token"]
        json_data = dumps(googleUser, indent=2)
        return json_data
