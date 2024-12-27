from bson import ObjectId
from flask import current_app
import uuid
import secrets
import mongoengine as me
from datetime import datetime, timedelta
from time import time
import jwt
from app import app
from app.authentication.models.crud_model import CollectionTemplate
from app.authentication.models.user_model import User
from app.authentication.schemas.user_schema import UserSchema
def gen_uuid():
    return uuid.uuid4().hex

class Updateable:
    def set_data(self, data):
        for attr, value in data.items():
            setattr(self, attr, value)

class Section(me.DynamicDocument, Updateable):
    _id = me.StringField(required=True, primary_key=True, default=gen_uuid)
    @property
    def modifier_par(self):
        return self.created_at
class Province(me.DynamicDocument, Updateable):
    _id = me.StringField(required=True, primary_key=True, default=gen_uuid)
    @property
    def modifier_par(self):
        return self.created_at
class Departement(me.DynamicDocument, Updateable):
    _id = me.StringField(required=True, primary_key=True, default=gen_uuid)
    @property
    def modifier_par(self):
        return self.created_at
class Parti(me.DynamicDocument, Updateable):
    _id = me.StringField(required=True, primary_key=True, default=gen_uuid)
    @property
    def modifier_par(self):
        return self.created_at
class TypeElection(me.DynamicDocument, Updateable):
    _id = me.StringField(required=True, primary_key=True, default=gen_uuid)
    @property
    def modifier_par(self):
        return self.created_at
class Siege(me.DynamicDocument, Updateable):
    _id = me.StringField(required=True, primary_key=True, default=gen_uuid)
    @property
    def modifier_par(self):
        return self.created_at
class Publication(CollectionTemplate, Updateable):
    _id = me.StringField(required=True, primary_key=True, default=gen_uuid)
    @property
    def modifier_par(self):
        return self.created_at
class Faculte(CollectionTemplate, Updateable):

    @property
    def id(self):
        return self._id
    @property
    def modifier_par(self):
        return self.created_at
class Departement(CollectionTemplate, Updateable):
    faculte = me.ReferenceField(Faculte, reverse_delete_rule=me.DENY)

        
        
    @property
    def modifier_par(self):
        return self.created_at
    @property
    def id(self):
        return self._id
class Categorie(CollectionTemplate, Updateable):
    @property
    def modifier_par(self):
        return self.created_at
    @property
    def id(self):
        return self._id
    # @property
    # def created_by(self):
    #     userSchema=UserSchema()
    #     print("Herrrrrr===========W",self._created_by)
    #     return self._created_by
    # @created_by.setter
    # def created_by(self, created_by):
    #     self._created_by=ObjectId(created_by.id)
   
    # @property
    # def updated_by(self):
    #     userSchema=UserSchema()
    #     return self._updated_by
    # @updated_by.setter
    # def updated_by(self, updated_by):
    #     self._created_by=ObjectId(updated_by.id)