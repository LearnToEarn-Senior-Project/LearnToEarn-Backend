from bson import ObjectId
from requests import get, post
from app.src.database import DB


class User(object):
    def __init__(self, id, firstname, lastname, email, googleObject, role):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.googleObject = googleObject
        self.role = role

    @staticmethod
    def getAccessToken(code):
        client_id = "DfQ7tTs1Qua9Jktfz5UupXN3uvZHsD1HUtYq617r"
        client_secret = "RsZ34h0zGHg446tSDWQ83UJkCDsrxdjJ7CQ78U9m"
        URI = "https://oauth.cmu.ac.th/v1/GetToken.aspx"
        request_body = {
            "code": code,
            "redirect_uri": "http:/localhost:3000/redirect",
            "client_id": client_id,
            "client_secret": client_secret,
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

    def addUser(self):
        if self.role is "teacher":
            DB.insert(collection='user', data={
                '_id': ObjectId().__str__(),
                'firstname': self.firstname,
                'lastname': self.lastname,
                'email': self.email,
                'google_object': self.googleObject,
                'role': ["teacher"],
            })
        else:
            DB.insert(collection='user', data={
                '_id': self.id,
                'firstname': self.firstname,
                'lastname': self.lastname,
                'email': self.email,
                'google_object': self.googleObject,
                'role': ["student"],
                'current_token': 0
            })
        return self.getUser(self.id)

    @staticmethod
    def getUser(id):
        cursor = DB.DATABASE['user'].find({"_id": id})
        cmuUser = list(cursor)
        try:
            del cmuUser[0]["google_object"]
        except:
            pass
        return cmuUser
