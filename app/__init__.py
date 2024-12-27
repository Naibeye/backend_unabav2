import json
from flask import Flask, redirect, url_for
from flask_mail import Mail
from alchemical.flask import Alchemical
from flask_cors import CORS
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from apifairy import APIFairy
from flask_mongoengine import MongoEngine
from flask_socketio import SocketIO
app = Flask(__name__)
app.config.from_object("config.ProdConfig")
mail = Mail()
mail.init_app(app)
db = MongoEngine(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
migrate = Migrate(app, db)
ma=Marshmallow(app)
apyFairy=APIFairy(app)
socketio = SocketIO(app,debug=True,cors_allowed_origins='*')
apifairy = APIFairy()
with open("./privilege.json") as f:
    config = json.load(f)
app.config.update(config)
from .authentication.views.user_view import user

from .authentication import models
app.register_blueprint(user, url_prefix="/api")
from .authentication.views.crud_view import crud
app.register_blueprint(crud, url_prefix="/api")
from .backend import model
from .backend.crud_view import crud_app
app.register_blueprint(crud_app, url_prefix="/api")
from .authentication.views.file_view import files
app.register_blueprint(files, url_prefix="/api")
from .authentication.views.user_view_new import usernew
app.register_blueprint(usernew, url_prefix="/api")
from .authentication.models.init import admins
admins()
@app.shell_context_processor
def shell_context():  # pragma: no cover
    ctx = {"db": db}
    for attr in dir(models):
        model = getattr(models, attr)
        if hasattr(model, "__bases__") and db.Model in getattr(model, "__bases__"):
            ctx[attr] = model
    return ctx


@app.route("/")
def index():  # pragma: no cover
    return redirect(url_for("apifairy.docs"))

#
from . import models
