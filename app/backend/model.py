from enum import Enum
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
class Matiere(CollectionTemplate, Updateable):
    departements=me.ListField(me.ReferenceField('Departement'))
    @property
    def id(self):
        return self._id
    @property
    def modifier_par(self):
        return self.created_at
class Ue(CollectionTemplate, Updateable):
    matieres=me.ListField(me.ReferenceField(Matiere, reverse_delete_rule=me.DENY))
    @property
    def id(self):
        return self._id
    @property
    def credit(self):
        return sum([matiere.credit for matiere in self.matieres])
    @property
    def coefficient(self):
        return sum([matiere.credit for matiere in self.matieres])
    @property
    def modifier_par(self):
        return self.created_at
class Faculte(CollectionTemplate, Updateable):
    departements=me.ListField(me.ReferenceField('Departement'))
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
class Cycle(Enum):
    L = 'L'
    M = 'M'
    D = 'D'
class Niveau(Enum):
    L1 = 'L1'
    L2 = 'L2'
    L3 = 'L3'
    M1 = 'M1'
    M2 = 'M2'
    D1 = 'D1'
class Semestre(Enum):
    S1 = 'S1'
    S2 = 'S2'
class Filiere(CollectionTemplate, Updateable):
    faculte = me.ReferenceField(Faculte, reverse_delete_rule=me.DENY)
    # cycle = me.EnumField(Cycle,  required=True)
    @property
    def modifier_par(self):
        return self.created_at
    @property
    def id(self):
        return self._id
class Programme(CollectionTemplate, Updateable):
    filiere = me.ReferenceField(Filiere, reverse_delete_rule=me.DENY)
    # niveau = me.EnumField(Niveau, required=True)
    # semestre = me.EnumField(Semestre, required=True)
    ues=me.ListField(me.ReferenceField(Ue, reverse_delete_rule=me.DENY))
    def id(self):
        return self._id
class Categorie(CollectionTemplate, Updateable):
    @property
    def modifier_par(self):
        return self.created_at
    @property
    def id(self):
        return self._id