# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model

base = automap_base()

# reflect the tables

base.prepare(autoload_with=engine)

# Save references to each table

station = base.classes.station
measurement = base.classes.measurement

# Create our session (link) from Python to the DB

session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

# 1./

# Start at the homepage.

# List all the available routes.
@app.route("/")
def welcome():
    """List all available api routes"""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"\
        )

        # f"/api/v1.0/start_date<br/>"
        # f"/api/v1.0/start_end<br/>"
    

#2. /api/v1.0/precipitation

# Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.

# Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():

    session=Session(engine)
    # Calculate the date 1 year ago from the last data point in the database
    one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    prev_last_date = dt.date(one_year.year, one_year.month, one_year.day)

    # Query for the date and precipitation for the last year
    results = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= prev_last_date).order_by(measurement.date).all()

    # Create a dictionary from the row data and append to a list of all_precipitation
    precipitation_data = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict[date] = prcp
        precipitation_data.append(precipitation_dict)

    return jsonify(precipitation_data)

# 3. # /api/v1.0/stations
# Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stations():
    #create session link
    session = Session(engine)
    #query the names of all stations in the list
    results = session.query(measurement.station).distinct().all()
    session.close()

    #create a dictionary of the active stations and their counts
    station_data = []
    for station in results:
        station_dict = {}
        station_dict["station name"] = station[0]
        station_data.append(station_dict)

    return jsonify(station_data)

# 4./api/v1.0/tobs

# Query the dates and temperature observations of the most-active station for the previous year of data.

# Return a JSON list of temperature observations for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    #create session link
    session = Session(engine)
    #query the last 12 months of temperature data from the most active observation station 
    one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    prev_last_date = dt.date(one_year.year, one_year.month, one_year.day)

    results = session.query(measurement.date, measurement.tobs).\
    filter((measurement.station=='USC00519281')&(measurement.date >= prev_last_date)).all()

    #create a dictionary of t_obs data for the most active station
    tobs_data = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Oberved Temperature"] = tobs
        tobs_data.append(tobs_dict)

    return jsonify(tobs_data)


if __name__ == '__main__':
    app.run(debug=True)