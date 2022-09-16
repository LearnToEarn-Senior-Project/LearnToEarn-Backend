from app.src.object.user.GoogleUser.entity.GoogleUser import GoogleUserDAO
from app.src.server.database import DB
from oauth2client import client
from app.src.resources import Google


class GoogleUserServices:

    @staticmethod
    def bindAccount(user_id, auth_code):
        try:
            scope = ["https://www.googleapis.com/auth/classroom.student-submissions.students.readonly",
                     "https://www.googleapis.com/auth/classroom.student-submissions.me.readonly",
                     "https://www.googleapis.com/auth/classroom.courses.readonly",
                     "https://www.googleapis.com/auth/classroom.rosters.readonly"]
            credentials = client.credentials_from_code(client_id=Google.client_id,
                                                       client_secret=Google.client_secret,
                                                       scope=scope,
                                                       code=auth_code)
            user_token = {
                "access_token": credentials.access_token,
                "refresh_token": credentials.refresh_token
            }
            googleData = credentials.id_token
            googleObject = GoogleUserDAO(googleData["sub"], user_token, googleData["given_name"],
                                         googleData["family_name"],
                                         googleData["email"], googleData["picture"])
            DB.update(collection='user', id=user_id, data={"google_object": {
                '_id': googleObject.id,
                'user_token': googleObject.user_token,
                'firstname': googleObject.firstname,
                'lastname': googleObject.lastname,
                'email': googleObject.email,
                'image_url': googleObject.image_url
            }})
            return list(DB.DATABASE['user'].find({"_id": user_id}, {"google_object": True, "_id": False}).limit(1))[0][
                "google_object"]
        except:
            return "The user is not found or got some error"

    @staticmethod
    def unbindAccount(user_id):
        try:
            DB.update(collection='user', id=user_id, data={"google_object": None})
            return "Unbind success"
        except:
            return "The user is not found or got some error"

    @staticmethod
    def get(user_id):
        try:
            Google.GoogleCredential(user_id)
            googleUser = list(DB.DATABASE['user'].find({"_id": user_id}, {"user_token": False}).limit(1))[0][
                "google_object"]
            return googleUser
        except:
            return "The user is not found or got some error"
