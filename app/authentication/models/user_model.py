from bson import ObjectId
from flask import current_app
import uuid
import secrets
import mongoengine as me
from datetime import datetime, timedelta
from time import time
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from app import app
def gen_uuid():
    return uuid.uuid4().hex

class Updateable:
    def set_data(self, data):
        for attr, value in data.items():
            setattr(self, attr, value)


class Role(me.DynamicDocument, Updateable):

    @property
    def id(self):
        return self._id
    @property
    def modifier_par(self):
        return self.created_at
class User(me.DynamicDocument, Updateable):
    nom=me.StringField(required=True)
    prenom=me.StringField()
    mail = me.StringField(required=True)
    motpasse_hash = me.StringField(required=True)
    status=me.BooleanField(default=False)
    is_validate=me.BooleanField(default=False)
    status=me.BooleanField(default=True)
    privileges = me.ListField()
    role = me.ReferenceField(Role)
    photo_full=me.DictField()
    @property
    def id(self):
        return self._id
    
    @property
    def motpasse(self):
        raise AttributeError("mot de passe pas en lecture")

    @motpasse.setter
    def motpasse(self, motpasse):
        self.motpasse_hash = generate_password_hash(motpasse)

    def verifier_motpasse(self, motpasse):
        return check_password_hash(self.motpasse_hash, motpasse)

    def ping(self):
        self.last_seen = datetime.utcnow()

    def generate_auth_token(self):
        token = Session()
        token.init(user=self)
        return token
    @staticmethod
    def verify_access_token(access_token):
        
        token = Session.objects(access_token=access_token).first()
        if token:
            if token.access_expiration > datetime.now():
                utilisateur=User.objects(_id=ObjectId(token.user.id)).first()
                token.ping()
                token.save()
                return utilisateur
    def generate_reset_token(self,id=None):
        return jwt.encode(
            {
                "exp": time() + app.config["RESET_TOKEN_MINUTES"]*60,
                "reset_email": self.mail,
                "id":id
            },
            current_app.config["SECRET"],
            algorithm="HS256",
        )

    @staticmethod
    def verify_reset_token(reset_token):
        try:
            data = jwt.decode(
                reset_token, app.config["SECRET"], algorithms=["HS256"]
            )
        except:
            return None
        user=User.objects(mail=data["reset_email"])
        user.update(**{"naibi_id":data["id"], "is_validate_naibi_id": True})
        return  user
class Session(Updateable, me.Document):
    user=me.ReferenceField(User)
    access_token=me.StringField(required=True)
    access_expiration= me.DateTimeField(default=datetime.now())
    last_seen = me.DateTimeField()
    def init(self,user, access_token=None):
        # self.access_token = secrets.token_urlsafe()
        self.access_token = access_token if access_token else secrets.token_urlsafe()
        self.user = user
        self.access_expiration = datetime.now() + timedelta(
            minutes=current_app.config["ACCESS_TOKEN_MINUTES"]
        )

    def expire(self):
        self.access_expiration = datetime.now()
        

    def ping(self):
        self.last_seen = datetime.now()
        self.access_expiration =datetime.now() + timedelta(
            minutes=current_app.config["ACCESS_TOKEN_MINUTES"]
        )

    @staticmethod
    def clean():
        """Remove any tokens that have been expired for more than a day."""
        yesterday =datetime.now() - timedelta(days=1)
        # db.session.execute(Token.delete().where(Token.refresh_expiration < yesterday))