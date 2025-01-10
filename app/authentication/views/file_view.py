"""
Welcome to the documentation for the Microblog API!

This project is written in Python, with the
[Flask](https://flask.palletsprojects.com/) web framework. This documentation
is generated automatically from the
[project's source code](https://github.com/miguelgrinberg/microblog-api) using
the [APIFairy](https://github.com/miguelgrinberg/apifairy) Flask extension.

## Introduction
"""

import json
from flask import Blueprint, abort, request, send_from_directory, url_for
from apifairy import authenticate, body, response, other_responses

from app import db, app
from app.auth import token_auth
from app.authentication.models import File
from app.authentication.schemas import FileSchema
from werkzeug.utils import secure_filename
import imghdr
import os
import uuid

files = Blueprint("files", __name__)
fileSchema = FileSchema()
filesSchema = FileSchema(many=True)


@files.route("/files", methods=["POST"])
@response(fileSchema, 201)
@other_responses({400: "Fichier pas image"})
def addfile():
    """Ajouter une nouvelle region"""
    uploaded_file = request.files["file"]
    filename = secure_filename(uploaded_file.filename)
    if filename != "":
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config["UPLOAD_IMAGE_EXTENSIONS"]:
            target = os.path.join(app.config["UPLOAD_PATH"], "files")
        else:
            target = os.path.join(app.config["UPLOAD_PATH"], "images")

        if not os.path.isdir(target):
            os.mkdir(target)
        id = str(uuid.uuid4())
        uploaded_file.save(os.path.join(target, id + file_ext))

    file = File(_id=id, nom=filename, ext=file_ext)
    file.save()
    return {**json.loads(file.to_json()), "url": url_for("files.get_file", uuid=file._id, _external=True)}


@files.route("/files/<string:uuid>", methods=["GET"])
# @response(imageSchema)
@other_responses({404: "Images non trouvée"})
def get_file(uuid):
    """Recuperer une image à partir uuid"""
    file=File.objects(_id=uuid).first()
    if file:
        if file.ext not in app.config["UPLOAD_IMAGE_EXTENSIONS"]:
            target = os.path.join(app.config["UPLOAD_PATH"], "files")
        else:
            target = os.path.join(app.config["UPLOAD_PATH"], "images")

        filename = file._id + file.ext
        return send_from_directory(target, filename)
    else:
        abort(404)
    

@files.route("/files/<string:uuid>", methods=["DELETE"])
# @authenticate(token_auth)
@other_responses({404: "Image non trouvée"})
def delete_file(uuid):
    """Supression d'une region"""
    file=File.objects(d=uuid).first()
    if file:
        if file.ext not in app.config["UPLOAD_IMAGE_EXTENSIONS"]:
            target = os.path.join(app.config["UPLOAD_PATH"], "files")
        else:
            target = os.path.join(app.config["UPLOAD_PATH"], "images")

        filename = file.uuid + file.ext
        os.remove(os.path.join((target, filename)))
        file.delete()
        return "", 204



@files.route("/files", methods=["GET"])
@authenticate(token_auth)
@response(filesSchema, 200)
# @paginated_response(imagesSchema, order_by=Image.nom)
def get_all_files():
    """Liste des roles"""
    data=File.objects()
    return {**json.loads(data.to_json())}
