from app.src.object.user.GoogleUser.entity.GoogleUser import GoogleUser
from app.src.server.database import DB
from oauth2client import client
from app.src.resources import Google


class GoogleUserServices:

    @staticmethod
    def bindAccount(id, authCode):
        auth_code = authCode
        scope = "profile " \
                "email " \
                "https://www.googleapis.com/auth/classroom.student-submissions.students.readonly " \
                "https://www.googleapis.com/auth/classroom.student-submissions.me.readonly " \
                "https://www.googleapis.com/auth/classroom.courses.readonly " \
                "https://www.googleapis.com/auth/classroom.rosters.readonly"
        credentials = client.credentials_from_code(Google.client_id, Google.client_secret, scope, auth_code)
        user_token = {
            "access_token": credentials.access_token,
            "refresh_token": credentials.refresh_token
        }
        googleData = credentials.id_token
        googleObject = GoogleUser(googleData["sub"], user_token, googleData["given_name"], googleData["family_name"],
                                  googleData["email"], googleData["picture"])
        DB.update(collection='user', id=id, data={"google_object": {
            '_id': googleObject.id,
            'user_token': googleObject.user_token,
            'firstname': googleObject.firstname,
            'lastname': googleObject.lastname,
            'email': googleObject.email,
            'image_url': googleObject.image_url
        }})
        googleUser = list(DB.DATABASE['user'].find({"_id": id}).limit(1))[0]["google_object"]
        return googleUser

    @staticmethod
    def unbindAccount(id):
        DB.update(collection='user', id=id, data={"google_object": None})
        return "Unbind success"

    @staticmethod
    def get(id):
        googleUser = list(DB.DATABASE['user'].find({"_id": id}).limit(1))[0]["google_object"]
        if googleUser is not None:
            del googleUser["_id"]
            del googleUser["user_token"]
        return googleUser
