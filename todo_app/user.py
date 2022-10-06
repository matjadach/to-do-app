from flask_login import UserMixin
import os

class User(UserMixin):
    def __init__(self, user_id):
        self.user_id = user_id

    def get_id(self):
        return (self.user_id)
    
    @property
    def role(self):
        if self.user_id == int(os.environ.get("ADMIN_ID")):
            return 'admin'
        else:
            return 'reader'