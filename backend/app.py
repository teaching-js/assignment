from flask import Flask, request
from flask_restplus import Api
from util.DB_Interface import DB
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)
db = DB()
