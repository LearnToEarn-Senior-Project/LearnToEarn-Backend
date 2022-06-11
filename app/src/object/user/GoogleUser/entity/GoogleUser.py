class GoogleUser(object):
    __slots__ = "id", "user_token", "firstname", "lastname", "email", "image_url"

    def __init__(self, id, user_token, firstname, lastname, email, image_url):
        self.id: str = id
        self.user_token: object = user_token
        self.firstname: str = firstname
        self.lastname: str = lastname
        self.email: str = email
        self.image_url: str = image_url
