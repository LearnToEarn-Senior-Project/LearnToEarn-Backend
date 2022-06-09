from app.src.database import DB
from app.src.entity.user.googleUser import GoogleUser
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


class Classroom(object):
    @staticmethod
    def getAllClassrooms():
        classroomList = list(DB.DATABASE['classroom'].find())
        return classroomList

    @staticmethod
    def getAllGoogleClassrooms(id):
        googleUser = list(DB.DATABASE['user'].find({"_id": id}).limit(1))[0]["google_object"]["user_token"]
        creds = Credentials.from_authorized_user_info({
            "client_id": GoogleUser.client_id,
            "client_secret": GoogleUser.client_secret,
            "refresh_token": googleUser["refresh_token"]
        })
        service = build('classroom', 'v1', credentials=creds)
        response = service.courses().list().execute()
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            DB.update(collection='user', id=id, data={
                "google_object.user_token.access_token": creds.__getstate__().get("token")
            })
            response = service.courses().list().execute()
        try:
            for data in response.get("courses"):
                if not list(DB.DATABASE['classroom'].find({"_id": data.get("id")}).limit(1)):
                    teacher_object = service.courses().teachers().get(courseId=data.get("id"),
                                                                      userId=data.get("ownerId")).execute()
                    teacher_object = {"teacher_id": teacher_object.get("userId"),
                                      "teacher_name": teacher_object.get("profile").get("name").get("fullName")}

                    student_object = service.courses().students().list(courseId=data.get("id")).execute().get(
                        "students")
                    student_object = [{"student_id": student.get("userId"),
                                       "student_name": student.get("profile").get("name").get("fullName")} for student
                                      in
                                      student_object]
                    assignment_object = service.courses().courseWork().list(courseId=data.get("id")).execute().get(
                        "courseWork")

                    for assignment in assignment_object:
                        assignment_object_history = service.courses().courseWork().studentSubmissions().list(
                            courseId=data.get("id"), courseWorkId=assignment.get("id")).execute().get(
                            "studentSubmissions")
                        state_object = [
                            {
                                "student_id": state.get("userId"),
                                "state": state.get("state"),
                                "score": state.get("assignedGrade") if state.get("assignedGrade") is not None else 0
                            } for state in assignment_object_history
                        ]

                        assignment_object_new = [{"_id": assignment.get("id"),
                                                  "name": assignment.get("title"),
                                                  "due_date": assignment.get("dueDate"),
                                                  "due_time": assignment.get("dueTime"),
                                                  "max_point": assignment.get("maxPoints"),
                                                  "student_submission": state_object} for assignment in
                                                 assignment_object]

                        if teacher_object and student_object is not None:
                            DB.insert(collection='classroom', data={
                                '_id': data.get("id"),
                                'name': data.get("name"),
                                'total_member': student_object.__len__(),
                                'environment': "google_classroom",
                                'teacher': teacher_object,
                                'student_list': student_object,
                                'assignment_list': assignment_object_new,
                                'criteria': None
                            })
        except:
            pass
        classroom_list = list(DB.DATABASE['classroom'].find({}))
        return classroom_list

    @staticmethod
    def getAllMSTeamsClassrooms():
        return None
