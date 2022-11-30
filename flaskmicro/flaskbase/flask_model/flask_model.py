import sqlalchemy as sa
import json
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from flaskmicro.database import db_session

Base = declarative_base()
Base.query = db_session.query_property()

class Author(Base):
    __tablename__ = 'authors'
    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.String)
    last_name = sa.Column(sa.String)
    email = sa.Column(sa.String)
    birthdate = sa.Column(sa.String)
    added = sa.Column(sa.String)

    def __init__(self, first_name=None, last_name=None, email=None, birthdate=None, added=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.birthdate = birthdate
        self.added = added


    def __repr__(self):
        return f'{self.first_name}, {self.last_name} ({self.email}, {self.birthdate}, {self.added})'

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
