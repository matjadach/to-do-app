from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_id):
        self.user_id = user_id

    def get_id(self):
        return (self.user_id)