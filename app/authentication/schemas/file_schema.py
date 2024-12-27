from marshmallow import (
    validate,
    validates,
    validates_schema,
    ValidationError,
    post_dump,
)
from app import ma

class FileSchema(ma.Schema):
    class Meta:
        ordered = True

    url = ma.String(dump_only=True)
    _id = ma.String(dump_only=True)
    nom = ma.String(required=True)
class Photo_Full_Schema(ma.Schema):
    class Meta:
        ordered = True
    alt = ma.String()
    url = ma.String()