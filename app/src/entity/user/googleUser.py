from json import dumps
from bson import ObjectId
from app.src.database import DB
# from oauth2client import client


class GoogleUser(object):
    user_token = None
    client_id = "726873603726-tq3t7s31jodv5qcu335dpn8beln6oise.apps.googleusercontent.com"
    client_secret = "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"

    def __init__(self, id, firstname, lastname, email, image_url):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.image_url = image_url

    def addGoogleJson(self):
        return {
            '_id': ObjectId().__str__(),
            'user_token': GoogleUser.user_token,
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
            del googleUser["user_token"]
        json_data = dumps(googleUser, indent=2)
        return json_data

    # @staticmethod
    # def getToken(authCode):
    #     auth_code = authCode
    #     scope = "profile " \
    #             "email " \
    #             "https://www.googleapis.com/auth/classroom.student-submissions.students.readonly " \
    #             "https://www.googleapis.com/auth/classroom.student-submissions.me.readonly " \
    #             "https://www.googleapis.com/auth/classroom.courses.readonly " \
    #             "https://www.googleapis.com/auth/classroom.rosters.readonly"
    #     credentials = client.credentials_from_code(GoogleUser.client_id, GoogleUser.client_secret, scope, auth_code)
    #     GoogleUser.user_token = {
    #         "access_token": credentials.access_token,
    #         "refresh_token": credentials.refresh_token
    #     }
    #     return GoogleUser.user_token
