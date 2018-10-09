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
    "likes": fields.List(fields.Integer())
})

post_details = api.model('post_details',{
  "id": fields.Integer(),
  "meta": fields.Nested(post_meta),
  "thumbnail": fields.String(),
  "src": fields.String()
})
post_list = api.model('post_list',{
    "posts" : fields.List(fields.Nested(post_details))
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
user_update_details = api.model('user_details', {
    'email': fields.String(example='greg@fred.com'),
    'name':  fields.String(example='greg'),
    'password': fields.String(example='1234')
})
signup_details = api.model('signup_details', {
  'username': fields.String(required=True, example='xX_greginator_Xx'),
  'password': fields.String(required=True, example='1234'),
  'email': fields.String(required=True, example='greg@fred.com'),
  'name':  fields.String(required=True, example='greg')
})

auth_details = api.parser().add_argument('Authorization', help="Your Authorization Token in the form Token <AUTH_TOKEN>",location='headers')

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
    @auth.response(400, 'Malformed Request')
    @auth.response(405, 'Username Taken')
    @api.expect(signup_details)
    def post(self):
        (un,ps,em,n) = unpack(request.json,"username","password","email","name")
        if db.exists("USER").where(username=un):
            abort(405, 'Username Taken')
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
            abort(405,'Invalid Authorization Token')
        t = t.split(" ")[1]
        u = db.select("USER").where(curr_token=t).execute()
        return {
            "username": u[1],
            "name": u[2],
            "id"  : u[0],
            "email": u[3],
            "posts": None
        }
    @user.response(405, 'Invalid Authorization Token')
    @api.response(200, 'Success')
    @api.response(400, 'Malformed user object')
    @api.expect(auth_details,user_update_details)
    def put(self):
        t = request.headers.get('Authorization',None)
        if not t :
            abort(405, 'Invalid Authorization Token')
        if not request.json:
            abort(400, 'Malformed request')
        keys = request.json.keys()
        valid_keys=["password","name","email"]
        if not sum([k in valid_keys for k in keys]) == len(keys):
            abort(400, 'Malformed request')
        t = t.split(" ")[1]
        u = db.select("USER").where(curr_token=t).execute()
        u_id = u[0]
        db.update("USER").where(id=u_id).set(**request.json).execute()

@user.route('/feed')
class User(Resource):
    @user.response(405, 'Invalid Authorization Token')
    @api.expect(auth_details)
    @user.response(200, 'Success', post_list)
    @user.param("p","Number of posts to fetch")
    def get(self):
        t = request.headers.get('Authorization',None)
        n = request.form.get('p',None)
        if not t:
            abort(405,'Invalid Authorization Token')
        if not n:
            abort(400,'Malformed Request')
        t = t.split(" ")[1]
        u = db.select("USER").where(curr_token=t).execute()
        return {
            #TODO: do dis
            "posts": []
        }

@user.route('/follow')
class User(Resource):
    @user.response(405, 'Invalid Authorization Token')
    @api.expect(auth_details)
    @user.response(200, 'Success')
    @user.param("username","username of person to follow")
    def put(self):
        t = request.headers.get('Authorization',None)
        n = request.form.get('username',None)
        if not t:
            abort(405,'Invalid Authorization Token')
        if not n  or not db.exists("USER").where(username=n):
            abort(400,'Malformed Request')
        t = t.split(" ")[1]
        u = db.select("USER").where(curr_token=t).execute()
        u_id = u[0]
        f_id = db.select("USER").where(username=u).execute()[0]
        following = u[4]
        if following == None:
            following = ""
        follow_list = ",".join(following.split(",").append(n))
        db.update("USER").where(id=u_id).set(following=follow_list).execute()



if __name__ == "__main__":
    app.run(debug=True)
