import datetime
from app.src.object.tokenHistory.services.TokenHistoryServices import TokenHistoryServices
from app.src.server.database import DB
from app.src.object.token.entity.Token import TokenDAO


class TokenServices:
    @staticmethod
    def add(amountOfCoin):
        try:
            if amountOfCoin > 0:
                tokenAmount = TokenDAO(amountOfCoin)
                try:
                    current_token = list(DB.DATABASE['token'].find({"_id": "1"}).limit(1))[0]["amount"]
                except:
                    current_token = 0
                DB.upsert(collection='token', id="1", data={
                    'amount': current_token + tokenAmount.amountOfCoin
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
    def getAmountOfCoin():
        try:
            return DB.DATABASE['token'].find({"_id": "1"}).limit(1)[0]["amount"]
        except:
            return 0

    @staticmethod
    def sendToken(course_id):
        studentList = list(DB.DATABASE['user'].find({"role": "student"}))
        tokenAmount = TokenServices.getAmountOfCoin()
        if not list(DB.DATABASE['criteria'].find({"_id": course_id}))[0]:
            return "Classroom not found"
        if studentList.__len__() <= 0:
            return "Students not found"
        elif tokenAmount <= 0:
            return "Token amount is 0 or less than 0"
        else:
            criteria = list(DB.DATABASE['criteria'].find({"_id": course_id}))[0]
            giveToken = (10 * tokenAmount) / (studentList.__len__() * (10 ** (len(str(round(tokenAmount, 3))) - 1)))
            allAssignmentList = list(DB.DATABASE['assignment'].find({"course_id": course_id},
                                                                    {'student_submission': True, 'name': True,
                                                                     'due_date': True, "due_time": True,
                                                                     "_id": False}))
            for allAssignmentListIndex, assignmentList in enumerate(allAssignmentList):
                if assignmentList["due_date"] is None or assignmentList["due_time"] is None:
                    pass
                else:
                    submissionList = allAssignmentList[allAssignmentListIndex]["student_submission"]
                    assignmentDateTime = datetime.datetime(assignmentList["due_date"]["year"],
                                                           assignmentList["due_date"]["month"],
                                                           assignmentList["due_date"]["day"],
                                                           assignmentList["due_time"]["hours"],
                                                           assignmentList["due_time"]["minutes"], 0)
                    if (assignmentDateTime - datetime.datetime.now()).days <= -1:
                        # ====================== Criteria 1 ===================
                        if (criteria["first"]["value"] is True) and (
                                "attendance" not in assignmentList["name"].lower()):
                            submissionDateTime = []
                            for criteriaOneIndex, studentSubmission in enumerate(submissionList):
                                submissionDateTime.append(
                                    datetime.datetime(studentSubmission["update_date"]["year"],
                                                      studentSubmission["update_date"]["month"],
                                                      studentSubmission["update_date"]["day"],
                                                      studentSubmission["update_time"]["hours"],
                                                      studentSubmission["update_time"]["minutes"],
                                                      studentSubmission["update_time"]["seconds"]))
                                print(studentSubmission["user_id"])
                                if (assignmentDateTime - submissionDateTime[criteriaOneIndex]).days >= 0 and \
                                        studentSubmission["state"] == "TURNED_IN":
                                    if "student" in list(DB.DATABASE['user'].find(
                                            {"google_object._id":
                                                 studentSubmission["user_id"]}))[0]["role"]:
                                        DB.DATABASE['user'].update_one(
                                            {"google_object._id": studentSubmission["user_id"]},
                                            {"$set": {
                                                "current_token":
                                                    list(DB.DATABASE['user'].find(
                                                        {"google_object._id":
                                                             studentSubmission["user_id"]}))[0][
                                                        "current_token"] + giveToken
                                            }})
                                        DB.DATABASE['token'].update_one(
                                            {"_id": "1"},
                                            {"$set": {
                                                "amount":
                                                    list(DB.DATABASE['token'].find(
                                                        {"_id": "1"}))[0]["amount"] - giveToken
                                            }})
                                        TokenHistoryServices.add(giveToken, list(DB.DATABASE['user'].find(
                                            {"google_object._id": studentSubmission["user_id"]}))[0]["_id"],
                                                                 "sendTokenToStudent")
                        # ====================== Criteria 2 ===================
                        if (criteria["second"]["value"] is True) and (
                                "attendance" not in assignmentList["name"].lower()):
                            submissionDateTime = []
                            for criteriaTwoIndex, studentSubmission in enumerate(submissionList):
                                submissionDateTime.append(
                                    datetime.datetime(studentSubmission["update_date"]["year"],
                                                      studentSubmission["update_date"]["month"],
                                                      studentSubmission["update_date"]["day"],
                                                      studentSubmission["update_time"]["hours"],
                                                      studentSubmission["update_time"]["minutes"],
                                                      studentSubmission["update_time"]["seconds"]))
                                keepTempContinuously = []
                                for count in range(criteria["second"]["count"]):
                                    if (assignmentDateTime - submissionDateTime[criteriaTwoIndex]).days >= 0 and \
                                            studentSubmission["state"] == "TURNED_IN":
                                        if studentSubmission not in keepTempContinuously:
                                            keepTempContinuously.append(studentSubmission)
                                if len(keepTempContinuously) >= criteria["second"]["count"]:
                                    if "student" in list(DB.DATABASE['user'].find(
                                            {"google_object._id":
                                                 studentSubmission["user_id"]}))[0]["role"]:
                                        DB.DATABASE['user'].update_one(
                                            {"google_object._id": studentSubmission["user_id"]},
                                            {"$set": {
                                                "current_token":
                                                    list(DB.DATABASE['user'].find(
                                                        {"google_object._id":
                                                             studentSubmission["user_id"]}))[0][
                                                        "current_token"] + giveToken
                                            }})
                                        DB.DATABASE['token'].update_one(
                                            {"_id": "1"},
                                            {"$set": {
                                                "amount":
                                                    list(DB.DATABASE['token'].find(
                                                        {"_id": "1"}))[0]["amount"] - giveToken
                                            }})
                                        TokenHistoryServices.add(giveToken, list(DB.DATABASE['user'].find(
                                            {"google_object._id": studentSubmission["user_id"]}))[0]["_id"],
                                                                 "sendTokenToStudent")
                        # ====================== Criteria 3 ===================
                        if criteria["third"]["value"] is True:
                            submissionDateTime = []
                            for criteriaThreeIndex, studentSubmission in enumerate(submissionList):
                                submissionDateTime.append(
                                    datetime.datetime(studentSubmission["update_date"]["year"],
                                                      studentSubmission["update_date"]["month"],
                                                      studentSubmission["update_date"]["day"],
                                                      studentSubmission["update_time"]["hours"],
                                                      studentSubmission["update_time"]["minutes"],
                                                      studentSubmission["update_time"]["seconds"]))
                                for studentSubmission in submissionList:
                                    if ("attendance" in assignmentList["name"].lower()) and (
                                            studentSubmission["state"] == "TURNED_IN") and (
                                            assignmentDateTime - submissionDateTime[criteriaThreeIndex]).days >= 0:
                                        if "student" in list(DB.DATABASE['user'].find(
                                                {"google_object._id":
                                                     studentSubmission["user_id"]}))[0]["role"]:
                                            DB.DATABASE['user'].update_one(
                                                {"google_object._id": studentSubmission["user_id"]},
                                                {"$set": {
                                                    "current_token":
                                                        list(DB.DATABASE['user'].find(
                                                            {"google_object._id":
                                                                 studentSubmission["user_id"]}))[0][
                                                            "current_token"] + giveToken
                                                }})
                                            DB.DATABASE['token'].update_one(
                                                {"_id": "1"},
                                                {"$set": {
                                                    "amount":
                                                        list(DB.DATABASE['token'].find(
                                                            {"_id": "1"}))[0]["amount"] - giveToken
                                                }})
                                            TokenHistoryServices.add(giveToken, list(DB.DATABASE['user'].find(
                                                {"google_object._id": studentSubmission["user_id"]}))[0]["_id"],
                                                                     "sendTokenToStudent")
            return "Send the token to the student successfully"
