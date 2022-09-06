from requests import post, get
from bson import ObjectId
from app.src.resources import CMU
from app.src.object.user.CMUUser.entity.CMUUser import CMUUserDAO
from app.src.server.database import DB


class CMUUserServices:

    @staticmethod
    def getAccessToken(code):
        response = post(url="https://oauth.cmu.ac.th/v1/GetToken.aspx", data=dict({
            "code": code,
            "redirect_uri": "https://learntoearn-se-cmu2022.web.app/redirect",
            "client_id": CMU.client_id,
            "client_secret": CMU.client_secret,
            "grant_type": "authorization_code"
        }), headers={'Content-Type': 'application/x-www-form-urlencoded'})
        return dict(response.json())

    @staticmethod
    def getCredentials(token):
        response = get(url="https://misapi.cmu.ac.th/cmuitaccount/v1/api/cmuitaccount/basicinfo", headers={
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "Authorization": "Bearer " + token,
        })
        return dict(response.json())

    @staticmethod
    def add(user_id, firstname, lastname, email, role):
        try:
            cmuUser = CMUUserDAO(user_id, firstname, lastname, email, None, role)
            if user_id and firstname and lastname and email and role is not None:
                if role == "teacher":
                    id = ObjectId().__str__()
                    DB.insert(collection='user', data={
                        '_id': id,
                        'firstname': cmuUser.firstname,
                        'lastname': cmuUser.lastname,
                        'email': cmuUser.email,
                        'google_object': cmuUser.google_object,
                        'role': ["teacher"],
                    })
                else:
                    DB.insert(collection='user', data={
                        '_id': cmuUser.id,
                        'firstname': cmuUser.firstname,
                        'lastname': cmuUser.lastname,
                        'email': cmuUser.email,
                        'google_object': cmuUser.google_object,
                        'role': ["student"],
                        'current_token': float(0)
                    })
                return CMUUserServices.get(cmuUser.id)
            else:
                return "Cannot add the user because the data is not complete"
        except:
            return "Cannot add the user because the error is found during operation"

    @staticmethod
    def get(user_id):
        try:
            cmuUser = list(DB.DATABASE['user'].find({"_id": user_id}, {"google_object": False, "current_token": False,
                                                                       "role": False}).limit(1))
            return cmuUser[0]
        except:
            return "User not found"

    @staticmethod
    def getRole(user_id):
        try:
            return list(DB.DATABASE['user'].find({"_id": user_id}, {"role": True, "_id": False}).limit(1))[0]["role"]
        except:
            return "User not found"

    @staticmethod
    def swapRole(user_id):
        try:
            data = list(DB.DATABASE['user'].find({"_id": user_id}).limit(1))[0]
            array = list(DB.DATABASE['user'].find({"_id": user_id}, {"role": True, "_id": False}).limit(1))[0]["role"]
            tmp = array[0]
            array[0] = array[1]
            array[1] = tmp
            DB.update(collection='user', id=user_id, data={
                '_id': user_id,
                'firstname': data.get("firstname"),
                'lastname': data.get("lastname"),
                'email': data.get("email"),
                'google_object': data.get("google_object"),
                'role': array,
                'current_token': data.get("current_token")
            })
            return array
        except:
            return "User not found or The user must contain more than one role"
