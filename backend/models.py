from globals import api
from flask_restplus import fields

comment_details = api.model('comment_details',{
    "author": fields.String(),
    "published": fields.String(),
    "comment": fields.String()
})
post_meta_details = api.model('post_meta_details',{
    "author": fields.String(),
    "description_text": fields.String(),
    "published": fields.String(),
    "likes": fields.List(fields.Integer()),
    "comments": fields.List(fields.Nested(comment_details))
})

post_details = api.model('post_details',{
  "id": fields.Integer(),
  "meta": fields.Nested(post_meta_details),
  "thumbnail": fields.String(),
  "src": fields.String()
})

new_post_details = api.model('new_post_details',{
  "description_text": fields.String(required=True, example='i had a fun time!'),
  "src": fields.String(required=True, example='image src base64 encoded')
})

post_list_details = api.model('post_list_details',{
    "posts" : fields.List(fields.Nested(post_details))
})

login_details = api.model('login_details', {
  'username': fields.String(required=True, example='xX_greginator_Xx'),
  'password': fields.String(required=True, example='1234'),
})

comment_details = api.model('comment_details', {
  'comment': fields.String(required=True, example='Cute photo!')
})

user_details = api.model('user_details', {
    'id': fields.Integer(min=0),
    'username': fields.String(example='xX_greginator_Xx'),
    'email': fields.String(example='greg@fred.com'),
    'name':  fields.String(example='greg'),
    'posts': fields.List(fields.Nested(post_details)),
    'following': fields.List(fields.Integer(min=0))
})
user_update_details = api.model('user_update_details', {
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
