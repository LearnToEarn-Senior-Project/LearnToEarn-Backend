import requests
from json import dumps
from app.src.database import DB
from app.src.entity.user.googleUser import GoogleUser


class Classroom(object):

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
        if response.status_code is not 200:
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
        data = response.json()["courses"]

        for data in data:
            if not list(DB.DATABASE['classroom'].find({"_id": data["id"]})):
                GetAllTeacherURI = "https://classroom.googleapis.com/v1/courses/{}/teachers".format(data["id"])
                GetAllStudentURI = "https://classroom.googleapis.com/v1/courses/{}/students".format(data["id"])
                GetAllAssignmentURI = "https://classroom.googleapis.com/v1/courses/{}/courseWork".format(data["id"])
                teacher_response = requests.get(GetAllTeacherURI, headers=headers)
                student_response = requests.get(GetAllStudentURI, headers=headers)
                assignment_response = requests.get(GetAllAssignmentURI, headers=headers)
                try:
                    teacher_object = teacher_response.json()["teachers"]
                    student_object = student_response.json()["students"]
                    assignment_object = assignment_response.json()["courseWork"]
                except:
                    teacher_object = {}
                    student_object = {}
                    assignment_object = {}
                    pass
                if teacher_object and student_object is not None:
                    try:
                        DB.insert(collection='classroom', data={
                            '_id': data["id"],
                            'name': data["name"],
                            'total_member': student_object.__len__(),
                            'environment': "google_classroom",
                            'teacher': teacher_object,
                            'student_list': student_object,
                            'assignment_list': assignment_object,
                        })
                    except:
                        pass
            # print(student_object)
            # print(teacher_object)
            # print(assignment_object)
        cursor = DB.DATABASE['classroom'].find({})
        classroom_list = list(cursor)
        json_data = dumps(classroom_list, indent=2)
        print(json_data)
        return json_data
