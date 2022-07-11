class TokenHistoryDAO(object):
    __slots__ = "date", "amount", "student_id", "reward_id"

    def __init__(self, date, amount, student_id, reward_id):
        self.date = date
        self.amount = amount
        self.student_id = student_id
        self.reward_id = reward_id
