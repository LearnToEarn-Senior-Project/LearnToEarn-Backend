from app.src.database import DB


class Assignment(object):
    def __init__(self, assignment_name, due_date, status):
        self.assignment_name = assignment_name
        self.due_date = due_date
        self.status = status

    @staticmethod
    def getAllAssignments():
        assignmentList = list(DB.DATABASE['assignment'].find())
        return assignmentList
