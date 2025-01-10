import json
from bson import ObjectId
from marshmallow import (
    post_load,
    pre_dump,
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
from app.backend.model import Cycle, Departement, Faculte, Categorie, Filiere, Matiere, Niveau, Programme, Ue

class FaculteSchema(ModelSchema):
    class Meta:
        model=Faculte
    id= ma.String()
    abr= ma.String(required=True)
    code= ma.String(required=True)
    faculte= ma.String(required=True)
    fichier_full=ma.Dict()
    # departements = ma.List(ma.Nested(DepartementSchema(exclude=("faculte",))), dump_only=True)
    # @pre_dump
    # def departement_out(sel, data, **kwargs):
    #     data['departements']=Departement.objects(faculte=ObjectId(data.id))
    #     return data
class DepartementSchema(ModelSchema):
    class Meta:
        model=Departement
    abr= ma.String(required=True)
    code= ma.String(required=True)
    departement= ma.String(required=True)
    # faculte_id= ma.String(required=True)
    faculte=ma.Nested(FaculteSchema)
    created_by=ma.Nested(UserSchema, dump_only=True)
    updated_by=ma.Nested(UserSchema, dump_only=True)
    @pre_load
    def faculte_set(self, data, **kwargs):
        faculte_id=data['faculte_id']
        data.pop('faculte_id', None)
        data.pop('faculte', None)
        faculteSchema=FaculteSchema()
        faculte=Faculte.objects(_id=ObjectId(faculte_id)).first()
        data['faculte']=faculteSchema.dump(faculte)
        return data
    
    @post_dump
    def faculte_out(sel, data, **kwargs):
        data['faculte_id']=data['faculte']['id']
        return data
class FiliereSchema(ModelSchema):
    class Meta:
        model=Filiere
    abr= ma.String(required=True)
    code= ma.String(required=True)
    libelle= ma.String(required=True)
    presentation= ma.String(required=True)
    cycle=ma.String(required=True)
    faculte=ma.Nested(FaculteSchema)
    created_by=ma.Nested(UserSchema, dump_only=True)
    updated_by=ma.Nested(UserSchema, dump_only=True)
    @pre_load
    def faculte_set(self, data, **kwargs):
        faculte_id=data['faculte_id']
        data.pop('faculte_id', None)
        data.pop('faculte', None)
        faculteSchema=FaculteSchema()
        faculte=Faculte.objects(_id=ObjectId(faculte_id)).first()
        data['faculte']=faculteSchema.dump(faculte)
        return data
    
    @post_dump
    def faculte_out(sel, data, **kwargs):
        data['faculte_id']=data['faculte']['id']
        return data

class MatiereSchema(ModelSchema):
    class Meta:
        model=Matiere
    code= ma.String(required=True)
    libelle= ma.String(required=True)
    credit=ma.Float(required=True)
    coefficient=ma.Float(equired=True)
    created_by=ma.Nested(UserSchema)
    updated_by=ma.Nested(UserSchema)
class UeSchema(ModelSchema):
    class Meta:
        model=Ue
    code= ma.String(required=True)
    libelle= ma.String(required=True)
    credit=ma.Float(dump_only=True)
    coefficient=ma.Float(dump_only=True)
    created_by=ma.Nested(UserSchema, dump_only=True)
    updated_by=ma.Nested(UserSchema, dump_only=True)
    matieres_id=ma.List(ma.Dict(), load_only=True)
    matieres=ma.List(ma.Nested(MatiereSchema), dump_only=True)
    credit=ma.Float(dump_only=True)
    coefficient=ma.Float(dump_only=True)
    @pre_load
    def matiere_pre(self, data, **kwargs):
        data.pop('matieres', None)
        data.pop('coefficient', None)
        data.pop('credit', None)
        return data
    @post_load
    def matiere_post(self, data, **kwargs):
        matieres=data['matieres_id']
        items=Matiere.objects(_id__in=[ObjectId(item['value']) for item in matieres])
        data['matieres']=items
        return data
    # @post_dump
    # def matieres_out(sel, data, **kwargs):
    #     data['matieres']=data['faculte']['id']
    #     return data
class ProgrammeSchema(ModelSchema):
    class Meta:
        model=Programme
    # filiere_id= ma.String(dump_only=True)
    filiere=ma.Nested(FiliereSchema, required=True)
    semestre=ma.String(required=True)
    niveau=ma.String(required=True)
    ues_id=ma.List(ma.Dict(), load_only=True)
    ues=ma.List(ma.Nested(UeSchema), dump_only=True)
    created_by=ma.Nested(UserSchema, dump_only=True)
    updated_by=ma.Nested(UserSchema, dump_only=True)

    # credit=ma.Float(dump_only=True)
    # coefficient=ma.Float(dump_only=True)
    @pre_load
    def programme_pre(self, data, **kwargs):
        data.pop('ues', None)
        filiere_id=data['filiere_id']
        data.pop('filiere_id', None)
        data.pop('filiere', None)
        filiereSchema=FiliereSchema()
        filiere=Filiere.objects(_id=ObjectId(filiere_id)).first()
        data['filiere']=filiereSchema.dump(filiere)
        data['filiere'].pop('updated_by', None)
        data['filiere'].pop('created_by', None)
        return data
    @post_load
    def programme_post(self, data, **kwargs):
        ues=data['ues_id']
        items=Ue.objects(_id__in=[ObjectId(item['value']) for item in ues])
        data['ues']=items
        return data
    @post_dump
    def filiere_set(self, data, **kwargs):
        data['filiere_id']=data['filiere']['id']
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