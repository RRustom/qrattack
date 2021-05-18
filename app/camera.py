import cv2
import zxingcpp
import numpy as np
from qr import decode_qr_image_nopath, qr_matrix_image, qr_matrix_rgb_from_matrix



def decoder(image):
    gray_array = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # result = zxingcpp.read_barcode(gray_array)
    # is_valid_qr = result.valid
    # if is_valid_qr:
    #     cv2.imwrite("camera_test.png", gray_array)
    #     position = result.position
    #     points = np.array([(position.top_left.x, position.top_left.y),
    #             (position.top_right.x, position.top_right.y),
    #             (position.bottom_right.x, position.bottom_right.y),
    #             (position.bottom_left.x, position.bottom_left.y)
    #             ], np.int32)
    #     points = points.reshape((-1, 1, 2))
    #     color = (0, 0, 255)
    #     thickness = 5
    #     cv2.polylines(image, [points], True, color, thickness)
    #     print("Found barcode:\n Text:    '{}'\n Format:   {}\n Position: {}".format(result.text, result.format, position))
    # return is_valid_qr

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    valid = decoder(frame)
    cv2.imshow('Image', frame)
    code = cv2.waitKey(10)
    if code == ord('q'):
        break
