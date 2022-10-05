import os

class Config:
    def __init__(self):
        """Base configuration variables."""
        self.API_KEY = os.environ.get('API_KEY')
        self.API_TOKEN = os.environ.get('API_TOKEN')
        self.BOARD = os.environ.get("BOARD")
        self.NOTSTARTED_LIST = os.environ.get("NOTSTARTED_LIST")
        self.INPROGRESS_LIST = os.environ.get("INPROGRESS_LIST")
        self.COMPLETED_LIST = os.environ.get("COMPLETED_LIST")
        self.SECRET_KEY = os.environ.get("SECRET_KEY")
        if not self.API_KEY:
            raise ValueError("No API_KEY defined. Did you follow the README file?")
        if not self.API_TOKEN:
            raise ValueError("No API_TOKEN defined. Did you follow the README file?")
        if not self.BOARD:
            raise ValueError("No BOARD ID defined. Did you follow the README file?")
        if not self.NOTSTARTED_LIST:
            raise ValueError("No NOTSTARTED_LIST ID defined. Did you follow the README file?")
        if not self.INPROGRESS_LIST:
            raise ValueError("No INPROGRESS_LIST ID defined. Did you follow the README file?")
        if not self.COMPLETED_LIST:
            raise ValueError("No COMPLETED_LIST ID defined. Did you follow the README file?")
        if not self.SECRET_KEY:
            raise ValueError("No SECRET_KEY ID defined. Did you follow the README file?")
