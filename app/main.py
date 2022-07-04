from flask import Flask
from flask_mail import Mail
# from config import Config as config
from app.database.database import db, base


def setup_database(app):
    with app.app_context():
        @app.before_first_request
        def create_tables():
            base.metadata.create_all(db)


app = Flask(__name__)
app.config.from_object("config.Config")
app.secret_key = "btIeBI8NJgtnPpaocmKyyimUbmsqlSWn"
mail = Mail(app)
# database first, then blueprints!
setup_database(app)

from .api import api_auth_bp, api_resumes_bp, api_templates_bp
from .views import auth_bp, resumes_bp, resume_templates_bp

app.register_blueprint(api_auth_bp)
app.register_blueprint(api_resumes_bp)
app.register_blueprint(api_templates_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(resumes_bp)
app.register_blueprint(resume_templates_bp)
