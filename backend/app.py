from globals import *
from models import *
import json
from datetime import datetime
from globals import app

# magic
auth = api.namespace('auth', description='Authentication Services')
user = api.namespace('user', description='User Information Services')
posts = api.namespace('post', description='Post Services')

# end points
@auth.route('/login')
class Login(Resource):
    @auth.response(200, 'Success')
    @auth.response(400, 'Missing Username/Password')
    @auth.response(405, 'Invalid Username/Password')
    @auth.expect(login_details)
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
            "message": "success",
            "token": t
        }

@user.route('/')
class User(Resource):
    @user.response(200, 'Success', user_details)
    @user.response(405, 'Invalid Auth Token')
    @user.response(400, 'Malformed Request')
    @user.expect(auth_details)
    def get(self):
        u = authorize(request)
        u_id = u[0]
        u_username = u[1]
        follow_list = get_text_list(u[4])
        posts_raw = db.select_all("POST").where(author=u_username).execute()
        posts = [post[0] for post in posts_raw]
        return {
            "username": u[1],
            "name": u[2],
            "id"  : u[0],
            "email": u[3],
            "following": [int(x) for x in follow_list],
            "posts": posts
        }

    @user.response(405, 'Invalid Authorization Token')
    @user.response(200, 'Success')
    @user.response(400, 'Malformed user object')
    @user.expect(auth_details,user_update_details)
    def put(self):
        u = authorize(request)
        u_id = u[0]
        if not request.json:
            abort(400, 'Malformed request')
        keys = request.json.keys()
        valid_keys=["password","name","email"]
        if not sum([k in valid_keys for k in keys]) == len(keys):
            abort(400, 'Malformed request')
        t = t.split(" ")[1]
        db.update("USER").where(id=u_id).set(**request.json).execute()

@user.route('/feed')
class Feed(Resource):
    @user.response(405, 'Invalid Auth Token')
    @user.response(400, 'Malformed Request')
    @user.response(200, 'Success', post_list_details)
    @user.expect(auth_details)
    @user.param("p","Number of posts to fetch")
    def get(self):
        u = authorize(request)
        n = request.args.get('p',None)
        if not n:
            abort(400,'Malformed Request')

        following = get_text_list(u[4],process_f=lambda x:int(x))
        following = [db.select("USER").where(id=id).execute()[1] for id in following]
        wildcards = ",".join(["?"]*len(following))
        q = "SELECT * FROM POSTS WHERE author in ({})".format(wildcards)
        q+=" LIMIT ?"
        following.append(n)
        all_posts = db.raw(q,following)
        all_posts = [format_post(row) for row in all_posts]
        print(all_posts)
        all_posts.sort(reverse=True,key=lambda x: datetime.strptime(x["meta"]["published"],"%Y-%m-%d %H:%M:%S.%f"))
        return {
            "posts": all_posts
        }

@user.route('/follow')
class Follow(Resource):
    @user.response(200, 'Success')
    @user.response(405, 'Invalid Auth Token')
    @user.response(400, 'Malformed Request')
    @user.expect(auth_details)
    @user.param("username","username of person to follow")
    def put(self):
        u = authorize(request)
        u_id = u[0]
        follow_list = get_text_list(u[4])
        to_follow = request.args.get('username',None)
        if to_follow == None or not db.exists("USER").where(username=to_follow):
            abort(400,'Malformed Request Or Unknown username')
        to_follow = db.select("USER").where(username=to_follow).execute()[0]
        follow_list.add(to_follow)
        db.update("USER").set(following=get_list_text(follow_list)).where(id=u_id).execute()
        return {
            "message": "success"
        }
@user.route('/unfollow')
class UnFollow(Resource):
    @user.response(200, 'Success')
    @user.response(405, 'Invalid Auth Token')
    @user.response(400, 'Malformed Request')
    @user.expect(auth_details)
    @user.param("username","username of person to follow")
    def put(self):
        u = authorize(request)
        u_id = u[0]
        following = get_text_list(u[4])
        to_follow = request.args.get('username',None)
        if to_follow == None or not db.exists("USER").where(username=to_follow):
            abort(400,'Malformed Request Or Unknown username')
        to_follow = db.select("USER").where(username=to_follow).execute()[0]
        follow_list.discard(to_follow)
        db.update("USER").set(following=get_list_text(follow_list)).where(id=u_id).execute()
        return {
            "message": "success"
        }

@posts.route('/')
class Post(Resource):
    @posts.response(200, 'Success')
    @posts.response(405, 'Invalid Auth Token')
    @posts.response(400, 'Malformed Request')
    @posts.expect(auth_details,new_post_details)
    def post(self):
        j = request.json
        u = authorize(request)
        u_username = u[1]
        if not j:
            abort(400, 'Malformed request')
        (desc,src) = unpack(j,"description_text","src")
        db.insert("POST").with_values(
            author=u_username,
            description=desc,
            published=datetime.now(),
            likes="",
            thumbnail=src, #TODO: what is the thumbnail supposed to be?
            src=src
        ).execute()
        return {
            "message": "success"
        }
    @posts.response(200, 'Success')
    @posts.response(405, 'Invalid Auth Token')
    @posts.response(400, 'Malformed Request')
    @posts.param("id","the id of the post to update")
    @posts.expect(auth_details,new_post_details)
    def put(self):
        j = request.json
        id = request.args.get("id",None)
        u = authorize(request)
        u_username = u[1]
        if not j or not id:
            abort(400, 'Malformed request')
        if not db.exists("POST").where(id=id):
            abort(400, 'Malformed request')
        # check the logged in user made this post
        post_author = db.select("POST").where(id=id).execute()[1]
        if u[1] != post_author:
            abort(405, 'You Are Unauthorized To Make That Request')
        (desc,src) = unpack(j,"description_text","src",required=False)
        updated = {}
        if desc:
            updated["description"] = desc
        if src:
            updated["src"] = src
        db.update("POST").set(**updated).where(id=id).execute()
        return {
            "message": "success"
        }
    @posts.response(200, 'Success')
    @posts.response(400, 'Missing Username/Password')
    @posts.response(405, 'Invalid Auth Token')
    @posts.expect(auth_details)
    @posts.param("id","the id of the post to delete")
    def delete(self):
        u = authorize(request)
        id = request.args.get("id",None)
        if not id:
            abort(400,"Malformed Request")

        if not db.exists("POST").where(id=id):
            return {
                "message": "No Post With Supplied ID Exists"
            }
        p = db.select("POST").where(id=id).execute()
        print(p[1],u[1])
        if p[1] != u[1]:
            abort(405,"You Are Unauthorized To Make That Request")
        comment_list = get_text_list(p[7])
        [db.delete("COMMENT").where(id=c_id).execute() for c_id in comment_list]
        db.delete("POST").where(id=id).execute()
        return {
            "message": "success"
        }
    @posts.response(200, 'Success',post_details)
    @posts.response(400, 'Missing Username/Password')
    @posts.response(405, 'Invalid Auth Token')
    @posts.expect(auth_details)
    @posts.param("id","the id of the post to fetch")
    def get(self):
        u = authorize(request)
        id = request.args.get("id",None)
        if not id:
            abort(400,"Malformed Request")
        p = db.select("POST").where(id=id).execute()
        if not p:
            abort(400,"Malformed Request")
        return format_post(p)

@posts.route('/like')
class Like(Resource):
    @posts.response(200, 'Success')
    @posts.response(405, 'Invalid Auth Token')
    @posts.response(400, 'Malformed Request')
    @posts.param("id","the id of the post to like")
    @posts.expect(auth_details)
    def put(self):
        u = authorize(request)
        id = request.args.get("id",None)
        if not id or not db.exists("POST").where(id=id):
            abort(400, 'Malformed request')
        p = db.select("POST").where(id=id).execute()
        likes = get_text_list(p[4],process_f=lambda x:int(x))
        likes.add(u[0])
        likes = get_list_text(likes)
        db.update("POST").set(likes=likes).where(id=id).execute()
        return {
            "message": "success"
        }

@posts.route('/unlike')
class Unlike(Resource):
    @posts.response(200, 'Success')
    @posts.response(405, 'Invalid Auth Token')
    @posts.response(400, 'Malformed Request')
    @posts.param("id","the id of the post to unlike")
    @posts.expect(auth_details)
    def put(self):
        u = authorize(request)
        id = request.args.get("id",None)
        if not id or not db.exists("POST").where(id=id):
            abort(400, 'Malformed request')
        p = db.select("POST").where(id=id).execute()
        likes = get_text_list(p[4],process_f=lambda x: int(x))
        likes.discard(u[0])
        likes = get_list_text(likes)
        db.update("POST").set(likes=likes).where(id=id).execute()
        return {
            "message": "success"
        }

@posts.route('/comment')
class Comment(Resource):
    @posts.response(200, 'Success')
    @posts.response(405, 'Invalid Auth Token')
    @posts.response(400, 'Malformed Request')
    @posts.param("id","the id of the post to comment on")
    @posts.expect(auth_details,comment_details)
    def put(self):
        u = authorize(request)
        j = request.json
        id = request.args.get("id",None)
        if not id or not j:
            abort(400, 'Malformed request')
        if not db.exists("POST").where(id=id):
            abort(400, 'Malformed request')
        (comment,) = unpack(j,"comment")
        comment_id = db.insert("COMMENT").with_values(
            comment=comment,
            author=u[1],
            published=datetime.now()
        ).execute()
        p = db.select("POST").where(id=id).execute()
        comment_list = get_text_list(p[7],process_f=lambda x: int(x))
        comment_list.add(comment_id)
        comment_list = get_list_text(comment_list)
        db.update("POST").set(comments=comment_list).where(id=id).execute()
        return {
            "message": "success"
        }

if __name__ == "__main__":
    app.run(debug=True)
