from datetime import datetime
import secrets
from flask import Blueprint, abort
from apifairy import authenticate, body, response, other_responses
from app.authentication.models.user_model import gen_uuid
from app import db
from app.authentication.schemas import UserSchema, SessionSchema, TokenSchema, LoginSchema, SessionTokenSchema
from app.authentication.schemas.user_schema import PrivilegeSchema
from app.lib.authentication import Authentication
from flask import current_app, render_template, jsonify, request
from ellipticcurve.privateKey import PrivateKey
from ellipticcurve.publicKey import PublicKey
import json
from app import app
from app.mail import send_email
from marshmallow import Schema, fields, ValidationError
from ..models import User, Session
from app.lib import OTP, string_to_base64, base64_to_string, Authentication
from flask import Blueprint, abort
from apifairy import authenticate, body, response, other_responses
import time
from mongoengine.queryset.visitor import Q
from app.auth import permission, token_auth
import urllib.parse



##  SSO API 
user = Blueprint("user", __name__)
userSchema=UserSchema()
usersSchema=UserSchema(many=True)
privileges_schema = PrivilegeSchema(many=True)

@user.route("/protect", methods=["GET"])
@authenticate(token_auth)
@permission(token_auth, privileges=["AP-101"])
@other_responses({401: "Role non trouvée"})
def protect():
    """
      protect
    The function `protect` returns a JSON response with a status code of 200 and user information
    extracted from a token-authenticated current user.
    :return: The `protect` function is returning a JSON response with a status code of 200 and the user
    information extracted from the current user's JSON representation.
    """
    return jsonify({"status": 200 , "user": json.loads(token_auth.current_user().to_json())})
@user.route("/validation/<string:jwt_token>", methods=["GET"])
@other_responses({401: "Role non trouvée"})
def validation(jwt_token):
    """
      validates a JWT token 
    The function validates a JWT token by verifying a user's reset token and returns a status code or
    aborts with a 401 error.
    
    :param jwt_token: The `jwt_token` parameter in the `validation` function is a JSON Web Token (JWT)
    that is used for verifying the identity of a user. The function attempts to verify the JWT token by
    calling the `verify_reset_token` method on the `User` class. If the verification is successful
    :return: a JSON response with a status code of 200 if the user is successfully verified using the
    JWT token. If the user cannot be verified, it will abort the request with a status code of 401.
    """
    user=User.verify_reset_token(jwt_token)
    if user: 
        return jsonify({"status": 200})
    else:
        abort(401)
@user.route("/registration", methods=["POST"])
@body(userSchema)
@response(SessionTokenSchema, 201)
@other_responses({401: "Donnees invalides", 200: "Attente de validation du mail" })
def regitration(args):
    """
      registration
    This Python function handles user registration, including validation of user data and sending
    validation emails.
    
    :param args: It seems like you forgot to provide the actual arguments for the `registration`
    function. Could you please provide the arguments that are passed to the `registration` function so
    that I can assist you further with understanding the code?
    :return: The function `registration` returns a dictionary containing user data and a token. The
    structure of the dictionary returned depends on the conditions met within the function:
    """
    try:
        data = UserSchema().load(args)
    except ValidationError as err:
        return abort(401)
    user=User.objects(mail=data.get("mail")).first()
    if user:
        if user.naibi_id==data["naibi_id"]:
            token =gen_uuid()
            session=Session()
            session.init(user._id, token)
            session.save()
            return  {**json.loads(user.to_json()), "token": session['access_token']}
        else:
            reset_jwt=user.generate_reset_token(data["naibi_id"])
            user.is_validate_naibi_id=False
            link= f"http://{app.config['FRONTEND_URL']}/api/validation/{reset_jwt}"
            send_email(to=data['mail'], subject="Compte validation", template=render_template("reset_id.html", **{**data, "url":link}))
            return  {**json.loads(user.to_json()), "token": None}

    else:
        user=User(**data)
        reset_jwt=user.generate_reset_token(data["naibi_id"])
        user.save()
        link= f"http://{app.config['FRONTEND_URL']}/api/validation/{reset_jwt}"
        send_email(to=data['mail'], subject="Compte validation", template=render_template("reset_id.html", **{**data, "url":link}))
        return  {**json.loads(user.to_json()), "token": None}
        
@user.route("/login", methods=["POST"])
@body(LoginSchema)
@response(SessionTokenSchema, 201)
@other_responses({401: "Donnees invalides"})
def login(args):
    """
      login
    The `login` function in the provided Python code handles user authentication, verification, and
    session management based on the input data.
    
    :param args: It seems like the code snippet you provided is a Python function for handling user
    login logic. The function takes a parameter `args`, which seems to be the input data for the login
    process
    :return: The code snippet provided is a Python function named `login` that seems to handle user
    authentication and session management.
    """
    try:
        
        try:
            data = LoginSchema().load(args)
        except ValidationError as err:
            return abort(401)
        data= Authentication.verify(data, app.config['SECRET_CRT'], app.config['CRT_NAIBI'])
        if data:
            user =User.objects(mail=data['proverIdentity']['mail']).first()
            if user:
                if user.naibi_id==data['_id'] and user.is_validate_naibi_id:
                    token =gen_uuid()
                    session=Session()
                    session.init(user, token)
                    session.save()
                    return  {**json.loads(user.to_json()), "token": session['access_token']}
                else:
                    reset_jwt=user.generate_reset_token(data['_id'])
                    user.is_validate_naibi_id=False
                    link= f"http://{app.config['FRONTEND_URL']}/api/validation/{reset_jwt}"
                    send_email(to=user.mail, subject="Compte validation", template=render_template("reset_id.html", **{**data, "url":link}))
                    return  {**json.loads(user.to_json()), "token": None}
            else:
                user=User(naibi_id=data['_id'], nom=data['proverIdentity']['name'], mail=data['proverIdentity']['mail'])
                reset_jwt=user.generate_reset_token(data["_id"])
                user.save()
                link= f"http://{app.config['FRONTEND_URL']}/api/validation/{reset_jwt}"
                send_email(to=user.mail, subject="Compte validation", template=render_template("reset_id.html", **{"nom":data['proverIdentity']['name'], "url":link}))
                return  {**json.loads(user.to_json()), "token": None}
        else:
            return abort(401)
    except ValidationError as err:
        return abort(401)
@user.route("/session", methods=["GET"])
@response(SessionSchema, 200)
def session_init():
    return  {"SESSION":"d8ab19560a3e45a8bffd613f60e9d230", "ID_NAIBI": app.config['ID_NAIBI'] }
@user.route("/session/<session_id>", methods=["GET"])
@response(SessionTokenSchema, 200)
@other_responses({404: "Session invalides"})
def session_token(session_id):
    """
    session_token

    The function `session_token` retrieves user information and access token based on a session ID after
    waiting for the session to be available for up to 60 seconds.
    
    :param session_id: The `session_id` parameter is used to identify a specific session in the
    `Session` collection. The function `session_token` is designed to retrieve information related to
    the session identified by the `session_id`. It continuously checks for the session's existence and
    waits for a maximum of 60 seconds before
    :return: a dictionary with keys "token", "nom", and "mail" along with their corresponding values.
    The values are fetched from the session and user objects based on the provided session_id.
    """
    session=None
    cumul_time=0
   
    while session or cumul_time<60:
        session=Session.objects(_id=session_id).first()
        time.sleep(1)
        cumul_time+=1
        if session: 
            if User.verify_access_token(session.access_token):
                user =User.objects(_id=session.user_id).first()
                return  {"token":session.access_token, "nom": user.nom, "mail":user.mail, "photo_full": user.photo_full}
    abort(404)
@user.route("/privileges", methods=["GET"])
# @authenticate(token_auth)
@response(privileges_schema)
def listeprivilege():
    """
    listeprivilege
    The function `listeprivilege` returns a list of privileges stored in the app configuration.
    :return: The function `listeprivilege()` is returning the value of `app.config["PRIVILEGES"]`, which
    presumably contains a list of privileges.
    """
    "Liste des privileges"
    return app.config["PRIVILEGES"]