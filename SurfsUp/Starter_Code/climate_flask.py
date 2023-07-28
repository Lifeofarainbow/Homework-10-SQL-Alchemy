import numpy as np
import datetime as dt
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

Base.classes.keys()

Base.prepare(autoload_with=engine)

Station = Base.classes.station
Measurements = Base.classes.measurements

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def Homepage():
    return (
        f"Welcome to the Homepage of the Hawaii Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def rain():
    """Return a list of precipitation of previous year"""

    results_date = session.query(Measurements.date).order_by(Measurements.date.desc()).first()
    results_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    result = session.query(Measurements.date, Measurements.prcp).\
        filter(Measurements.date > results_year).\
        order_by(Measurements.date).all()

    results = []
    for result in result:
        row = {}
        row["date"] = result[0]
        row["prcp"] = result[1]
        results.append(row)

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
