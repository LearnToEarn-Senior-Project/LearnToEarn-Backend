from requests import post, get

from app.src.resources import CMU
from app.src.object.user.CMUUser.entity.CMUUser import CMUUser
from app.src.server.database import DB


class CMUUserServices:

    @staticmethod
    def getAccessToken(code):
        URI = "https://oauth.cmu.ac.th/v1/GetToken.aspx"
        request_body = {
            "code": code,
            "redirect_uri": "http:/localhost:3000/redirect",
            "client_id": CMU.client_id,
            "client_secret": CMU.client_secret,
            "grant_type": "authorization_code"
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = post(URI, data=dict(request_body), headers=headers)
        return dict(response.json())

    @staticmethod
    def getCredentials(token):
        URI = "https://misapi.cmu.ac.th/cmuitaccount/v1/api/cmuitaccount/basicinfo"
        headers = {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "Authorization": "Bearer " + token,
        }
        response = get(URI, headers=headers)
        return dict(response.json())

    @staticmethod
    def add(id, firstname, lastname, email, google_object, role):
        cmuUser = CMUUser(id, firstname, lastname, email, google_object, role)
        if role == "teacher":
            DB.insert(collection='user', data={
                '_id': cmuUser.id,
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
                'current_token': 0
            })
        return CMUUserServices.get(cmuUser.id)

    @staticmethod
    def get(id):
        cmuUser = list(DB.DATABASE['user'].find({"_id": id}).limit(1))
        try:
            del cmuUser[0]["google_object"]
            del cmuUser[0]["current_token"]
            del cmuUser[0]["role"]
        except:
            pass
        return cmuUser

    @staticmethod
    def getRole(id):
        return list(DB.DATABASE['user'].find({"_id": id}).limit(1))[0].get("role")

    @staticmethod
    def swapRole(id):
        data = list(DB.DATABASE['user'].find({"_id": id}).limit(1))[0]
        array = list(DB.DATABASE['user'].find({"_id": id}).limit(1))[0].get("role")
        tmp = array[0]
        array[0] = array[1]
        array[1] = tmp
        DB.update(collection='user', id=id, data={
            '_id': id,
            'firstname': data.get("firstname"),
            'lastname': data.get("lastname"),
            'email': data.get("email"),
            'google_object': data.get("google_object"),
            'role': array,
            'current_token': data.get("current_token")
        })
        return array
