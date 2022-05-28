import requests
from json import dumps
from app.src.database import DB
from app.src.entity.user.googleUser import GoogleUser


class Classroom(object):
    def __init__(self, id, classroom_name, total_member, semester, teacher, environment, assignment_list, student_list):
        self.id = id
        self.classroom_name = classroom_name
        self.total_member = total_member
        self.semester = semester
        self.teacher = teacher
        self.environment = environment
        self.assignment_list = assignment_list
        self.student_list = student_list

    def addClassroomJson(self):
        return {
            '_id': self.id,
            'classroom_name': self.classroom_name,
            'total_member': self.total_member,
            'semester': self.semester,
            'teacher': self.teacher,
            'environment': self.environment,
            'assignment_list': self.assignment_list,
            'student_list': self.student_list
        }

    @staticmethod
    def getAllClassroom():
        cursor = DB.DATABASE['classroom'].find()
        rewardList = list(cursor)
        json_data = dumps(rewardList, indent=2)
        return json_data

    @staticmethod
    def getAllGoogleClassrooms(id):
        cursor = DB.DATABASE['user'].find({"_id": id})
        googleUser = list(cursor)
        googleUser = googleUser[0]["google_object"]
        googleUser = googleUser["user_token"]
        AllClassroomURI = "https://classroom.googleapis.com/v1/courses"
        headers = {
            "Authorization": "Bearer " + googleUser["access_token"]
        }
        response = requests.get(AllClassroomURI, headers=headers)
        if response.status_code == 400:
            auth_url = "https://accounts.google.com/o/oauth2/token"
            params = {
                "grant_type": "refresh_token",
                "client_id": GoogleUser.client_id,
                "client_secret": GoogleUser.client_secret,
                "refresh_token": googleUser["refresh_token"]
            }
            refresh_response = requests.post(auth_url, data=dict(params))
            DB.update(collection='user', id=id, data={
                "google_object.user_token.access_token": refresh_response.json()["access_token"]
            })
        response = requests.get(AllClassroomURI, headers=headers)
        data = response.json()["courses"]
        json_data = dumps(data, indent=2)
        for data in data:
            GetAllTeacherURI = "https://classroom.googleapis.com/v1/courses/{}/teachers".format(data["id"])
            GetAllStudentURI = "https://classroom.googleapis.com/v1/courses/{}/students".format(data["id"])
            teacher_response = requests.get(GetAllTeacherURI, headers=headers)
            student_response = requests.get(GetAllStudentURI, headers=headers)
            teacher_object = teacher_response.json()
            student_object = student_response.json()
            # try:
            #     if teacher_object["teachers"] and student_object["students"] is not None:
            #         Classroom(id=data["id"], classroom_name=data["name"], )
            # except:
            #     print("")
            print("////////////////////")
        return json_data

    def addGoogleClassroom(self):
        DB.insert(collection='classroom', data=self.addClassroomJson())
