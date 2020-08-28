import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    #Query results
    results = session.query(Measurement.date, Measurement.prcp).all()

    #Create dictionary
    precip = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict['date'] = date
        precip_dict['precipitation'] = prcp
        precip.append(precip_dict)

    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():

    """Return a list of all station names"""
    # Query all stations
    results = session.query(Station.name).all()

    # Convert list of tuples into normal list
    station_names = list(np.ravel(results))

    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def tobs():

    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    query_date
    
    output = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= query_date).all()
    
    temp_results = list(np.ravel(output))
    return jsonify(temp_results)
# If statements need three parts: for, if, and return. 
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def pick_dates(start=None, end= None):

    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        date = session.query(*sel).filter(Measurement.date >= start).all()
        startresults= list(np.ravel(date ))
        return jsonify(startresults)

    date = session.query(*sel).\
         filter(Measurement.date >= start).\
         filter(Measurement.date <= end).all()

    startresults= list(np.ravel(date ))
    return jsonify(startresults)

session.close()

if __name__ == '__main__':
    app.run(debug=True)