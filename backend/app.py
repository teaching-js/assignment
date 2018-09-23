import falcon
import sqlite3
from endpoints.Login import Login

class App:
    def __init__(self, db_url):
        self.db = sqlite3.connect(db_url)
        self.api = falcon.API()
        self.api.add_route('/login', Login(self.db))
