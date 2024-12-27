from flask import Blueprint, abort
from apifairy import authenticate, body, response, other_responses
import time
from mongoengine.queryset.visitor import Q
from app.auth import permission, token_auth
import urllib.parse
from app.authentication.models.crud_model import *
from app.authentication.models.user_model import *
from app.authentication.schemas.crud_schema import CrudInSchema, CrudOutSchema
import json


##  SSO API 
crud = Blueprint("crud", __name__)
crudIn=CrudInSchema()
crudOut=CrudOutSchema()
crud_privileges={
    "User": {
        "POST": ["AP-101", "all"],
        "GETALL": ["AP-102", "all"],
        "GET": ["AP-103", "all"],
        "PUT": ["AP-104", "all"],
        "DELETE": ["AP-101", "all"],
    },
    "Role": {
        "POST": ["AP-101", "all"],
        "GETALL": ["AP-102", "all"],
        "GET": ["AP-103", "all"],
        "PUT": ["AP-104", "all"],
        "DELETE": ["AP-101", "all"],
    },
    "TypeChambre": {
        "POST": ["AP-101", "all"],
        "GETALL": ["AP-102", "all"],
        "GET": ["AP-103", "all"],
        "PUT": ["AP-104", "all"],
        "DELETE": ["AP-101", "all"],
    }
}
@crud.route("/crud", methods=["POST"])
@authenticate(token_auth)
@body(CrudInSchema)
@response(CrudOutSchema, 200)
@other_responses({401: "Donnees invalides" })
def function_crud(args):
    method=args["method"]
    collection=args["collection"]
    id=args["id"]
    body=args["body"]
    @permission(token_auth, privileges=crud_privileges[collection][method])
    def creation(collection, body):
        print("========>",body)
        data=globals()[collection](**body, 
                                   created_by=token_auth.current_user()["_id"])
        data.save() 
        print("========>",data)  
        return {"data": [json.loads(data.to_json())], "message": "ok", "status":"200"}
    @permission(token_auth, privileges=crud_privileges[collection][method])
    def get_all(collection):
        data=globals()[collection].objects()
        return {"data": json.loads(data.to_json()), "message": "ok", "status":"200"}
    @permission(token_auth, privileges=crud_privileges[collection][method])
    def get_by_id(collection, id):
        data=globals()[collection].objects(_id=id).first()
        
        if data:
            
            return {"data": [json.loads(data.to_json())], "message": "ok", "status":"200"}
        else:
            return {"data": [], "message": "Not found", "status":"401"}
    @permission(token_auth, privileges=crud_privileges[collection][method])
    def update(collection, id, body):
        data=globals()[collection].objects(_id=id).first()
        if data:

            data.update(**body, updated_by=token_auth.current_user()["_id"], updated_at=datetime.now() )
            return {"data": [json.loads(data.to_json())], "message": "ok", "status":"200"}
        else:
            return {"data": [], "message": "Not found", "status":"411"}
    @permission(token_auth, privileges=crud_privileges[collection][method])
    def delete(collection, id):
        data=globals()[collection].objects(_id=id).first()
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
        case _:
           pass
