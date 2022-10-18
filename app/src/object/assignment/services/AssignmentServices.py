from orjson import orjson
from starlette.responses import Response
from app.src.resources import Google
from app.src.server.database import DB
from pymongo import UpdateOne


class AssignmentServices:

    @staticmethod
    def getAll(user_id, course_id):
        try:
            google = Google.GoogleCredential(user_id)
            googleUserId = \
                list(DB.DATABASE['user'].find({"_id": user_id}, {"google_object._id": True, "_id": False}).limit(1))[0][
                    'google_object']['_id']
            DATA = []
            for assignment in google.courses().courseWork().list(courseId=course_id).execute().get(
                    "courseWork"):
                submission = google.courses().courseWork().studentSubmissions().list(
                    courseId=course_id, courseWorkId=assignment.get("id"), userId=googleUserId).execute().get(
                    "studentSubmissions")[0]
                dateTime = submission.get("updateTime").replace("-", "/").replace("T", " ").split(".")
                dateTime = dateTime[0].split(" ")
                date = dateTime[0].split("/")
                time = dateTime[1].split(":")
                if len(time) == 1:
                    time[1] = 0
                elif len(time) == 2:
                    time[2] = 0
                submissionObject = {
                    "user_id": submission.get("userId"),
                    "state": submission.get("state"),
                    "update_date": {
                        "year": int(date[0]),
                        "month": int(date[1]),
                        "day": int(date[2])
                    },
                    "update_time": {
                        "hours": int(time[0]),
                        "minutes": int(time[1]),
                        "seconds": int(time[2])
                    },
                    "score": submission.get("assignedGrade") if submission.get(
                        "assignedGrade") is not None else 0,
                }
                try:
                    studentSubmissionList = list(
                        DB.DATABASE["assignment"].find(
                            {"_id": assignment.get("id")}).limit(1))[0]["student_submission"]
                    arr = []
                    for submissionList in studentSubmissionList:
                        arr.append(submissionList["user_id"])
                except:
                    studentSubmissionList = [submissionObject]

                DATA.append(UpdateOne({'_id': assignment.get("id")}, {'$set': {
                    "_id": assignment.get("id"),
                    "course_id": assignment.get("courseId"),
                    "name": assignment.get("title"),
                    "due_date": assignment.get("dueDate"),
                    "due_time": assignment.get("dueTime"),
                    "max_point": assignment.get("maxPoints"),
                    "student_submission": studentSubmissionList if submission is not None else []
                }}, upsert=True))
                if len(DATA) == 10:
                    DB.DATABASE['assignment'].bulk_write(DATA, ordered=False)
                    DATA = []
            if len(DATA) > 0:
                DB.DATABASE['assignment'].bulk_write(DATA, ordered=False)
            assignment = list(DB.DATABASE['assignment'].find({"course_id": course_id}, {"student_submission": False}))[
                0]

            return Response(content=orjson.dumps(assignment))
        except:
            return "The assignment is not found for this ID or the classroom ID is not correct"
