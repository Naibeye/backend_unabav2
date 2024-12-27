import json
from bson import ObjectId
from marshmallow import (
    pre_load,
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
from app.backend.model import Departement, Faculte, Categorie

class FaculteSchema(ModelSchema):
    class Meta:
        model=Faculte
    id= ma.String(required=True)
    abr= ma.String(required=True)
    code= ma.String(required=True)
    faculte= ma.String(required=True)
class DepartementSchema(ModelSchema):
    class Meta:
        model=Departement
    abr= ma.String(required=True)
    code= ma.String(required=True)
    departement= ma.String(required=True)
    faculte=ma.Nested(FaculteSchema)
    @pre_load
    def process_author(self, data, **kwargs):
        faculte_id=data['faculte_id']
        faculteSchema=FaculteSchema()
        faculte=Faculte.objects(_id=ObjectId(faculte_id)).first()
        print(faculteSchema.dump(faculte))

        data['faculte']=faculteSchema.dump(faculte)
        data.pop('faculte_id', None)
        return data

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