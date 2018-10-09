import sqlite3
import secrets
from flask import Flask, request, make_response, render_template
from flask_restplus import Resource, Api, abort, reqparse, fields
from util.DB_Interface import DB
import json

# magic
app = Flask(__name__)
api = Api(app)
auth = api.namespace('auth', description='Authentication Services')
user = api.namespace('user', description='User Information Services')
db = DB()

# Modals



post_meta = api.model('post_meta',{
    "author": fields.Integer(),
    "description_text": fields.String(),
    "published": fields.String(),
    "likes": fields.List(fields.String())
})

post_details = api.model('post_details',{
  "id": fields.Integer(),
  "meta": fields.Nested(post_meta),
  "thumbnail": fields.String(),
  "src": fields.String()
})

login_details = api.model('login_details', {
  'username': fields.String(required=True, example='xX_greginator_Xx'),
  'password': fields.String(required=True, example='1234'),
})

user_details = api.model('user_details', {
    'id': fields.Integer(min=0),
    'username': fields.String(example='xX_greginator_Xx'),
    'email': fields.String(example='greg@fred.com'),
    'name':  fields.String(example='greg'),
    'posts': fields.List(fields.Nested(post_details))
})

signup_details = api.model('signup_details', {
  'username': fields.String(required=True, example='xX_greginator_Xx'),
  'password': fields.String(required=True, example='1234'),
  'email': fields.String(required=True, example='greg@fred.com'),
  'name':  fields.String(required=True, example='greg')
})

auth_details = api.parser().add_argument('Authorization', location='headers')

# Globals

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

# end points
@auth.route('/login')
class Login(Resource):
    def gen_token():
        token = secrets.token_hex(32)
        while db.exists("USER").where(curr_token=token):
            token = secrets.token_hex(32)
        return token

    @auth.response(200, 'Success')
    @auth.response(400, 'Missing Username/Password')
    @auth.response(405, 'Invalid Username/Password')
    @api.expect(login_details)
    def post(self):
        (un,ps) = unpack(request.json,"username","password")
        if not db.exists("USER").where(username=un,password=ps):
            abort(405)
        t = gen_token()
        db_r = db.update("USER").set(curr_token=t).where(username=un)
        db_r.execute()
        return {
            "msg": "success",
            "token": t
        }

@auth.route('/signup')
class Signup(Resource):
    @auth.response(200, 'Success')
    @auth.response(400, 'Missing Username/Password/Email')
    @auth.response(405, 'Username Taken')
    @api.expect(signup_details)
    def post(self):
        (un,ps,em,n) = unpack(request.json,"username","password","email","name")
        if db.exists("USER").where(username=un):
            abort(405)
        t = gen_token()
        db_r = db.insert("USER").with_values(
            curr_token=t,
            username=un,
            password=ps,
            email=em,
            name=n
        )
        db_r.execute()
        return {
            "msg": "success",
            "token": t
        }

@user.route('/')
class User(Resource):
    @user.response(405, 'Invalid Authorization Token')
    @api.expect(auth_details)
    @api.response(200, 'Success', user_details)
    def get(self):
        t = request.headers.get('Authorization',None)
        if not t:
            abort(405)
        t = t.split(" ")[1]
        u = db.select("USER").where(curr_token=t).execute()
        return {
            "username": u[1],
            "name": u[2],
            "id"  : u[0],
            "email": u[3],
            "posts": None
        }


if __name__ == "__main__":
    app.run(debug=True)
