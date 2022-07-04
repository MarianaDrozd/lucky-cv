from flask import request, Blueprint, render_template, session, redirect, url_for

import config

from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_mail import Mail, Message

from app.models import UserModel
from app.views.decorators.decorators import login_required

mail = Mail()

auth_bp = Blueprint('auth', __name__)

s = URLSafeTimedSerializer(config.Config.SECRET_KEY)


@auth_bp.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    """
    Method for user register
    :return: register form
    """
    if request.method == "POST":
        user = UserModel(
            username=request.form.get('username'),
            email=request.form.get('email'),
            _password=UserModel.generate_hash('password'),
        )
        user.is_admin = True if user.email == config.Config.MAIL_ADMIN else False
        user.save_to_db()
        msg = Message(subject='Registration',
                      sender=config.Config.MAIL_DEFAULT_SENDER,
                      recipients=[user.email])

        token = s.dumps(request.form.get("email"), salt='email-confirm')
        link = url_for('auth.confirm_email', token=token, _external=True)
        msg.html = render_template("activation.html", link=link, user=user)
        mail.send(msg)
        session['user'] = user.serialize
        return redirect("/")
    else:
        if session.get('user', False):
            return redirect('/')
        return render_template("signup.html")


@auth_bp.route('/confirm-email/<token>', methods=["GET"])
@login_required
def confirm_email(token):
    """
    Method for confirming email
    :param token: generates
    :return: confirming activation
    """
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        return render_template("emails/notactivated.html")

    user = UserModel.find_by_email(email=email)
    user.activated = True
    user.save_to_db()
    session["user"] = user.serialize
    return render_template("emails/activated.html")


@auth_bp.route('/sign-in', methods=['GET', 'POST'])
def login():
    """
    Method for user login
    :return: saving user data
    """
    if request.method == "POST":
        user = UserModel.find_by_username(request.form.get('username'))
        password = UserModel.generate_hash(request.form.get("password"))
        if user:
            if not UserModel.verify_hash(password, user.password):
                session['user'] = user.serialize
            else:
                return render_template('signin.html', wrong_data=True, username=request.form.get('username'))
        else:
            return render_template('errors/error_404.html')
        return redirect("/")
    if session.get('user', False):
        return redirect('/')
    return render_template('signin.html')


@auth_bp.route('/change-password', methods=["GET", "POST"])
def update_password():
    """
    Method for changing password
    :return: saving new password
    """
    if request.method == "POST":
        user = UserModel.find_by_username(session.get("user")["username"])
        if user.activated:
            user.password = user.generate_hash(request.form.get("new_password"))
            user.save_to_db()
            return redirect("/")
        else:
            return render_template("errors/need_activation.html")
    return render_template('password_change.html')


@auth_bp.route('/logout', methods=['GET'])
def logout():
    """
    Method for user logout
    """
    session.pop('user')
    return redirect('/')
