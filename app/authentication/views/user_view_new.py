from datetime import datetime
import secrets
from flask import Blueprint, abort
from apifairy import authenticate, body, response, other_responses
from app.authentication.models.user_model import gen_uuid
from app import db
from app.authentication.schemas import UserSchema,LoginNewSchema, RegistrationSchema, SessionSchema, TokenSchema, LoginSchema, SessionTokenSchema
from app.authentication.schemas.user_schema import PrivilegeSchema
from app.lib.authentication import Authentication
from flask import current_app, render_template, jsonify, request
from ellipticcurve.privateKey import PrivateKey
from ellipticcurve.publicKey import PublicKey
import json
from app import app
from app.mail import send_email
from marshmallow import Schema, fields, ValidationError
from ..models import User, Session, Role
from app.lib import OTP, string_to_base64, base64_to_string, Authentication
from flask import Blueprint, abort
from apifairy import authenticate, body, response, other_responses
import time
from mongoengine.queryset.visitor import Q
from app.auth import permission, token_auth
import urllib.parse
from werkzeug.security import generate_password_hash


##  SSO API 
usernew = Blueprint("usernew", __name__)
userSchema=UserSchema()
registrationSchema = RegistrationSchema()
login_new_schema=LoginNewSchema()
usersSchema=UserSchema(many=True)
privileges_schema = PrivilegeSchema(many=True)
sessionTokenSchema=SessionTokenSchema
@usernew.route("/utilisateurs", methods=["POST"])
@body(registrationSchema)
# @response(userSchema, 201)
@other_responses({401: "Compte existe deja", 400: "Donnees invalides"})
def new(args):
    """Register a new utilisateur"""
    try:
        data = RegistrationSchema().load(args)
    except ValidationError as err:
        return abort(400)
    user=User.objects(mail=data.get("mail")).first()
    if user:
        return abort(401)

    else:
        guest_role=Role.objects(code="RO-002").first()
        motpasse=data['motpasse']
        del data['motpasse']
        user=User(**data, role_id=guest_role['_id'], motpasse_hash=generate_password_hash(motpasse))
        reset_jwt=user.generate_reset_token()
        user.save()
        link= f"http://{app.config['FRONTEND_URL']}/api/validation/{reset_jwt}"
        send_email(to=data['mail'], subject="Compte validation", template=render_template("reset_id.html", **{**data, "url":link}))
        return  {"token": None}
@usernew.route("/newlogin", methods=["POST"])
@body(login_new_schema)
@response(sessionTokenSchema, 200)
@other_responses({401: "Invalid mail or password"})
def login(args):
    """Creer une nouvelle connection

    The refresh token is also returned as a hardened cookie, in case the
    client is running in an insecure environment such as a web browser, and
    cannot securely store the token.
    """
    # user = basic_auth.current_user()
    try:
        data = LoginNewSchema().load(args)
    except ValidationError as err:
        return abort(400)
    mail = data["mail"]
    motpasse = data["motpasse"]
    if mail and motpasse:
        utilisateur = User.objects(Q(mail=data.get("mail")) & Q(is_validate=True) & Q(status=True)  ).first()
        if utilisateur and utilisateur.verifier_motpasse(motpasse):
            token = utilisateur.generate_auth_token()
            token.save()
            return {"token":token.access_token, "nom": utilisateur.nom, "mail":utilisateur.mail, "photo_full": utilisateur.photo_full}
        else:
            abort(401)
    else:
        abort(401)