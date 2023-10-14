from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
import os

Base = declarative_base()
user = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
host = os.environ.get('DB_HOST')
port = os.environ.get('DB_PORT')
name = os.environ.get('DB_NAME')

class Database:
    def build(self, db_uri):
        self.engine = create_engine(db_uri)
        self.Session = sessionmaker(bind=self.engine)

    def create_all(self):
        is_test = os.environ.get('is_test')
        uri = self.get_uri(is_test)
        self.create_database(is_test, uri)
        self.build(uri)        
        Base.metadata.create_all(self.engine)

    def get_uri(self, is_test):
        uri = f'postgresql://{user}:{password}@{host}:{port}/{name}'        
        if is_test :
            uri = f'sqlite:///:memory:'
        return uri

    def create_database(self, is_test, uri):
        if not database_exists(uri) and not is_test:
            create_database(uri)

    def drop_all(self):
        Base.metadata.drop_all(self.engine)

    def get_session(self):
        return self.Session()

db = Database()
