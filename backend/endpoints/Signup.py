import falcon
import json
import secrets
from util.DB_Interface import DB

class Signup:
    def __init__(self, db_conn):
        self.db = DB(db_conn)

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_405

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
