from flask import Flask, request, Response, jsonify, send_file
import datetime
import numpy as np
import cv2
from generate_malicious_qr import generate_malicious_qr
from generate_broken_qr import generate_broken_qr
from flask_cors import CORS

# generate_malicious_qr('./tests/target/yahoo.png')

ECC_LEVEL = {0: 'LOW', 1: 'MEDIUM', 2: 'QUARTILE', 3: 'HIGH'}

app = Flask(__name__)
CORS(app)

@app.route('/api/tamper', methods=['GET'])
def tamper():
    # 1. get arguments
    message = request.args.get('message')
    ecc = request.args.get('ecc')
    ecc = ECC_LEVEL[abs(int(ecc))]
    version = abs(int(request.args.get('version')))
    mask = abs(int(request.args.get('mask')))

    print("MESSAGE: ", message)
    print("VERSION: ", version)
    print("ECC: ", ecc)
    print("MASK: ", mask)

    # 2. create filename
    filename = str(datetime.datetime.now())
    print("FILENAME: ", filename)

    output_path = generate_malicious_qr(message, ecc, version, mask, filename)
    file = open('demo/' + output_path + '.txt',"r")
    malicious_message = file.readlines()
    file.close()
    print("MESSAGE: ", malicious_message)
    return  malicious_message[0] + '   ' + output_path#send_file(output_path, mimetype='image/png')


@app.route('/api/destroy', methods=['GET'])
def destroy():
    # 1. get arguments
    message = request.args.get('message')
    ecc = request.args.get('ecc')
    ecc = ECC_LEVEL[abs(int(ecc))]
    version = abs(int(request.args.get('version')))
    mask = abs(int(request.args.get('mask')))

    # attack = 1 for change, 2 for destroy
    print("MESSAGE: ", message)
    print("VERSION: ", version)
    print("ECC: ", ecc)
    print("MASK: ", mask)

    # 2. create filename
    filename = str(datetime.datetime.now())
    print("FILENAME: ", filename)

    output_path = generate_broken_qr(message, ecc, version, mask, filename)
    return send_file(output_path, mimetype='image/png')


@app.route('/api/get_image', methods=['GET'])
def get_image():

    # 1. get arguments
    name = request.args.get('name')

    # attack = 1 for change, 2 for destroy
    return send_file('demo/' + name + '.png', mimetype='image/png')
    #
    # # 2. create filename
    # filename = str(datetime.datetime.now())
    # print("FILENAME: ", filename)
    #
    # # change attack
    # if attack == 1:
    #     output_path = generate_malicious_qr(message, ecc, version, mask, filename)
    #
    #
    # output_path = generate_broken_qr(message, ecc, version, mask, filename)
    # return send_file(output_path, mimetype='image/png')



@app.route('/api/test', methods=['POST'])
def test():
    data = request.get_json()
    print("GOT DATA: ", data)

    # response = {'message': "beep"}
    # response_pickled = jsonpickle.encode(response)

    return jsonify(data) # , mimetype="application/json"


# start flask app
app.run(host="127.0.0.1", port=8080)
