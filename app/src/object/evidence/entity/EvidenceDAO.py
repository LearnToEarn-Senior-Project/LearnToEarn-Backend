class EvidenceDAO(object):
    __slots__ = "reward_name", "student_name", "student_id", "remain_reward", "price", "date"

    def __init__(self, reward_name, student_name, student_id, remain_reward, price, date):
        self.reward_name = reward_name
        self.student_name = student_name
        self.student_id = student_id
        self.remain_reward = remain_reward
        self.price = price
        self.date = date