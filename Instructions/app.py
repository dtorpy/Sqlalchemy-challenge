import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)



# 1. 

@app.route("/")
def welcome():
    """List all available api routes."""
    return(
        f"Available Routes:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"List of Stations: /api/v1.0/stations<br/>"
        f"Temperatures: /api/v1.0/temp<br/>"
        f"Start: /api/v1.0/start<br/>"
        f"Year: /api/v1.0/year<br/>"

    )

#2.
#@app.route('/api/v1.0/<start>')
#def get_t_start(start):
### 
"""
#session = Session(engine)
 #    queryresult = session.query(func.min(Measurement.temp), func.avg(Measurement.temp), func.max(Measurement.temp)).\
  #      filter(Measurement.date >= start).all()
   # session.close()

  #  tempall = []
   # for min,avg,max in queryresult:
    #    temp_dict = {}
    #    temp_dict["Min"] = min
    #    temp_dict["Average"] = avg
        temp_dict["Max"] = max
        tempall.append(temp_dict)

    return jsonify(tempall)
###
"""

@app.route('/api/v1.0/precipitation')
def precipitation():
    querydate = dt.date(2017,8,23)-dt.timedelta(days=365)
    sel = [Measurement.date,Measurement.prcp]
    queryresult = session.query(*sel).\
        filter(Measurement.date >= querydate).all()
    precip_dict = {date:prcp for date, prcp in queryresult}
    return jsonify(precip_dict)

@app.route('/api/v1.0/stations')
def stations():
    list_stations = session.query(Station.station).all()
    return jsonify(list_stations)

@app.route('/api/v1.0/temp')
def tobs():
    active = session.query(Measurement.tobs, Measurement.date).filter(Measurement.station=='USC00519281').\
        filter(Measurement.date>='2016-08-22').order_by(Measurement.date).all()
    active =[i[0] for i in active]
    temp = list(np.ravel(active))
    return jsonify(active)

@app.route('/api/v1.0/year')


if __name__ == "__main__":
    app.run(debug=True)
