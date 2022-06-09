from app.src.database import DB
from oauth2client import client


class GoogleUser(object):
    client_id = "726873603726-tq3t7s31jodv5qcu335dpn8beln6oise.apps.googleusercontent.com"
    client_secret = "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"
    user_token = None
    firstname = None
    lastname = None
    email = None
    image_url = None

    @staticmethod
    def bindGoogleAccount(id, authCode):
        auth_code = authCode
        scope = "profile " \
                "email " \
                "https://www.googleapis.com/auth/classroom.student-submissions.students.readonly " \
                "https://www.googleapis.com/auth/classroom.student-submissions.me.readonly " \
                "https://www.googleapis.com/auth/classroom.courses.readonly " \
                "https://www.googleapis.com/auth/classroom.rosters.readonly"
        credentials = client.credentials_from_code(GoogleUser.client_id, GoogleUser.client_secret, scope, auth_code)
        GoogleUser.user_token = {
            "access_token": credentials.access_token,
            "refresh_token": credentials.refresh_token
        }
        googleData = credentials.id_token
        GoogleUser.firstname = googleData["given_name"]
        GoogleUser.lastname = googleData["family_name"]
        GoogleUser.email = googleData["email"]
        GoogleUser.image_url = googleData["picture"]
        DB.update(collection='user', id=id, data={"google_object": {
            '_id': googleData["sub"],
            'user_token': GoogleUser.user_token,
            'firstname': GoogleUser.firstname,
            'lastname': GoogleUser.lastname,
            'email': GoogleUser.email,
            'image_url': GoogleUser.image_url
        }})
        googleUser = list(DB.DATABASE['user'].find({"_id": id}).limit(1))[0]["google_object"]
        return googleUser

    @staticmethod
    def unbindGoogleAccount(id):
        DB.update(collection='user', id=id, data={"google_object": None})

    @staticmethod
    def getUserGoogleData(id):
        googleUser = list(DB.DATABASE['user'].find({"_id": id}).limit(1))[0]["google_object"]
        if googleUser is not None:
            del googleUser["_id"]
            del googleUser["user_token"]
        return googleUser
