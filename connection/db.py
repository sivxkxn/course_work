from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from connection.config import Config

Base = declarative_base()
engine = create_engine(f'postgresql://{Config.user}:{Config.password}@{Config.host}/{Config.dbname}')
session = sessionmaker(bind=engine)()

def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
