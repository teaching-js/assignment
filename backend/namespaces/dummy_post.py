from app import api,db
from util.globals import *
from util.models import *
from flask_restplus import Resource, abort, reqparse, fields
from PIL import Image
from io import BytesIO
import base64
import time
from flask import request

dummy_posts = api.namespace('dummy_post', description='Dummy Post Services for testing')

@dummy_posts.route('/')
class Dummy_Post(Resource):
    @dummy_posts.response(200, 'Success', post_id_details)
    @dummy_posts.response(400, 'Malformed Request / Image could not be processed')
    @dummy_posts.expect(new_post_details)
    @dummy_posts.doc(description='''
        Identical to POST /post but doesn't require any authentication
        Allows you to act as a "Anon" user.
    ''')
    def post(self):
        j = request.json
        u = get_dummy_user()
        u_username = u[1]
        if not j:
            abort(400, 'Malformed request')
        (desc,src) = unpack(j,'description_text','src')
        if desc == "" or src == "":
            abort(400, 'Malformed request')
        try:
            size = (150,150)
            im = Image.open(BytesIO(base64.b64decode(src)))
            im.thumbnail(size, Image.ANTIALIAS)
            buffered = BytesIO()
            im.save(buffered, format='PNG')
            thumbnail = str(base64.b64encode(buffered.getvalue()))
        except:
            abort(400,'Image Data Could Not Be Processed')
        post_id = db.insert('POST').with_values(
            author=u_username,
            description=desc,
            published=str(time.time()),
            likes='',
            thumbnail=thumbnail,
            src=src
        ).execute()
        return {
            'post_id': post_id,
        }

    @dummy_posts.response(200, 'Success')
    @dummy_posts.response(400, 'Malformed Request')
    @dummy_posts.param('id','the id of the post to update')
    @dummy_posts.expect(new_post_details)
    @dummy_posts.doc(description='''
        Identical to PUT /post but doesn't require any authentication
        Allows you to act as a "Anon" user.
    ''')
    def put(self):
        j = request.json
        id = int(request.args.get('id',None))
        u = get_dummy_user()
        u_username = u[1]
        if not j or not id:
            abort(400, 'Malformed request')
        if not db.exists('POST').where(id=id):
            abort(400, 'Malformed request')
        # check the logged in user made this post
        post_author = db.select('POST').where(id=id).execute()[1]
        if u[1] != post_author:
            # exposing what post id's are valid and unvalid
            # may be a security issue lol
            abort(403, 'You Are Unauthorized To Edit That Post')
        (desc,src) = unpack(j,'description_text','src',required=False)
        if desc == None and src == None:
            abort(400, 'Malformed Request')
        updated = {}
        if desc:
            updated['description'] = desc
        if src:
            updated['src'] = src
        db.update('POST').set(**updated).where(id=id).execute()
        return {
            'message': 'success'
        }

    @dummy_posts.response(200, 'Success')
    @dummy_posts.response(400, 'Missing Username/Password')
    @dummy_posts.param('id','the id of the post to delete')
    @dummy_posts.doc(description='''
        Identical to DELETE /post but does not require any authentication
        Allows you to act as a "Anon" user.
    ''')
    def delete(self):
        u = get_dummy_user()
        id = int(request.args.get('id',None))
        if not id:
            abort(400,'Malformed Request')
        if not db.exists('POST').where(id=id):
            abort(400,'Malformed Request')
        p = db.select('POST').where(id=id).execute()
        print(p[1],u[1])
        if p[1] != u[1]:
            abort(403,'You Are Unauthorized To Make That Request')
        comment_list = text_list_to_set(p[7])
        [db.delete('COMMENT').where(id=c_id).execute() for c_id in comment_list]
        db.delete('POST').where(id=id).execute()
        return {
            'message': 'success'
        }
    @dummy_posts.response(200, 'Success',post_details)
    @dummy_posts.response(400, 'Missing Username/Password')
    @dummy_posts.param('id','the id of the post to fetch')
    @dummy_posts.doc(description='''
        Identical to GET /post but doesn't require any authentication
        Allows you to act as a "Anon" user.
    ''')
    def get(self):
        u = get_dummy_user()
        id = int(request.args.get('id',None))
        if not id:
            abort(400,'Malformed Request')
        p = db.select('POST').where(id=id).execute()
        if not p:
            abort(400,'Malformed Request')
        return format_post(p)

@dummy_posts.route('/like')
class Like(Resource):
    @dummy_posts.response(200, 'Success')
    @dummy_posts.response(400, 'Malformed Request')
    @dummy_posts.param('id','the id of the post to like')
    @dummy_posts.doc(description='''
        Identical to PUT /post/list but doesn't require any authentication
        Allows you to act as a "Anon" user.
    ''')
    def put(self):
        u = get_dummy_user()
        id = int(request.args.get('id',None))
        if not id:
            abort(400, 'Malformed request')
        if not db.exists('POST').where(id=id):
            abort(400, 'Malformed request')
        p = db.select('POST').where(id=id).execute()
        likes = text_list_to_set(p[4],process_f=lambda x:int(x))
        likes.add(u[0])
        likes = set_to_text_list(likes)
        db.update('POST').set(likes=likes).where(id=id).execute()
        return {
            'message': 'success'
        }

@dummy_posts.route('/unlike')
class Unlike(Resource):
    @dummy_posts.response(200, 'Success')
    @dummy_posts.response(400, 'Malformed Request')
    @dummy_posts.param('id','the id of the post to unlike')
    @dummy_posts.doc(description='''
        Identical to PUT /post/unlike but doesn't require any authentication
        Allows you to act as a "Anon" user.
    ''')
    def put(self):
        u = get_dummy_user()
        id = int(request.args.get('id',None))
        if not id or not db.exists('POST').where(id=id):
            abort(400, 'Malformed request')
        p = db.select('POST').where(id=id).execute()
        likes = text_list_to_set(p[4],process_f=lambda x: int(x))
        likes.discard(u[0])
        likes = set_to_text_list(likes)
        db.update('POST').set(likes=likes).where(id=id).execute()
        return {
            'message': 'success'
        }

@dummy_posts.route('/comment')
class Comment(Resource):
    @dummy_posts.response(200, 'Success')
    @dummy_posts.response(400, 'Malformed Request')
    @dummy_posts.param('id','the id of the post to comment on')
    @dummy_posts.expect(comment_details)
    @dummy_posts.doc(description='''
        Identical to PUT /comment but doesn't require any authentication
        Allows you to act as a "Anon" user.
    ''')
    def put(self):
        u = get_dummy_user()
        j = request.json
        id = int(request.args.get('id',None))
        if not id or not j:
            abort(400, 'Malformed request')
        if not db.exists('POST').where(id=id):
            abort(400, 'Malformed request')
        (comment,) = unpack(j,'comment')
        if comment == "":
            abort(400, 'Malformed request')
        comment_id = db.insert('COMMENT').with_values(
            comment=comment,
            author=u[1],
            published=str(time.time())
        ).execute()
        p = db.select('POST').where(id=id).execute()
        comment_list = text_list_to_set(p[7],process_f=lambda x: int(x))
        comment_list.add(comment_id)
        comment_list = set_to_text_list(comment_list)
        db.update('POST').set(comments=comment_list).where(id=id).execute()
        return {
            'message': 'success'
        }
