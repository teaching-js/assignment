from app import api,db
from util.globals import *
from util.models import *
from flask_restplus import Resource, abort, reqparse, fields
from flask import request

dummy_user = api.namespace('dummy_user', description='Dummy User Information Services for testins')

@dummy_user.route('/')
class User(Resource):
    @dummy_user.response(200, 'Success', user_details)
    @dummy_user.response(400, 'Malformed Request')
    @dummy_user.param('id','Id of user to get information for (defaults to logged in user)')
    @dummy_user.doc(description='''
        Identical to GET /user but doesn't require any authentication
        Allows you to act as a "Anon" user.
    ''')
    def get(self):
        u = get_dummy_user()
        u_id = int(request.args.get('id',u[0]))
        if not db.exists('USER').where(id=u_id):
            abort(400,'Malformed Request')
        u = db.select('USER').where(id=u_id).execute()
        u_username = u[1]

        follow_list = text_list_to_set(u[4])
        posts_raw = db.select_all('POST').where(author=u_username).execute()
        posts = [post[0] for post in posts_raw]
        return {
            'username': u[1],
            'name': u[2],
            'id'  : int(u[0]),
            'email': u[3],
            'following': [int(x) for x in follow_list],
            'followed_num': u[5],
            'posts': posts
        }

    @dummy_user.response(200, 'Success')
    @dummy_user.response(400, 'Malformed user object')
    @dummy_user.expect(user_update_details)
    @dummy_user.doc(description='''
        Identical to PUT /user but doesn't require any authentication
        Allows you to act as a "Anon" user.
    ''')
    def put(self):
        u = get_dummy_user()
        u_id = int(u[0])
        if not request.json:
            abort(400, 'Malformed request')

        allowed_keys=['password','name','email']
        safe = {}
        valid_keys = [k in allowed_keys for k in request.json.keys()]
        if len(valid_keys) < 1:
            abort(400, 'Malformed request')
        if "password" in valid_keys and request.json["password"] == "":
            abort(400, 'Malformed request')
        for k in valid_keys:
            safe[k] = request.json[k]
        db.update('USER').where(id=u_id).set(**safe).execute()
        return {
            "message": "success"
        }
@dummy_user.route('/feed')
class Feed(Resource):
    @dummy_user.response(200, 'Success', post_list_details)
    @dummy_user.param('n','Number of posts to fetch, 10 by default')
    @dummy_user.param('p','What post to start at, 0 by default')
    @dummy_user.doc(description='''
        Identical to GET /feed but doesn't require any authentication
        Allows you to act as a "Anon" user.
    ''')
    def get(self):
        u = get_dummy_user()
        n = request.args.get('n',10)
        p = request.args.get('p',0)
        following = text_list_to_set(u[4],process_f=lambda x:int(x))
        following = [db.select('USER').where(id=int(id)).execute()[1] for id in following]
        wildcards = ','.join(['?']*len(following))
        q = 'SELECT * FROM POSTS WHERE author in ({})'.format(wildcards)
        q+=' LIMIT ? OFFSET ?'
        following.append(n)
        following.append(p)
        all_posts = db.raw(q,following)
        all_posts = [format_post(row) for row in all_posts]
        all_posts.sort(reverse=True,key=lambda x: int(x["meta"]["published"]))
        return {
            'posts': all_posts
        }

@dummy_user.route('/follow')
class Follow(Resource):
    @dummy_user.response(200, 'Success')
    @dummy_user.response(400, 'Malformed Request')
    @dummy_user.param('username','username of person to follow')
    @dummy_user.doc(description='''
        Identical to PUT /user/follow but doesn't require any authentication
        Allows you to act as a "Anon" user.
    ''')
    def put(self):
        u = get_dummy_user()
        u_id = int(u[0])
        follow_list = text_list_to_set(u[4])
        to_follow = request.args.get('username',None)
        if to_follow == None or not db.exists('USER').where(username=to_follow):
            abort(400,'Malformed Request')
        if to_follow == u[1]:
            abort(400,'Malformed Request')
        to_follow = db.select('USER').where(username=to_follow).execute()[0]
        if to_follow not in follow_list:
            db.raw('UPDATE USERS SET FOLLOWED_NUM = FOLLOWED_NUM + 1 WHERE ID = ?',[to_follow])
        follow_list.add(to_follow)
        db.update('USER').set(following=set_to_text_list(follow_list)).where(id=u_id).execute()
        return {
            'message': 'success'
        }

@dummy_user.route('/unfollow')
class UnFollow(Resource):
    @dummy_user.response(200, 'Success')
    @dummy_user.response(400, 'Malformed Request')
    @dummy_user.param('username','username of person to follow')
    @dummy_user.doc(description='''
        Identical to PUT /user/unfollow but doesn't require any authentication
        Allows you to act as a "Anon" user.
    ''')
    def put(self):
        u = get_dummy_user()
        u_id = int(u[0])
        following = text_list_to_set(u[4])
        to_follow = request.args.get('username',None)
        if to_follow == u[1]:
            abort(400,'Malformed Request')
        if to_follow == None or not db.exists('USER').where(username=to_follow):
            abort(400,'Malformed Request Or Unknown username')
        to_follow = db.select('USER').where(username=to_follow).execute()[0]
        if to_follow in follow_list:
            db.raw('UPDATE USERS SET FOLLOWED_NUM = FOLLOWED_NUM - 1 WHERE ID = ?',[to_follow])
        follow_list.discard(to_follow)
        db.update('USER').set(following=set_to_text_list(follow_list)).where(id=u_id).execute()

        return {
            'message': 'success'
        }
