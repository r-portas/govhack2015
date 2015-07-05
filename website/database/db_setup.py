# db_setup.py
# Database setup
# (c) 2015 Roy Portas

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
ip_address = ""
username = ""
password = ""

def setup_engine():
    """Sets up the engine
    Returns a engine object
    """
    print("Setting up engine")
    engine = create_engine('mysql+pymysql://{}:{}@{}/govhack2015'.format(
            username, password, ip_address))

    return engine

def setup_session():
    """Sets up the session for accessing the database
    Returns a session object
    """
    print("Setting up session")
    engine = setup_engine()
    Base.metadata.bin = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    return session
