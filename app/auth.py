import json
from bson import ObjectId
from flask import current_app
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from werkzeug.exceptions import Unauthorized, Forbidden
from functools import wraps
from flask import abort
from app import db
from app.authentication.models import User, Role


token_auth = HTTPTokenAuth()


@token_auth.verify_token
def verify_token(access_token):
    if access_token:
        return User.verify_access_token(access_token)


@token_auth.error_handler
def token_auth_error(status=401):
    error = (Forbidden if status == 403 else Unauthorized)()
    return {
        "code": error.code,
        "message": error.name,
        "description": error.description,
    }, error.code
def permission(token_auth, privileges=[]):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user=token_auth.current_user()
            
            role=Role.objects(_id=ObjectId(user.role.id)).first()
            tab=set(role.privileges).intersection(set(privileges))
            if len(tab)==0 and len(privileges)==0:
                abort(401)
            return f(*args, **kwargs)
        return decorated_function

    return decorator
def format_out(many=False):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data=f(*args, **kwargs)
            data=data["data"]
            created_at=data.created_at
            created_by=User.objects(data.created_by).first() 
            return {**json.loads(data.to_json())}
        return decorated_function

    return decorator