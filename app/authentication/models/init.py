
import random
import click
from flask import Blueprint
from app import db, app
from sqlalchemy.exc import IntegrityError
from .user_model import User, Role
from werkzeug.security import generate_password_hash
# admins = Blueprint('admin', __name__)

# @admins.cli.command("admin_init")
def admins():  # pragma: no cover
    """Create the administrator."""
    role_admin=Role.objects(code="RO-001").first()
    if not role_admin:
        role_admin=Role(code="RO-001", libelle="Administrateur", privileges=["all"])
        role_admin.save()
        admin=User.objects(mail=app.config['ADMIN_MAIL_UA']).first()
        if not admin: 
            admin=User(mail=app.config["ADMIN_MAIL_UA"],is_validate=True, role=role_admin, nom="Admin", motpasse_hash=generate_password_hash(app.config["ADMIN_PASSWORD_UA"]))
            admin.save()
        else:
            print( 'admin  exist.')

    else:
        print( 'admin role exist.')
        admin=User.objects(mail=app.config['ADMIN_MAIL_UA']).first()
        if not admin: 
            admin=User(motpasse_hash=generate_password_hash(app.config["ADMIN_PASSWORD_UA"]), mail=app.config["ADMIN_MAIL_UA"],is_validate=True, role=role_admin, nom="Admin")
            admin.save()
        else:
            print( 'admin  exist.')
    role_guest=Role.objects(code="RO-002").first()
    if not role_guest:
        role_guest=Role(code="RO-002", libelle="Invite", privileges=[])
        role_guest.save()
    else:
        print( 'guest role exist.')


