#!/usr/bin/python
# coding=utf-8

import sys
import os.path
import json
# from PyQt5.QtWidgets import QApplication
# Initialize a QApplication object
# app = QApplication(sys.argv)


# Add the root directory to the Python path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) + '/src/'
sys.path.append(root_dir)

import numpy as np
import sys
from maya_widget import MayaviQWidget  # Adjusted import statement
import utils  # Adjusted import statement
import uuid

# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address

from flask import Flask, request, jsonify, send_file
app = Flask(__name__)

# Configure Flask-Limiter
# limiter = Limiter(
#     get_remote_address,
#     app=app,
#     default_limits=["3 per day"]
# )

viewer3D_MALE = MayaviQWidget("male")
viewer3D_FEMALE = MayaviQWidget("female")

def predict(gender, dataList):
    print({ "gender": gender, "weight": dataList[0], "height": dataList[1] })
    w = float(dataList[0])
    h = float(dataList[1])
    data = []
    data.append(w ** (1.0 / 3.0) * 1000)
    data.append(h * 10)
    for i in range(2, 19):
        try:
            tmp = 0
            if len(dataList)-1 > i:
                tmp = float(dataList[i])    
            data.append(tmp * 10)
        except ValueError:
            data.append(0)
    data = np.array(data).reshape(utils.M_NUM, 1)

    viewer3D = viewer3D_MALE if gender == 1 else viewer3D_FEMALE

    [t_data, value] = viewer3D.predict(data)
    hash = uuid.uuid4().hex
    output = viewer3D.save(hash)
    resArr = []

    print("data ready...")
    
    if output is not None:
        for i in range(0, utils.M_NUM):
            # print("%s: %f" % (utils.M_STR[i], output[i, 0]))
            resArr.append({ "name" : utils.M_STR[i], "value": output[i, 0] / 10 })
    else:
        pass
    
    return jsonify({ "data" : resArr, "hash": hash })

@app.route('/scan')

#  data_list = ["weight", "height", "neck", "chest",
#   "belly button waist", "gluteal hip",
#   "neck shoulder elbow wrist", "crotch knee floor",
#   "across back shoulder neck", "neck to gluteal hip",
#   "natural waist", "max. hip", "natural waist rise",
#   "shoulder to midhand", "upper arm", "wrist",
#   "outer natural waist to floor", "knee", "max. thigh"]

def scan():
    try:
        gender = float(request.args.get('g'))
        data_list = json.loads(request.args.get('ls'))
    except (TypeError, ValueError, json.JSONDecodeError) as e:
        return jsonify({'error': str(e)}), 400
    
    prediction = predict(gender, data_list)
    return prediction

@app.route('/model')
def model():
    hash = request.args.get('hash')
    print({ "hash": hash })
    return send_file(os.path.join(root_dir, '../.tmp', hash + '.obj'), mimetype='model/obj')

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)

print("server listening on port 8080")
