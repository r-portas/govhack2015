# db_schema.py
# Contains all the schema for the database
# (c) 2015 Roy Portas

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from .db_setup import setup_engine, setup_session

Base = declarative_base()

class Sub(Base):
    """Stores the base data"""
    __tablename__ = "sub"

    suburb = Column(String(50), primary_key=True)
    postcode = Column(Integer)

    def __repr__(self):
        return "<Sub: ({}, {})>".format(self.suburb, self.postcode)

class Crime(Base):
    """Stores crime information"""
    __tablename__ = "crime"

    suburb = Column(String(50), primary_key=True)
    total = Column(Integer)

    def __repr__(self):
        return "<Crime: ({}, {})>".format(self.suburb, self.total)

class Tax(Base):
    """Stores tax data"""
    __tablename__ = "tax"
    postcode = Column(Integer, primary_key=True)
    gross_num = Column(Integer)
    gross_tax = Column(Integer)
    medicare_levy = Column(Integer)
    help_debt = Column(Integer)

    def __repr__(self):
        return "<Tax: ({}, {}, {}, {}, {})".format(
            self.postcode, self.gross_num, self.gross_tax, self.medicare_levy,
            self.help_debt
        )


class Broadband(Base):
    """Stores broadband data"""
    __tablename__ = "broadband"

    da = Column(String(50), primary_key=True)
    suburb = Column(String(50))
    count = Column(Integer)
    avail = Column(String(30))
    adsl_avail = Column(String(30))
    adsl_rating = Column(String(30))
    adsl_speed = Column(Float)
    fibre_avail = Column(String(30))
    fibre_rating = Column(String(30))
    mobile_avail = Column(String(30))
    mobile_rating = Column(String(30))

    def __repr__(self):
        return "<Broadband: ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})>".format(
            self.da, self.suburb, self.count, self.avail, self.adsl_avail, self.adsl_rating,
            self.adsl_speed, self.fibre_avail, self.fibre_rating, self.mobile_avail,
            self.mobile_rating
        )

class Hospitals(Base):
    """Stores all hospitals"""
    __tablename__ = "hospitals"

    postcode = Column(Integer)
    name = Column(String(50), primary_key=True)
    addr1 = Column(String(100))
    addr2 = Column(String(100))
    num_beds = Column(Integer)
    has_emergency = Column(Boolean)
    has_surgery = Column(Boolean) # Non emergency surgery
    lat = Column(Float)
    lng = Column(Float)

    def __repr__(self):
        return "<Hospital: ({}, {}, {}, {}, {}, {}, {}, {}, {})>".format(
            self.postcode, self.name, self.addr1, self.addr2, self.num_beds, self.has_emergency,
            self.has_surgery, self.lat, self.lng
        )

class BusStop(Base):
    """Stores all bus stops"""
    __tablename__ = "busstops"

    id = Column(Integer, primary_key=True)
    suburb = Column(String(50))
    street_name = Column(String(50))
    lat = Column(Float)
    lng = Column(Float)

    def __repr__(self):
        return "<BusStop: ({}, {}, {}, {}, {})".format(self.id, self.suburb,
            self.street_name, self.lat, self.lng)

def create_tables():
    """Creates the tables for the database
    WARNING: THIS WILL PROBABLY PURGE THE DATABASE"""
    engine = setup_engine()
    print("Creating tables...")
    Base.metadata.create_all(engine)

    print("Testing connection...")
    connection = engine.connect()
    print("Closing connection")
    connection.close()

def wipe_tables():
    """Deletes all data within tables"""
    session = setup_session()
    tables = [Broadband, Sub]

    for table in tables:
        try:
            num_deleted = session.query(table).delete()
            print("Deleted {} entries from {}".format(num_deleted,
                                            table.__tablename__))

            session.commit()
        except:
            session.rollback()


if __name__ == "__main__":
    create_tables()
