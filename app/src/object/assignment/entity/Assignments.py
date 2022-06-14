class Assignment(object):
    __slots__ = "name", "due_date", "due_time", "max_point"

    def __init__(self, name, due_date, due_time, max_point):
        self.name: str = name
        self.due_date: object = due_date
        self.due_time: object = due_time
        self.max_point: int = max_point
