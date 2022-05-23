from json import dumps

from bson import ObjectId

from app.src.database import DB


class Assignment(object):
    def __init__(self, assignment_name, due_date, status):
        self.assignment_name = assignment_name
        self.due_date = due_date
        self.status = status

    @staticmethod
    def getAllAssignments():
        cursor = DB.DATABASE['assignment'].find()
        assignmentList = list(cursor)
        json_data = dumps(assignmentList, indent=2)
        return json_data
