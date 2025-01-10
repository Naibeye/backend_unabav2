from marshmallow import (
    validate,
    validates,
    validates_schema,
    ValidationError,
    post_dump,
)
from app import ma
from app.authentication.schemas.file_schema import FileSchema, Photo_Full_Schema
class RegistrationSchema(ma.Schema):
    class Meta:
        ordered = True
    nom = ma.String(required=True)
    mail = ma.String(
        required=True, validate=[validate.Length(max=120), validate.Email()]
    )
    prenom= ma.String()
    motpasse = ma.String(required=True)
class LoginNewSchema(ma.Schema):
    class Meta:
        ordered = True
    mail = ma.String(
        required=True, validate=[validate.Length(max=120), validate.Email()]
    )
    motpasse = ma.String(required=True)
class UserSchema(ma.Schema):
    class Meta:
        ordered = True
    nom = ma.String(required=True)
    mail = ma.String(
        required=True, validate=[validate.Length(max=120), validate.Email()]
    )
    prenom= ma.String()
    photo_full=ma.Nested(Photo_Full_Schema)
class SessionSchema(ma.Schema):
    class Meta:
        ordered = True
    SESSION = ma.String(required=True)
    ID_NAIBI = ma.String(required=True)
class TokenSchema(ma.Schema):
    class Meta:
        ordered = True
    token = ma.String(required=True)
class LoginSchema(ma.Schema):
    class Meta:
        ordered = True
    data = ma.String(required=True)
    publicKeyEp =ma.String(required=True)
class SessionTokenSchema(ma.Schema):
    class Meta:
        ordered = True
    nom = ma.String(required=True)
    mail = ma.String(
        required=True,dumps_only=True
    )
    prenom= ma.String()
    token =ma.String(required=True, dumps_only=True)
    photo_full=ma.Nested(Photo_Full_Schema)
class PrivilegeSchema(ma.Schema):
    class Meta:
        ordered = True
    value = ma.String(required=True)
    label = ma.String(required=True)
    children = ma.Nested("PrivilegeSchema", dump_only=True, many=True)