class CMUUserDAO(object):
    __slots__ = "id", "firstname", "lastname", "email", "google_object", "role"

    def __init__(self, id, firstname, lastname, email, google_object, role):
        self.id: str = id
        self.firstname: str = firstname
        self.lastname: str = lastname
        self.email: str = email
        self.google_object: object = google_object
        self.role: str = role
