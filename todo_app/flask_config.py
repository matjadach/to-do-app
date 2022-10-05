import os

class Config:
    def __init__(self):
        """Base configuration variables."""
        self.SECRET_KEY = os.environ.get("SECRET_KEY")
        if not self.SECRET_KEY:
            raise ValueError("No SECRET_KEY ID defined. Did you follow the README file?")

        self.CLIENT_ID = os.environ.get("CLIENT_ID")
        if not self.CLIENT_ID:
            raise ValueError("No CLIENT_ID ID defined. Did you follow the README file?")

        self.CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
        if not self.CLIENT_SECRET:
            raise ValueError("No CLIENT_SECRET ID defined. Did you follow the README file?")

        self.SECRET_KEY = os.environ.get("SECRET_KEY")
        if not self.SECRET_KEY:
            raise ValueError("No SECRET_KEY ID defined. Did you follow the README file?")
