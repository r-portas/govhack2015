# db_query.py
# Queries the database
# (c) 2015 Roy Portas

from .db_setup import setup_session, setup_engine
from .db_schema import Broadband, Hospitals, BusStop, Sub, Tax, Crime
from .geocode import lookup_suburb
from sqlalchemy.sql import text
from sqlalchemy.exc import OperationalError
from .db_exceptions import *
from .postcode_lookup import get_postcode

def get_crime(suburb):
    """Gets crime for a suburb"""
    session = setup_session()
    sub = suburb.upper()
    results = session.query(Crime).filter(Crime.suburb == sub).first()
    return results.total

def get_closest_hospital(lat, long):
    """Gets the closest hospital to a give latitude longitude"""
    engine = setup_engine()
    query = "SELECT name, addr1, addr2, lat, lng, num_beds, has_emergency, " \
        "has_surgery, 111.045 * DEGREES(ACOS(COS(RADIANS({lat})) * COS(RADIANS(lat))" \
        " * COS(RADIANS(lng) - RADIANS({lng})) + SIN(RADIANS({lat})) * SIN(RADIANS(lat))))"\
        " AS distance_in_km FROM hospitals ORDER BY distance_in_km ASC LIMIT 0,5;".format(lat=lat, lng=long)
    #query = "select * from hospitals"
    results = engine.execute(query).fetchall()
    return results

def get_tax_data(postcode):
    """Gets tax data from a suburb"""
    session = setup_session()

    results = []

    try:
        if postcode is not None:
            tax_data = session.query(Tax).filter(Tax.postcode == postcode).first()
            results = [
                tax_data.gross_tax/tax_data.gross_num,
                tax_data.medicare_levy/tax_data.gross_num,
                tax_data.help_debt/tax_data.gross_num,
            ]

    except:
        pass
    return results

def search_for_suburb(suburb):
    session = setup_session()
    sub = suburb.upper()

    location = lookup_suburb(sub)
    if location == None:
        raise NoInternetAccess("Internet access could not established")

    results = {}
    results["lat"] = location["latitude"]
    results["lng"] = location["longitude"]

    try:
        hospitals = get_closest_hospital(location["latitude"], location["longitude"])
        results["hospitals"] = hospitals

        broadband = session.query(Broadband).filter(Broadband.suburb == sub).first()
        results["broadband"] = broadband

        bus_stops = session.query(BusStop).filter(BusStop.suburb == sub).all()
        results["bus_stops"] = bus_stops

        # Handle tax stuff
        results["tax"] = None
        results["postcode"] = None
        postcode = get_postcode(suburb)
        if postcode is not None:
            tax_data = session.query(Tax).filter(Tax.postcode == postcode).first()
            tdata = [("Total number of tax payers", tax_data.gross_num), ("Average per tax payer", "${:,}".format(int(tax_data.gross_tax/tax_data.gross_num))), ("Total tax", "${:,}".format(tax_data.gross_tax)),
            ("Total medicare levy", "${:,}".format(tax_data.medicare_levy)), ("Help debt repayments", "${:,}".format(tax_data.help_debt))]
            results["tax"] = tdata
            results["postcode"] = postcode

    except OperationalError:
        raise NoDatabaseAccess("Could not connect to database")

    return results

def get_all_postcodes_for_hospitals():
    """Get all postcodes for hospitals"""
    session = setup_session()
    postcodes = session.query(Hospitals.postcode).all()
    results = []
    for postcode in postcodes:
        if postcode[0] != None:
            results.append(postcode[0])
    return results

if __name__ == "__main__":
    print(search_for_suburb("coorparoo"))
