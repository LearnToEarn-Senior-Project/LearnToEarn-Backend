class TokenHistoryDAO(object):
    __slots__ = "date", "amountOfCoin", "student_id", "reward_id"

    def __init__(self, date, amountOfCoin, student_id, reward_id):
        self.date = date
        self.amountOfCoin = amountOfCoin
        self.student_id = student_id
        self.reward_id = reward_id
