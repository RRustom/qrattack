from __future__ import print_function
import requests
import json
import cv2

addr = 'http://localhost:5000'
test_url = addr + '/api/test'

payload = {'message': 'cic-health.com', 'ecc': 1, 'version': 1, 'mask': 7}

response = requests.post(test_url, data=json.dumps(payload), headers=headers)

print(response.read().decode())
