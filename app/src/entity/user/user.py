from json import dumps

from bson import ObjectId

from app.src.database import DB


class User(object):
    def __init__(self, firstname, lastname, email, googleObject, role):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.googleObject = googleObject
        self.role = role

    def addJson(self):
        return {
            '_id': ObjectId().__str__(),
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'google_object': self.googleObject,
            'role': self.role
        }
    # def bindGoogleAccount(self):
