# database/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Path: database.py
URL_DATABSE = 'mysql+pymysql://u426733178_rootfyp:Bike5672@193.203.166.177:3306/u426733178_fyp'

engine = create_engine(URL_DATABSE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
