import os

import pytest

# from app.models import UserModel
from app.models import UserModel, ResumeModel

TEST_USERNAME = "test"
TEST_PASSWORD = "testpassword"
TEST_EMAIL = "test@email.com"
ADMIN_TEST_USERNAME = "admintest"
ADMIN_TEST_PASSWORD = "admintestpassword"
ADMIN_TEST_EMAIL = "admintest@example.com"


@pytest.fixture
def app(monkeypatch):
    db_path = os.path.abspath("test.db")
    monkeypatch.setenv('SQLALCHEMY_DATABASE_URI', f"{db_path}")
    from app.main import app

    return app


@pytest.fixture
def client(app):
    """A test client for the app."""
    app.testing = True
    return app.test_client()


@pytest.fixture
def authentication_headers(client):
    def _authentication_headers(is_admin: bool):

        if is_admin:
            username = ADMIN_TEST_USERNAME
            password = ADMIN_TEST_PASSWORD
        else:
            username = TEST_USERNAME
            password = TEST_PASSWORD

        resp = client.post(
            '/APIv1/auth/login',
            json={
                "username": username,
                "password": password,
            }
        )

        if resp.json['message'] == f"User {username} doesn't exist":

            if is_admin:
                email = ADMIN_TEST_EMAIL
            else:
                email = TEST_EMAIL

            resp = client.post(
                '/APIv1/auth/user-register',
                json={
                    "email": email,
                    "username": username,
                    "password": password,
                    "is_admin": is_admin,
                }
            )

        auth_token = resp.json['token']
        headers = {"Authorization": f"Bearer {auth_token}"}

        return headers

    return _authentication_headers


@pytest.fixture(scope='module')
def my_user():
    user = UserModel()
    user.id = 1
    user.email = TEST_EMAIL
    user.hashed_password = user.generate_hash(TEST_PASSWORD)

    user.username = TEST_USERNAME
    return user


@pytest.fixture(scope='module')
def my_resume():
    resume = ResumeModel()
    resume.title = "Junior Python Developer"
    resume.user_id = 1
    resume.first_name = "Olena"
    resume.last_name = "Pchilka"
    resume.email = "pchilkaukr@test.net"
    resume.phone_number = "+38025896314"
    resume.linkedin = "linkedin.linkedin"
    resume.github = "github.github"
    resume.location = "Kyiv, Ukraine"
    resume.summary = "Some summary including 3-5 sentences"
    resume.education = "Education experience"
    resume.job_experience = "Job experience"
    resume.hard_skills = "Hard skills"
    resume.soft_skills = "Soft skills"
    resume.languages = "Ukrainian, English"
    return resume


# @pytest.fixture(scope='module')
# def my_revoked_token():
#     revoked_token = RevokedTokenModel()
#     revoked_token.id_ = 1
#     revoked_token.jti = "11111111111111111111"
#     revoked_token.blacklisted_on = "Mon Apr 11 2022 20:11"
#     return revoked_token
