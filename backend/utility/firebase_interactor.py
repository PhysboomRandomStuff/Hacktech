from functools import wraps

import pyrebase
import firebase_admin
from firebase_admin import credentials, auth
import json

firebase_config = {
    "apiKey": "AIzaSyA4g9K1pbbd4zNkKoGKVc6Q5Jo4V44gatg",
    "authDomain": "hacktechvocab.firebaseapp.com",
    "databaseURL": "https://hacktechvocab-default-rtdb.firebaseio.com/",
    "storageBucket": "hacktechvocab.appspot.com",
    "serviceAccount": "firebase-conf.json",
}

cred = credentials.Certificate(firebase_config["serviceAccount"])
firebase = firebase_admin.initialize_app(cred)

pb = pyrebase.initialize_app(firebase_config)
database = pb.database()
pbauth = pb.auth()

def check_token(request):
    def check_token_decorator(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if not request.headers.get('authorization'):
                return json.dumps({"success": False, "error": 'No token provided'})
            try:
                user = auth.verify_id_token(request.headers['authorization'])
                request.user = user

            except:
                return json.dumps({"success": False, "error": 'Invalid token provided'})
            return f(*args, **kwargs)

        return wrap

    return check_token_decorator


def noquote(s, safe=None):
    return s

def verify_id_token(id_token):
    try:
        return {"success": True, "data": auth.verify_id_token(id_token)}
    except:
        return {"success": False, "error": "Invalid token"}

# Push an object to the database
def push_object(path, data, load_json=True):
    db = pb.database()
    db.child(path).set(json.loads(data) if load_json else data)


# Get an object from the database
def get_object(path, query_dict={}):
    top = database
    for key in path.split("/"):
        top = top.child(key)
    methdict = {
        "order_by_child": top.order_by_child,
        "limit_to_first": top.limit_to_first,
        "limit_to_last": top.limit_to_last,
        "start_at": top.start_at,
        "end_at": top.end_at,
    }
    typedict = {
        "order_by_child": str,
        "limit_to_first": int,
        "limit_to_last": int,
        "start_at": noquote,
        "end_at": noquote,
    }
    for key in query_dict.keys():
        try:
            top = methdict[key](typedict[key](query_dict[key]))
        except Exception as e:
            print(e)
    return top.get().val()

def login(email, password):
    try:
        user = pbauth.sign_in_with_email_and_password(email, password)
        return {"success": True, "id_token": user["idToken"], "uuid": user["localId"], "refresh_token": user["refreshToken"]}
    except:
        return {"success": False, "error": "Invalid credentials"}

def register_user(email, password):
    try:
        user = pbauth.create_user_with_email_and_password(email, password)
        return {"success": True, "message": "Registered successfully!", "id_token": user["idToken"], "uuid": user["localId"], "refresh_token": user["refreshToken"]}
    except:
        return {"success": False, "error": "User already exists or is invalid"}