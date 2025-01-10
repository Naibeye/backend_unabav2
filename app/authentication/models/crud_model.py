import uuid
import secrets
import mongoengine as me
from datetime import datetime, timedelta
from time import time
import jwt
from app import app
from app.authentication.models.user_model import User
from app.authentication.schemas.user_schema import UserSchema

def gen_uuid():
    return uuid.uuid4().hex
class Updateable:
    def set_data(self, data):
        for attr, value in data.items():
            setattr(self, attr, value)
class CollectionTemplate(me.DynamicDocument):
    created_at = me.DateTimeField()
    updated_at = me.DateTimeField()
    created_by = me.ReferenceField(User, reverse_delete_rule=me.DENY)
    updated_by = me.ReferenceField(User, reverse_delete_rule=me.DENY)
    meta = { 'abstract': True}
    
    
