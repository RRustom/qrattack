from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2
from generate_malicious_qr import generate_malicious_qr

# generate_malicious_qr('./tests/target/yahoo.png')

app = Flask(__name__)

@app.route('/api/test', methods=['POST'])
def test():
    print("!!!!!!!HERE")
    print(request.form)
    print(request.form['message'])

    response = {'message': "beep"}
    response_pickled = jsonpickle.encode(response)

    return Response(response=response, status=200, mimetype="application/json")


# start flask app
app.run(host="0.0.0.0", port=5000)
