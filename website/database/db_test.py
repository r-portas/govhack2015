# db_test.py
# Test the database
# (c) 2015 Roy Portas

from db_setup import setup_engine, setup_session
from db_schema import Base, Sub, Broadband

def add_test_entries():
    """Add some test entries"""
    session = setup_session()
    try:
        suburb = Sub(suburb="TEST", postcode=9999)
        session.add(suburb)
        session.commit()
    except:
        print("Could not add suburb")

    try:
        broadband = Broadband(da="TEST_DA", suburb="TEST",
                                count=100, fibre_rating="E")
        session.add(broadband)
        session.commit()
    except:
        print("Could not add broadband")

    print("Added test data to database")
    suburbs = session.query(Sub).all()
    for suburb in suburbs:
        print(suburb)

    broadbands = session.query(Broadband).all()
    for b in broadbands:
        print(b)
