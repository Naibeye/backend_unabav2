import json
from marshmallow import (
    validate,
    validates,
    validates_schema,
    ValidationError,
    post_dump,
)
from marshmallow_jsonschema import JSONSchema
from app import ma
from marshmallow import fields
from marshmallow_mongoengine import ModelSchema

from app.authentication.schemas.user_schema import UserSchema
from app.backend.model import Faculte, Categorie

class CrudInSchema(ma.Schema):
    class Meta:
        ordered = True
    method = ma.String(required=True)
    collection = ma.String(required=True)
    id= ma.String()
    body = ma.Dict()
    req = ma.Dict()
class CrudOutSchema(ma.Schema):
    class Meta:
        ordered = True
    data =ma.List(ma.Dict)
    message= ma.String(required=True)
    status = ma.String()
class FaculteSchema(ModelSchema):
    class Meta:
        model=Faculte
    abr= ma.String(required=True)
    code= ma.String(required=True)
    faculte= ma.String(required=True)
class CategorieSchema(ModelSchema):
    class Meta:
        model=Categorie
    abr= ma.String(required=True)
    code= ma.String(required=True)
    libelle= ma.String(required=True)
    created_at= ma.String(dump_only=True)
    updated_at = ma.String(dump_only=True)
    created_by=ma.Nested(UserSchema, dump_only=True)
    updated_by=ma.Nested(UserSchema, dump_only=True)