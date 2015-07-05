# db_add.py
# Adds information to database
# (c) 2015 Roy Portas

from .db_setup import setup_session
from .db_schema import Broadband, Hospitals, BusStop, Sub, Tax, Crime
from .db_query import get_all_postcodes_for_hospitals
from .geocode import geocode_to_postcode
from .postcode_lookup import get_suburb
from csv import reader


def read_csv_file(file_location):
    """Reads a csv file
    returns a list of lists of csv cols and rows"""
    header_num = 0
    data = []
    csv_reader = reader(open(file_location))
    for row in csv_reader:
        if header_num == 0:
            # Skip the header row
            header_num = 1
        else:
            data.append(row)

    return data

def add_crime_data(file_location):
    """Add's QLD Police Crime Data"""
    data = read_csv_file(file_location)
    session = setup_session()
    list_size = len(data)

    suburb_crime = {}
    total_crime = 0
    crime_avg = 0

    list_counter = 0

    for entry in data:
        if not (entry[1].endswith("15") or entry[1].endswith("14") or entry[1].endswith("13")):
            continue
        crime_sum = 0
        for i in range(2,89):
            crime_sum += float(entry[i])
        total_crime += crime_sum
        suburb = entry[0]
        if suburb not in suburb_crime.keys():
            suburb_crime[suburb] = crime_sum
        else:
            suburb_crime[suburb] += crime_sum

    crime_avg = total_crime/len(suburb_crime.keys())
    list_size = len(suburb_crime.keys())

    for key in suburb_crime.keys():
        list_counter += 1

        crime = Crime(
            suburb = key,
            total = suburb_crime[key]
        )

        try:
            session.add(crime)
            print("Adding ({}/{})".format(list_counter, list_size))
            session.commit()
        except Exception as e:
            session.rollback()
            print("Could not add entry")


def add_tax_data(file_location):
    """Adds tax data"""
    data = read_csv_file(file_location)
    session = setup_session()
    list_size = len(data)
    list_counter = 0
    for entry in data:
        if (entry[0] == "QLD"):
            list_counter += 1
            tax = Tax(
                postcode = entry[1],
                gross_num = int(entry[5].replace(',', "")),
                gross_tax = int(entry[6].replace(',', "")),
                medicare_levy = int(entry[8].replace(',', "")),
                help_debt = int(entry[14].replace(',', ""))
            )
            print(tax)
            try:
                session.add(tax)
                print("Adding ({}/{}): {}".format(list_counter, list_size, tax))
                session.commit()
            except Exception as e:
                session.rollback()
                print("Could not add entry")

def add_bus_stops_data(file_location):
    """Adds bus stop data"""
    data = read_csv_file(file_location)
    session = setup_session()
    list_size = len(data) / 2
    list_counter = 0

    skip_line = 1
    for entry in data:
        if skip_line:
            skip_line = 0
        else:
            list_counter += 1
            skip_line = 1
            suburb = entry[3]
            street_name = entry[2]
            lat = entry[7]
            long = entry[8]

            stop = BusStop(
                suburb=suburb,
                street_name=street_name,
                lat=lat,
                lng=long
            )

            try:
                session.add(stop)
                print("Adding ({}/{}): {}".format(list_counter, list_size, street_name))
                session.commit()
            except Exception as e:
                session.rollback()
                print("Could not add entry: " + str(e))


def add_hospital_data(file_location):
    """Adds hospital data"""
    data = read_csv_file(file_location)
    session = setup_session()
    list_size = len(data)
    list_counter = 0

    for entry in data:
        list_counter += 1

        state = entry[0]
        name = entry[1]
        addr1 = entry[6]
        addr2 = entry[7]
        num_beds = entry[10]
        has_emergency = False
        if entry[14] == "Yes":
            has_emergency = True
        has_surgery = False
        if entry[15] == "Yes":
            has_surgery = True

        if state == "QLD":
            # Only geocode if the hospital is in queensland
            data = geocode_to_postcode(addr1 + " " + addr2)
            if data is not None:
                hospital = Hospitals(
                    postcode=data["postcode"],
                    name=name,
                    addr1=addr1,
                    addr2=addr2,
                    num_beds=num_beds,
                    has_emergency=has_emergency,
                    has_surgery=has_surgery,
                    lat=data["latitude"],
                    lng=data["longitude"]
                )

                try:
                    session.add(hospital)
                    print("Adding ({}/{}): {}".format(list_counter, list_size, name))
                    session.commit()
                except Exception as e:
                    session.rollback()
                    print("Could not add entry")

def add_postcode_data():
    session = setup_session()
    postcodes = get_all_postcodes_for_hospitals()
    for postcode in postcodes:
        suburb = get_suburb(postcode)
        if suburb != None:
            sub = Sub(suburb=suburb, postcode=postcode)
            try:
                session.add(sub)
                print("Adding {}".format(suburb))
                session.commit()
            except Exception as e:
                session.rollback()
                print("Could not add entry")


def add_broadband_data(file_location):
    """Adds the broadband data"""
    data = read_csv_file(file_location)

    session = setup_session()

    list_size = len(data)
    list_counter = 0

    for entry in data:
        list_counter += 1

        da = entry[0]
        suburb = entry[1]
        state = entry[2]
        count = entry[3]
        avail = entry[4]
        fibre_avail = entry[7]
        fibre_rating = entry[13]
        adsl_rating = entry[9]
        adsl_quality = entry[15]
        adsl_speed = entry[16]
        mobile_avail = entry[17]
        mobile_rating = entry[18]

        broadband = Broadband(
            da=da,
            suburb=suburb,
            count=count,
            avail=avail,
            adsl_avail=adsl_quality,
            adsl_rating=adsl_rating,
            adsl_speed=adsl_speed,
            fibre_avail=fibre_avail,
            fibre_rating=fibre_rating,
            mobile_avail=mobile_avail,
            mobile_rating=mobile_rating
        )

        try:
            if (state == "QLD"):
                print("Adding: {}% complete".format(float(list_counter)/float(list_size)*100))
                session.add(broadband)
                session.commit()
        except Exception as e:
            session.rollback()
            print("Could not add entry: " + str(e))

if __name__ == "__main__":
    #add_broadband_data("data/broadband.csv")
    #add_hospital_data("data/public_hospitals.csv")
    #add_bus_stops_data("data/dataset_bus_stops.csv")
    #add_postcode_data()
    add_tax_data("data/tax.csv")
    pass
