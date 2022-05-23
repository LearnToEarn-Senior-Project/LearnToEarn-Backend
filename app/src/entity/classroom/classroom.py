from json import dumps

from bson import ObjectId

from app.src.database import DB


class Classroom(object):
    def __init__(self, classroom_name, total_member, semester, teacher, environment, assignment_list, student_list):
        self.classroom_name = classroom_name
        self.total_member = total_member
        self.semester = semester
        self.teacher = teacher
        self.environment = environment
        self.assignment_list = assignment_list
        self.student_list = student_list

    def addJson(self):
        return {
            '_id': ObjectId().__str__(),
            'classroom_name': self.classroom_name,
            'total_member': self.total_member,
            'semester': self.semester,
            'teacher': self.teacher,
            'environment': self.environment,
            'assignment_list': self.assignment_list,
            'student_list': self.student_list
        }

    @staticmethod
    def getAllRewards():
        cursor = DB.DATABASE['classroom'].find()
        rewardList = list(cursor)
        json_data = dumps(rewardList, indent=2)
        return json_data

    def addReward(self):
        DB.insert(collection='classroom', data=self.addJson())
