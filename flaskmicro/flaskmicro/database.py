# from flask import request, current_app

# from jivacore.db.constants import MIRROR_DA
# from jivacore.db.db import attach_utc_and_timezone


# def get_secondary_session():
#     """
#     """
#     mirror_session = get_db_session(db_name=MIRROR_DA)
#     return mirror_session


# def get_primary_session():
#     """
#     """
#     session = current_app.scoped_session()
#     db_session = attach_utc_and_timezone(session, request, request.context["username"])
#     return db_session


# def jiva_context(**kwargs):
#     """
#     """
#     cxt = dict(db_session=request.db_session,
#                mirror_session=get_secondary_session(),
#                utc_timedelta=db_session.utc_timedelta,
#                timezone_name=db_session.timezone_name,
#                loggedin_user_id=request.context['user_idn'],
#                loggedin_user=request.context['identity']
#                )
#     cxt.update(kwargs)
#     return cxt




# Below code will be removed

from os import getenv
from sys import platform
import json

import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import OperationalError


from flaskmicro.common.exceptions import DBConnectionError
from sqlalchemy.ext.declarative import declarative_base
# from flaskbase.flask_model.flask_model import Author



# db_host = getenv('DB_HOST')
# db_name = getenv('DB_NAME')
# db_user = getenv('DB_USERNAME')
# db_password = getenv('DB_PASSWORD')
# db_port = getenv('DB_PORT')
# driver = 'ODBC Driver 17 for SQL Server'
# if platform == 'win32':
#     driver = 'SQL Server'

DB_HOST='localhost'
DB_NAME='local_db'
DB_USERNAME='root'
DB_PASSWORD='root'
DB_PORT=3306

db_user = DB_USERNAME
db_password = DB_PASSWORD
db_host = DB_HOST
db_port = DB_PORT
db_name = DB_NAME

# SQLALCHEMY_DATABASE_URI = f'mssql+pyodbc://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?driver={driver}'
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
engine = db.create_engine(SQLALCHEMY_DATABASE_URI)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
