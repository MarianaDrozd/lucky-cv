from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import config
# from app.main import config


db_string = config.Config.SQLALCHEMY_DATABASE_URI

db = create_engine(db_string)
base = declarative_base()

Session = sessionmaker(db)
session = Session()
