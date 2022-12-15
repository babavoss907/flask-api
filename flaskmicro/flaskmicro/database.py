from os import getenv
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session

db_host = getenv('DB_HOST')
db_name = getenv('DB_NAME')
db_user = getenv('DB_USERNAME')
db_password = getenv('DB_PASSWORD')
db_port = getenv('DB_PORT')

SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

engine = db.create_engine(SQLALCHEMY_DATABASE_URI)

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
