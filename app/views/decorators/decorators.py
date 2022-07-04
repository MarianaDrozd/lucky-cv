import functools

from flask import g, redirect, url_for, session


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get("user") is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


def admin_required(func):
    def wrapper(*args, **kwargs):
        if not session.get("user").get("is_admin"):
            return {"message": "Forbidden"}, 403

        result = func(*args, **kwargs)
        return result

    wrapper.__name__ = func.__name__
    return wrapper

