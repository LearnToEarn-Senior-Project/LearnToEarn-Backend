import datetime
from app.src.server.database import DB
from app.src.object.token.entity.TokenDAO import TokenDAO


class TokenServices:
    @staticmethod
    def add(amount):
        try:
            if amount > 0:
                tokenAmount = TokenDAO(amount)
                try:
                    current_token = list(DB.DATABASE['token'].find({"_id": "1"}).limit(1))[0]["amount"]
                except:
                    current_token = 0
                DB.upsert(collection='token', id="1", data={
                    'amount': current_token + tokenAmount.amount
                })
                return list(DB.DATABASE['token'].find({"_id": "1"}).limit(1))[0]
            else:
                return "Token amount must more than 0!!"
        except:
            return "The token amount cannot be null"

    @staticmethod
    def getStudentToken(user_id):
        try:
            studentToken = list(DB.DATABASE['user'].find({"_id": user_id}).limit(1))[0]["current_token"]
        except:
            studentToken = []
        return studentToken

    @staticmethod
    def getAmount():
        try:
            return DB.DATABASE['token'].find({"_id": "1"}).limit(1)[0]["amount"]
        except:
            return 0

    @staticmethod
    def sendToken():
        studentList = list(DB.DATABASE['user'].find({"role": "student"}))
        tokenAmount = list(DB.DATABASE['token'].find({"_id": "1"}, {"amount": True, "_id": False}))[0]["amount"]
        criteriaList = list(DB.DATABASE['criteria'].find())
        for index, criteria in enumerate(criteriaList):
            if DB.DATABASE['assignment'].find({"course_id": criteria['_id']}) is not []:
                giveToken = (10 * tokenAmount) / (studentList.__len__() * (10 ** (len(str(tokenAmount)) - 1))) \
                    if studentList.__len__() > 0 else 0
                allAssignmentList = list(DB.DATABASE['assignment'].find({"course_id": criteria['_id']},
                                                                        {'student_submission': True, 'name': True,
                                                                         'due_date': True, "due_time": True,
                                                                         "_id": False}))
                for allAssignmentListIndex, assignmentList in enumerate(allAssignmentList):
                    submissionList = allAssignmentList[allAssignmentListIndex]["student_submission"]
                    assignmentDateTime = datetime.datetime(assignmentList["due_date"]["year"],
                                                           assignmentList["due_date"]["month"],
                                                           assignmentList["due_date"]["day"],
                                                           assignmentList["due_time"]["hours"],
                                                           assignmentList["due_time"]["minutes"], 0)

                    if (assignmentDateTime - datetime.datetime.now()).days <= -1:
                        # ====================== Criteria 1 ===================
                        if (criteria["first"] is True) and ("attendance" not in assignmentList["name"].lower()):
                            submissionDateTime = []
                            for criteriaOneIndex, studentSubmission in enumerate(submissionList):
                                submissionDateTime.append(
                                    datetime.datetime(studentSubmission["update_date"]["year"],
                                                      studentSubmission["update_date"]["month"],
                                                      studentSubmission["update_date"]["day"],
                                                      studentSubmission["update_time"]["hours"],
                                                      studentSubmission["update_time"]["minutes"],
                                                      studentSubmission["update_time"]["seconds"]))
                                if (assignmentDateTime - submissionDateTime[criteriaOneIndex]).days > 0:
                                    DB.DATABASE['user'].update_one({"google_object._id": studentSubmission["user_id"]},
                                                                   {"$set": {
                                                                       "current_token":
                                                                           list(DB.DATABASE['user'].find(
                                                                               {"google_object._id":
                                                                                    studentSubmission[
                                                                                        "user_id"]}))[
                                                                               0][
                                                                               "current_token"] + giveToken
                                                                   }})

                        #   ====================== Criteria 2 =================== ติดดดดด แงงงงงงงง
                        if criteria["second"]["value"] is True:
                            allAssignmentInClassroom = list(
                                DB.DATABASE['assignment'].find({"course_id": criteria['_id']},
                                                               {"student_submission": True}))
                            try:
                                for count in range(criteria["second"]["count"]):
                                    for criteriaTwoIndex, studentSubmission in enumerate(
                                            allAssignmentInClassroom[count]["student_submission"]):
                                        print(studentSubmission)
                            except:
                                print("Bruh")
                                continue

                        #   ====================== Criteria 3 ===================
                        if criteria["third"] is True:
                            for studentSubmission in submissionList:
                                if ("attendance" in assignmentList["name"].lower()) and (
                                        studentSubmission["state"] == "TURNED_IN"):
                                    DB.DATABASE['user'].update_one({"google_object._id": studentSubmission["user_id"]},
                                                                   {"$set": {
                                                                       "current_token":
                                                                           list(DB.DATABASE['user'].find(
                                                                               {"google_object._id":
                                                                                    studentSubmission[
                                                                                        "user_id"]}))[
                                                                               0][
                                                                               "current_token"] + giveToken
                                                                   }})

# for summaryChecked in submissionList:
#     DB.DATABASE['assignment'].update_one(
#         {"_id": criteria['_id'], "student_submission.user_id": summaryChecked["user_id"]}, {
#             "$set": {
#                 "student_submission.checked": True
#             }
#         }, upsert=True)
# DB.DATABASE['assignment'].update_one(
#     {"_id": criteria['_id']}, {
#         "$set": {
#             "checked": True
#         }
#     }, upsert=True)
