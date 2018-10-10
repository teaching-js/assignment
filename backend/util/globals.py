import secrets

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

def authorize(r):
    t = r.headers.get('Authorization',None)
    if not t:
        abort(405,'Unsupplied Authorization Token')
    try:
        t = t.split(" ")[1]
    except:
        abort(405,'Invalid Authorization Token')
    if not db.exists("USER").where(curr_token=t):
        abort(405,'Invalid Authorization Token')
    return db.select("USER").where(curr_token=t).execute()

def get_text_list(raw,process_f=lambda x:x):
    if raw == None:
        return set()
    return set([process_f(x) for x in raw.split(",") if x != ''])

def get_list_text(l):
    return ",".join([str(x) for x in l])

def format_post(post):
    comments = []
    for c_id in get_text_list(post[7],process_f=lambda x:int(x)):
        comment = db.select("COMMENT").where(id=c_id).execute()
        comments.append({
            "author":  comment[1],
            "published":  comment[2],
            "comment": comment[3]
        })
    return {
        "id": post[0],
        "meta": {
            "author": post[1],
            "description_text": post[2],
            "published": post[3],
            "likes": list(get_text_list(post[4],process_f=lambda x:int(x)))
        },
        "thumbnail": post[5],
        "src": post[6],
        "comments": comments
    }
