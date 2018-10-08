import sqlite3
import secrets
from flask import Flask, request, make_response, render_template
from flask_restplus import Resource, Api, abort, reqparse, fields
from util.DB_Interface import DB
import json

app = Flask(__name__)
api = Api(app)
auth = api.namespace('auth', description='Authentication Services')
user = api.namespace('user', description='User Information Services')
db = DB()

user_details = api.model('Test', {
  'username': fields.String(required=True, example='greg'),
  'password': fields.String(required=True, example='1234'),
})

@auth.route('/login')
class Login(Resource):
    def unpack(j,*args,**kargs):
        r = [j.get(arg,None) for arg in args]
        if kargs.get("required",True):
            [abort(kargs.get("error",400)) for e in r if e == None]
        return r

    def gen_token():
        token = secrets.token_hex(32)
        while db.exists("USER").where(curr_token=token):
            token = secrets.token_hex(32)
        return token

    @auth.response(200, 'Success')
    @auth.response(400, 'Missing Username/Password')
    @auth.response(405, 'Invalid Username/Password')
    @api.expect(user_details)
    def post(self):
        (un,ps) = unpack(request.json,"username","password")
        if not db.exists("USER").where(username=un,password=ps):
            abort(405)
        t = self.gen_token()
        db_r = db.update("USER").set(curr_token=t).where(username=un)
        db_r.execute()
        return {
            "msg": "success",
            "token": t
        }

@user.route('/user')
class User(Resource):
    def get(self):
        t = request.headers.get('Authorization',None)
        if not t:
            abort(400)
        t = t.split(" ")[1]
        u = db.select("USER").where(curr_token=t).execute()
        return {
            "username": u[0]
        }

# base
@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
