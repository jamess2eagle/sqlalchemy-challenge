import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify



# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

session = Session(engine)

# Flask Setup
app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Welcome to climate API!<br/>"
        f"Precipitation data: /api/v1.0/precipitation<br/>"
        f"Stations data: /api/v1.0/stations<br/>"
        f"Temperature data: /api/v1.0/tobs<br/>"
        f"Temperature with given start date: /api/v1.0/startdate or given start and end date: /api/v1.0/startdate/enddate"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    #Convert the query results to a dictionary using date as the key and prcp as the value.
    #Return the JSON representation of your dictionary.
    data1 = session.query(measurement.date, measurement.prcp).filter(measurement.date > "2016-08-23").all()
    prcp = []
    for row in data1:
        prcpdict = {}
        prcpdict["date"] = row.date
        prcpdict["precipitation"] = row.prcp
        prcp.append(prcpdict)
    return jsonify(prcp)

@app.route("/api/v1.0/stations")
def stations():
#     #Return a JSON list of stations from the dataset.
    data2 = session.query(station.station, station.name).all()
    stationdata = []
    for row in data2:
        stationdict = {}
        stationdict["station"] = row.station
        stationdict["name"] = row.name
        stationdata.append(stationdict)
    return jsonify(stationdata)
@app.route("/api/v1.0/tobs")
def tobs():
#     #Query the dates and temperature observations of the most active station for the last year of data.
#     #Return a JSON list of temperature observations (TOBS) for the previous year.
    data3 = session.query(measurement.station).group_by(measurement.station).order_by(func.count(measurement.station).desc()).first()
    data4 = session.query(measurement.date, measurement.tobs).filter(measurement.date > "2016-08-23", measurement.station == data3.station).all()
    tobsdata = []
    for row in data4:
        tobsdict = {}
        tobsdict["date"] = row.date
        tobsdict["tobs"] = row.tobs
        tobsdata.append(tobsdict)
    return jsonify(tobsdata)

#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>")
def long_vacation(start):
    data5 = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).all()
    startdata = []
    for row in data5:
        startdict = {}
        startdict["min temp"] = row[0]
        startdict["avg temp"] = row[1]
        startdict["max temp"] = row[2]
        startdata.append(startdict)
    return jsonify(startdata)
@app.route("/api/v1.0/<start>/<end>")
def vacation(start, end):
    data6 = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start, measurement.date <= end).all()
    rangedata = []
    for row in data6:
        rangedict = {}
        rangedict["min temp"] = row[0]
        rangedict["avg temp"] = row[1]
        rangedict["max temp"] = row[2]
        rangedata.append(rangedict)
    return jsonify(rangedata)




if __name__ == '__main__':
    app.run(debug=True)
