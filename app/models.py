from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy import Column, String, Integer, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship, backref
from app.helpers.serializers import Serializer
from app.database.database import base, session


class UserModel(base, Serializer):
    __tablename__ = 'users'
    id_ = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    _password = Column(String(256), nullable=False)
    # resume = relationship("ResumeModel", back_ref="user", lazy="dynamic")
    activated = Column(Boolean, nullable=False, default=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, nullable=False, default=True)

    def __repr__(self):
        return f'User {self.username}'

    @classmethod
    def find_by_username(cls, username):
        user = session.query(cls).filter_by(username=username, is_active=True).first()
        return user

    @classmethod
    def find_by_email(cls, email):
        user = session.query(cls).filter_by(email=email, is_active=True).first()
        return user

    def save_to_db(self):
        session.add(self)
        session.commit()

    @property
    def serialize(self):
        return {
            "id": self.id_,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "activated": self.activated,
            "is_admin": self.is_admin,
            "is_active": self.is_active
        }

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = self.generate_hash(password)

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, pass_hash):
        return sha256.verify(password, pass_hash)


class ResumeModel(base, Serializer):
    __tablename__ = 'resumes'
    id_ = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id_'))
    user = relationship("UserModel", backref=backref("resumes", uselist=False))
    # user = relationship("UserModel", back_populates="resume")
    # resume_templates = relationship("ResumeTemplateModel", lazy="dynamic",
    #                                 cascade="all, delete-orphan",
    #                                 foreign_keys="ResumeTemplateModel.resume_id")
    title = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    phone_number = Column(String(15), nullable=False)
    linkedin = Column(String(50), nullable=False)
    github = Column(String(50), nullable=False)
    location = Column(String(50), nullable=False)
    summary = Column(Text, nullable=False)
    education = Column(Text, nullable=False)
    job_experience = Column(Text, nullable=True)
    hard_skills = Column(String(200), nullable=False)
    soft_skills = Column(String(200), nullable=False)
    languages = Column(String(100), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    @classmethod
    def find_by_user_id(cls, user_id):
        resumes = session.query(cls).filter_by(user_id=user_id, is_active=True).order_by(cls.id_).all()
        return [resume.serialize for resume in resumes]

    @classmethod
    def find_by_id(cls, id_):
        resume = session.query(cls).filter_by(id_=id_, is_active=True).first()
        return resume

    def save_to_db(self):
        session.add(self)
        session.commit()

    def delete_from_db(self):
        session.delete(self)
        session.commit()

    @property
    def serialize(self):
        return {
            "id": self.id_,
            "title": self.title,
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "linkedin": self.linkedin,
            "github": self.github,
            "location": self.location,
            "summary": self.summary,
            "education": self.education,
            "job_experience": self.job_experience,
            "hard_skills": self.hard_skills,
            "soft_skills": self.soft_skills,
            "languages": self.languages,
            "is_active": self.is_active
        }


class ResumeTemplateModel(base, Serializer):
    __tablename__ = 'resume_templates'
    id_ = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), unique=True, nullable=False)
    resume_id = Column(Integer, ForeignKey('resumes.id_'))
    resume = relationship("ResumeModel", backref=backref("resume_templates", uselist=False))
    # resume = relationship("ResumeModel", back_populates="resume_templates")
    is_active = Column(Boolean, nullable=False, default=True)

    @classmethod
    def return_all(cls):
        templates = session.query(cls).all()
        return [template.serialize for template in templates]

    @classmethod
    def find_by_id(cls, id_):
        template = session.query(cls).filter_by(id_=id_).first()
        return template

    def save_to_db(self):
        session.add(self)
        session.commit()

    @property
    def serialize(self):
        return {
            "id": self.id_,
            "name": self.name,
            "resume_id": self.resume_id,
            "is_active": self.is_active
        }

