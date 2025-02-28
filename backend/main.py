import os
from flask import Flask
from flask_restful import Api
from flask_security import Security, SQLAlchemySessionUserDatastore
from application.config import LocalDevelopmentConfig
from application.data.model import User, Role,db
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from werkzeug.security import generate_password_hash
from application.jobs import workers
from application.jobs import tasks

app = None
api = None
celery = None
cache = None

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()
    api = Api(app)
    app.app_context().push()

    jwt = JWTManager(app)
    datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    app.security = Security(app, datastore)
    app.app_context().push()
    
    celery=workers.celery
    celery.conf.update(
        broker_url = app.config["CELERY_BROKER_URL"],
        result_backend = app.config["CELERY_RESULT_BACKEND"],
        timezone="Asia/Kolkata",
        broker_connection_retry_on_startup=True
    )

    celery.Task=workers.ContextTask
    app.app_context().push()
    cache=Cache(app)
    app.app_context().push()

    return app, api, celery, cache


app, api,celery,cache= create_app()


def create_roles():
    with app.app_context():
        db.create_all()

        # Create admin role if it doesn't exist
        if Role.query.filter_by(name='admin').first() is None:
            role_admin = Role(name='admin', description='administer role')
            db.session.add(role_admin)

        # Create user role if it doesn't exist
        if Role.query.filter_by(name='user').first() is None:
            role_user = Role(name='user', description='user role')
            db.session.add(role_user)

        # Create service_professional role if it doesn't exist
        if Role.query.filter_by(name='service_professional').first() is None:
            role_sp = Role(name='service_professional', description='service professional role')
            db.session.add(role_sp)

        db.session.commit()

        # Create an admin user if it doesn't exist
        user = User.query.filter_by(username='admin').first()
        if user is None:
            datastore = app.security.datastore
            datastore.create_user(
                username='admin',
                password=generate_password_hash('1234'),
                email="admin@gmail.com"
            )
            db.session.commit()

            user = User.query.filter_by(username='admin').first()
            role = Role.query.filter_by(name='admin').first()
            datastore.add_role_to_user(user, role)
            db.session.commit()



from application.controllers.controllers import *

from application.controllers.api import *

#api.add_resource(SectionAPI, '/api/section', '/api/section/<int:id>')

#api.add_resource(BookAPI, '/api/sectbook/<id>', '/api/book/<int:s_id>')


if __name__ == "__main__":
    create_roles()
    app.run(debug=True)
