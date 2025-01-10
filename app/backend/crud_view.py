import bson
from flask import Blueprint, abort
from apifairy import authenticate, body, response, other_responses
import time
from marshmallow import ValidationError
from mongoengine.queryset.visitor import Q
from app.auth import permission, token_auth
import urllib.parse
from app.backend.model import *
from app.authentication.schemas.crud_schema import CrudInSchema, CrudOutSchema
from app.authentication.schemas.user_schema import UserSchema
from app.backend.crud_schema import FaculteSchema, DepartementSchema, CategorieSchema, MatiereSchema, UeSchema,FiliereSchema, ProgrammeSchema
import json

from datetime import datetime, timedelta
##  SSO API 
crud_app = Blueprint("crud_app", __name__)
crudIn=CrudInSchema()
crudOut=CrudOutSchema()
crud_privileges={

    "Publication": {
        "POST": ["AP-101", "all"],
        "FILTER": ["AP-101", "all"],
        "GETALL": ["AP-102", "all"],
        "GET": ["AP-103", "all"],
        "PUT": ["AP-104", "all"],
        "DELETE": ["AP-101", "all"],
    },
    "Section": {
        "POST": ["AP-101", "all"],
        "FILTER": ["AP-101", "all"],
        "GETALL": ["AP-102", "all"],
        "GET": ["AP-103", "all"],
        "PUT": ["AP-104", "all"],
        "DELETE": ["AP-101", "all"],
    },
        "Matiere": {
        "POST": ["AP-101", "all"],
        "FILTER": ["AP-101", "all"],
        "GETALL": ["AP-102", "all"],
        "GET": ["AP-103", "all"],
        "PUT": ["AP-104", "all"],
        "DELETE": ["AP-101", "all"],
    },
        "Ue": {
        "POST": ["AP-101", "all"],
        "FILTER": ["AP-101", "all"],
        "GETALL": ["AP-102", "all"],
        "GET": ["AP-103", "all"],
        "PUT": ["AP-104", "all"],
        "DELETE": ["AP-101", "all"],
    },
      "Departement": {
        "POST": ["AP-101", "all"],
        "FILTER": ["AP-101", "all"],
        "GETALL": ["AP-102", "all"],
        "GET": ["AP-103", "all"],
        "PUT": ["AP-104", "all"],
        "DELETE": ["AP-101", "all"],
    },
       "Faculte": {
        "POST": ["AP-101", "all"],
        "FILTER": ["AP-101", "all"],
        "GETALL": ["AP-102", "all"],
        "GET": ["AP-103", "all"],
        "PUT": ["AP-104", "all"],
        "DELETE": ["AP-101", "all"],
    },
       "Filiere": {
        "POST": ["AP-101", "all"],
        "FILTER": ["AP-101", "all"],
        "GETALL": ["AP-102", "all"],
        "GET": ["AP-103", "all"],
        "PUT": ["AP-104", "all"],
        "DELETE": ["AP-101", "all"],
    },
       "Programme": {
        "POST": ["AP-101", "all"],
        "FILTER": ["AP-101", "all"],
        "GETALL": ["AP-102", "all"],
        "GET": ["AP-103", "all"],
        "PUT": ["AP-104", "all"],
        "DELETE": ["AP-101", "all"],
    },
      "Parti": {
        "POST": ["AP-101", "all"],
        "FILTER": ["AP-101", "all"],
        "GETALL": ["AP-102", "all"],
        "GET": ["AP-103", "all"],
        "PUT": ["AP-104", "all"],
        "DELETE": ["AP-101", "all"],
    },
     "TypeElection": {
        "POST": ["AP-101", "all"],
        "FILTER": ["AP-101", "all"],
        "GETALL": ["AP-102", "all"],
        "GET": ["AP-103", "all"],
        "PUT": ["AP-104", "all"],
        "DELETE": ["AP-101", "all"],
    },
      "Siege": {
        "POST": ["AP-101", "all"],
        "FILTER": ["AP-101", "all"],
        "GETALL": ["AP-102", "all"],
        "GET": ["AP-103", "all"],
        "PUT": ["AP-104", "all"],
        "DELETE": ["AP-101", "all"],
    },
      "Categorie": {
        "POST": ["AP-101", "all"],
        "FILTER": ["AP-101", "all"],
        "GETALL": ["AP-102", "all"],
        "GET": ["AP-103", "all"],
        "PUT": ["AP-104", "all"],
        "DELETE": ["AP-101", "all"],
    }
}
@crud_app.route("/hcrud", methods=["POST"])
@body(CrudInSchema)
@response(CrudOutSchema, 200)
@other_responses({401: "Donnees invalides" })
def function_crud(args):
    method=args["method"]
    collection=args["collection"]
    id=args["id"]
    body=args["body"]
    filter_req=args.get("req", {})
    @authenticate(token_auth)
    @permission(token_auth, privileges=crud_privileges[collection][method])
    def creation(collection, body):
        data=globals()[collection](**body, 
                                   created_by=token_auth.current_user())
        
        
        data.save()   
        return {"data": json.loads(data.to_json()), "message": "ok", "status":"200"}
    @authenticate(token_auth)
    @permission(token_auth, privileges=crud_privileges[collection][method])
    def get_all(collection):
        data=globals()[collection].objects()
        return {"data": json.loads(data.to_json()), "message": "ok", "status":"200"}
    # @permission(token_auth, privileges=crud_privileges[collection][method])
    def filter(collection,filter_req):
        data=globals()[collection].objects(**filter_req)
        return {"data": json.loads(data.to_json()), "message": "ok", "status":"200"}
    @authenticate(token_auth)
    @permission(token_auth, privileges=crud_privileges[collection][method])
    def get_by_id(collection, id):
        data=globals()[collection].objects(_id=bson.ObjectId(id)).first()
        
        if data:
            
            return {"data": [json.loads(data.to_json())][0], "message": "ok", "status":"200"}
        else:
            return {"data": [], "message": "Not found", "status":"401"}
    @authenticate(token_auth)
    @permission(token_auth, privileges=crud_privileges[collection][method])
    def update(collection, id, body):
        data=globals()[collection].objects(_id=bson.ObjectId(id)).first()
        entries_to_remove = ('created_by', 'updated_by', 'created_at', 'updated_at')
        for k in entries_to_remove:
            body.pop(k, None)
        if data:
            data.update(**body , updated_by=token_auth.current_user(), updated_at=datetime.now())

            return {"data": [json.loads(data.to_json())], "message": "ok", "status":"200"}
        else:
            return {"data": [], "message": "Not found", "status":"411"}
    @authenticate(token_auth)
    @permission(token_auth, privileges=crud_privileges[collection][method])
    def delete(collection, id):
        data=globals()[collection].objects(_id=bson.ObjectId(id)).first()
        data.delete()
        return {"data": [], "message": "ok", "status":"200"}
    match method:
        case "POST":
           return creation(collection, body)
        case "GET":
            return get_by_id(collection, id)
        case "GETALL":
            return get_all(collection)
        case "DELETE":
            return delete(collection, id)
        case "PUT":
            return update(collection, id, body)
        case "FILTER":
            return filter(collection, filter_req)
        case _:
           pass

@crud_app.route("/v2hcrud", methods=["POST"])
@body(CrudInSchema)
@other_responses({401: "Donnees invalides" })
def function_crudv2(args):
    method=args["method"]
    collection=args["collection"]
    id=args["id"]
    body=args["body"]
    filter_req=args.get("req", {})
    @authenticate(token_auth)
    @permission(token_auth, privileges=crud_privileges[collection][method])
    def creation(collection, body):
        try:
            data_in=globals()[f'{collection}Schema']().load(body)
        except ValidationError as error:
            print(error)
            abort(403, error.messages)
        data_in.created_by=token_auth.current_user()
        data_in.created_at=datetime.now()
        data_in.updated_at=datetime.now()
        data_in.updated_by=token_auth.current_user()
        data_in.save()
        # data=globals()[collection](**data_in.data, 
        #                            created_by=token_auth.current_user())
        
        # data.save()   
        
        return {"data": globals()[f'{collection}Schema']().dump(data_in), "message": "ok", "status":"200"}
    @authenticate(token_auth)
    @permission(token_auth, privileges=crud_privileges[collection][method])
    def get_all(collection):
        data=globals()[collection].objects()
        print(globals()[f'{collection.lower()}sSchema'].dump(data).data)
        return {"data": globals()[f'{collection}Schema'](many=True).dump(data), "message": "ok", "status":"200"}
    # @permission(token_auth, privileges=crud_privileges[collection][method])
    def filter(collection,filter_req):
        data=globals()[collection].objects(**filter_req)
        return {"data": globals()[f'{collection}Schema'](many=True).dump(data), "message": "ok", "status":"200"}
    @authenticate(token_auth)
    @permission(token_auth, privileges=crud_privileges[collection][method])
    def get_by_id(collection, id):
        data=globals()[collection].objects(_id=bson.ObjectId(id)).first()
        
        if data:
            
            return {"data": globals()[f'{collection}Schema']().dump(data).data, "message": "ok", "status":"200"}
        else:
            return {"data": [], "message": "Not found", "status":"401"}
    @authenticate(token_auth)
    @permission(token_auth, privileges=crud_privileges[collection][method])
    def update(collection, id, body):
        data=globals()[collection].objects(_id=bson.ObjectId(id)).first()
        entries_to_remove = ('created_by', 'updated_by', 'created_at', 'updated_at')
        for k in entries_to_remove:
            body.pop(k, None)

        try:
            data_in=globals()[f'{collection}Schema']().load(body)
        except ValidationError as error:
            abort(403, error.messages)
        print(data_in.__dict__)
        # data_in= globals()[f'{collection.lower()}Schema'].dump(data_in)
        if data_in:
            data_in.updated_at=datetime.now()
            data_in.updated_by=token_auth.current_user()
            data_in.created_at=data.created_at
            data_in.created_by=data.created_by
            data_in.save()
            return {"data": globals()[f'{collection}Schema']().dump(data_in), "message": "ok", "status":"200"}
        else:
            return {"data": [], "message": "Not found", "status":"411"}
    @authenticate(token_auth)
    @permission(token_auth, privileges=crud_privileges[collection][method])
    def delete(collection, id):
        data=globals()[collection].objects(_id=bson.ObjectId(id)).first()
        data.delete()
        return {"data": [], "message": "ok", "status":"200"}
    match method:
        case "POST":
           return creation(collection, body)
        case "GET":
            return get_by_id(collection, id)
        case "GETALL":
            return get_all(collection)
        case "DELETE":
            return delete(collection, id)
        case "PUT":
            return update(collection, id, body)
        case "FILTER":
            return filter(collection, filter_req)
        case _:
           pass