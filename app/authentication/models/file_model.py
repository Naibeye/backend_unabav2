
from flask import current_app, url_for
import uuid
import secrets
import mongoengine as me
from datetime import datetime, timedelta
from time import time
import jwt
from app import app
def gen_uuid():
    return uuid.uuid4().hex

class Updateable:
    def set_data(self, data):
        for attr, value in data.items():
            setattr(self, attr, value)
class File(Updateable, me.Document):
    _id = me.StringField(required=True,  primary_key=True, default=gen_uuid)
    ext = me.StringField(required=True, nullable=False)
    nom = me.StringField(required=True, nullable=False)

    @property
    def url(self):
        return url_for("files.get_file", uuid=self._id, _external=True)