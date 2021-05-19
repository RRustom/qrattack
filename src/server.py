from flask import Flask, request, Response, jsonify, send_file
import datetime
import numpy as np
import cv2
from generate_malicious_qr import generate_malicious_qr
from generate_broken_qr import generate_broken_qr

# generate_malicious_qr('./tests/target/yahoo.png')

ECC_LEVEL = {0: 'LOW', 1: 'MEDIUM', 2: 'QUARTILE', 3: 'HIGH'}

app = Flask(__name__)

@app.route('/api/generate', methods=['GET'])
def generate():
    data = request.args

    # 1. get arguments
    message = request.args.get('message')
    ecc = request.args.get('ecc')
    ecc = ECC_LEVEL[int(ecc)]
    version = int(request.args.get('version'))
    mask = int(request.args.get('mask'))

    # attack = 1 for change, 2 for destroy
    attack = int(request.args.get('attack'))
    print("MESSAGE: ", message)
    print("VERSION: ", version)
    print("ECC: ", ecc)
    print("MASK: ", mask)

    # 2. create filename
    filename = str(datetime.datetime.now())
    print("FILENAME: ", filename)

    # change attack
    if attack == 1:
        output_path = generate_malicious_qr(message, ecc, version, mask, filename)
        return send_file(output_path, mimetype='image/png')

    output_path = generate_broken_qr(message, ecc, version, mask, filename)
    return send_file(output_path, mimetype='image/png')



@app.route('/api/test', methods=['POST'])
def test():
    data = request.get_json()
    print("GOT DATA: ", data)

    # response = {'message': "beep"}
    # response_pickled = jsonpickle.encode(response)

    return jsonify(data) # , mimetype="application/json"


# start flask app
app.run(host="0.0.0.0", port=5000)
