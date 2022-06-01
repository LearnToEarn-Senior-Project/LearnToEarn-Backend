from json import dumps

import requests
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
        response = requests.post(URI, data=dict(request_body), headers=headers)
        return response.json()

    @staticmethod
    def getCredentials(token):
        URI = "https://misapi.cmu.ac.th/cmuitaccount/v1/api/cmuitaccount/basicinfo"
        headers = {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "Authorization": "Bearer " + token,
        }
        response = requests.get(URI, headers=headers)
        return response.json()

    def addUser(self):
        DB.insert(collection='user', data={
            '_id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'google_object': self.googleObject,
            'role': self.role
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
        json_data = dumps(cmuUser, indent=2)
        return json_data
