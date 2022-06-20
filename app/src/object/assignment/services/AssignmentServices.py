import numpy as np
from srsly.ujson import ujson
from starlette.responses import Response

from app.src.resources import Google
from app.src.server.database import DB
from pymongo import UpdateOne


class AssignmentServices:

    @staticmethod
    def getAll(id, course_id):
        try:
            submitList = None
            submission = None
            google = Google.GoogleCredential(id)
            googleUserId = list(DB.DATABASE['user'].find({"_id": id}).limit(1))[0]["google_object"]["_id"]
            DATA = np.array([])
            for assignment in google.courses().courseWork().list(courseId=course_id).execute().get("courseWork"):
                arr = np.array([])
                try:
                    submission = google.courses().courseWork().studentSubmissions().list(
                        courseId=course_id, courseWorkId=assignment.get("id"), userId=googleUserId).execute().get(
                        "studentSubmissions")[0]
                    submitList = list(
                        DB.DATABASE["assignment"].find(
                            {"_id": assignment.get("id"), "student_submission.user_id": submission.get("userId")}))
                    if submission.get("userId") not in submitList:
                        np.append(arr, [{
                            "user_id": submission.get("userId"),
                            "state": submission.get("state"),
                            "score": submission.get("assignedGrade") if submission.get(
                                "assignedGrade") is not None else 0
                        }], axis=0)
                except:
                    pass
                np.append(DATA, [UpdateOne({'_id': assignment.get("id")}, {'$set': {
                    "_id": assignment.get("id"),
                    "course_id": assignment.get("courseId"),
                    "name": assignment.get("title"),
                    "due_date": assignment.get("dueDate"),
                    "due_time": assignment.get("dueTime"),
                    "max_point": assignment.get("maxPoints"),
                    "student_submission": arr if submission is not None else []
                }}, upsert=True)], axis=0)
                if len(DATA) == 10:
                    DB.DATABASE['assignment'].bulk_write(DATA, ordered=False)
                    DATA = np.array([])
            if len(DATA) > 0:
                DB.DATABASE['assignment'].bulk_write(DATA, ordered=False)
            return Response(content=ujson.dumps(list(DB.DATABASE['assignment'].find({"course_id": course_id}))))
        except:
            return "The assignment is not available for this ID or the classroom ID is not correct"
