from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from app.main import mail
from flask import request, url_for, session, Blueprint
from config import Config
from app.models import UserModel
from flask_mail import Message

s = URLSafeTimedSerializer(Config.SECRET_KEY)

api_auth_bp = Blueprint('api_auth', __name__)


@api_auth_bp.route("/APIv1/auth/user-register", methods=["POST"])
def user_register():
    """
    Method for user registration and sending activation email.
    :return: user, token
    """
    user = UserModel(
        username=request.json.get('username'),
        email=request.json.get('email'),
        _password=UserModel.generate_hash(request.json.get('password')),
    )
    user.is_admin = True if user.email == Config.MAIL_ADMIN else False
    msg = Message(subject='Registration',
                  sender=Config.MAIL_DEFAULT_SENDER,
                  recipients=[user.email])
    token = s.dumps(request.json.get("email"), salt='email-confirm')
    link = url_for('auth.confirm_email', token=token, _external=True)
    msg.html = link
    mail.send(msg)
    session['user'] = user.serialize
    user.save_to_db()
    return f'User {user} was created'


@api_auth_bp.route("/APIv1/auth/confirm-email/<token>", methods=["GET"])
def confirm_email(token):
    """
    Method for confirming email and setting "activated" to True
    :param token: randomly generated
    :return: user
    """
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        return {"message": "token expired"}

    user = UserModel.find_by_email(email=email)
    user.activated = True
    user.save_to_db()
    session["user"] = user.serialize
    return user.serialize


@api_auth_bp.route("/APIv1/auth/login", methods=["POST"])
def login():
    """
    Method for user login.
    :return: user
    """
    user = UserModel.find_by_username(request.json.get('username'))
    password = UserModel.generate_hash(request.json.get("password"))
    if user:
        if not UserModel.verify_hash(password, user.password):
            session['user'] = user.serialize
            return user.serialize
        else:
            return {"message": "Login failed"}
    else:
        return {"message": "Not Found"}


@api_auth_bp.route('/APIv1/auth/logout', methods=['GET'])
def logout():
    """
    Method for user logout.
    """
    if session.get("user"):
        session.pop('user')
        return {"message": "logout"}, 440
    return {"message": "User not authorized"}, 401

