import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Welcome to my Climate Module 10 challenge page!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start]<br/>"
        f"/api/v1.0/[start]/[end]<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Convert the query results to a dictionary by using 'date' as the key and 'prcp' as the value.
    Return the JSON representation of your dictionary."""
    results = session.query(Measurement.date,Measurement.prcp).\
        filter(Measurement.date > '2016-08-23').all()
    
    # Close Session
    session.close()
    
    # Convert list of tuples into normal list
    all_dates_prcp = list(np.ravel(results))

    return jsonify(all_dates_prcp)

@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)
    """Return a JSON list of stations from the dataset"""
    results = session.query(Measurement.station).distinct().all()
    session.close()
    
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)
 
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurement.date,Measurement.tobs).\
        filter(Measurement.date > '2016-08-23').\
        filter(Measurement.station == "USC00519281").all()
    session.close()
    
    tobs_data = list(np.ravel(results))
    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def Temp(start=None,end=None):
    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range."""
    session = Session(engine)
    
    # select relevant output:
    sel = [func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)]
    
    if end == None:   #if end date is not specified
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
    else:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
    
    temp_data = list(np.ravel(results))
    return jsonify(temp_data)
 
if __name__ == "__main__":
    app.run(debug=True)
