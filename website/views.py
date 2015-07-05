__author__ = 'Ryan Lonergan'

from flask import render_template, flash, redirect, request, jsonify
from website import app
from .database.db_query import search_for_suburb, get_tax_data, get_crime
from .database.db_exceptions import *

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           title="How's My Suburb?")

@app.route('/', methods=['POST'])
def search():
    suburb = request.form['text']
    if len(suburb) == 0:
        return redirect('/')
    return redirect('/details/{}'.format(suburb))

@app.route('/details/<suburb>')
def details(suburb):
    try:
        results = search_for_suburb(suburb)
    except NoInternetAccess:
        return "ERROR: No internet available"
    except NoDatabaseAccess:
        return "ERROR: Could not connect to database"

    broadband = results["broadband"]
    res = []

    crime = get_crime(suburb)

    postcode = results["postcode"]
    chart_tax = get_tax_data(postcode)

    if broadband is not None:
        res = [
            ("Availability", broadband.avail),
            ("ADSL Availability", broadband.adsl_avail),
            ("ADSL Rating", broadband.adsl_rating),
            ("Avg ADSL Speed", str(broadband.adsl_speed) + " Mbps"),
            ("Fibre Availability", broadband.fibre_avail),
            ("Fibre Rating", broadband.fibre_rating),
            ("Mobile Availability", broadband.mobile_avail),
            ("Mobile Rating", broadband.mobile_rating)
        ]

    hosp = results["hospitals"]

    tax_data = results["tax"]

    return render_template('details.html',
                           title="Results for " + suburb,
                           suburb=suburb,
                           results=res,
                           hospitals=hosp,
                           lat=results["lat"],
                           lng=results["lng"],
                           tax=tax_data,
                           chart_tax=chart_tax,
                           avg_crime=crime)

@app.route("/api/<suburb>")
def get_data(suburb):
    """Send data to the javascript portion of the app"""
    try:
        results = search_for_suburb(suburb)
    except NoInternetAccess:
        return "ERROR: No internet available"
    except NoDatabaseAccess:
        return "ERROR: Could not connect to database"
    res = {}
    res["bus_stops"] = []
    res["hospitals"] = []

    hosp = results["hospitals"]

    for h in hosp:
        res["hospitals"].append({"name": h[0], "lat": h[3], "lng": h[4]})

    stops = results["bus_stops"]
    for stop in stops:
        res["bus_stops"].append([stop.lat, stop.lng])


    return jsonify(res)
