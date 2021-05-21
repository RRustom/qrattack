import qr
import cv2
import copy
import numpy as np
from PIL import Image


def generate_broken_qr(message, ecc, version, mask, filename):
    q0 = qr.generate_qr_code(message, ecc, version, mask)
    qr_matrix = qr.qr_matrix(q0) #0,1
    deep_copy = copy.deepcopy(qr_matrix)
    broken_qr_matrix = cover_format_modules(qr_matrix)#0,1 plus borkenness

    diff = qr.qr_diff(deep_copy, broken_qr_matrix) # a greyscale numpy array with values that are either 0 (black) or 255
    print(diff)
    # q0 is numpy array that has values of either 0 or 1

    greyscale_qr_good = qr.qr_matrix_rgb_from_matrix(deep_copy) #This converts q0 to greyscale 0,1 -> 0,255
    rgb_qr_good=cv2.cvtColor(greyscale_qr_good, cv2.COLOR_GRAY2RGB) #convert greyscale original to RGB

    diff_color = cv2.cvtColor(diff, cv2.COLOR_GRAY2RGB)
    rgb_qr_good[np.all(diff_color == (0, 0, 0), axis=-1)] = (255, 0, 0)

    img= Image.fromarray(rgb_qr_good, 'RGB')

    output_path = 'demo/' + filename + '.png'
    qr.qr_matrix_image(rgb_qr_good, output_path, show=True)
    return output_path


def cover_format_modules(qr_matrix):
    """
    Takes in numpy matrix of qr_matrix and changes any 0s in the format
    specification areas to 1s
    """
    for i in range(8):
        qr_matrix[8][i] = 1 # horizontal top left
        qr_matrix[8][-i] = 1 # horizontal top right
        qr_matrix[i][8] = 1 # vertical top left
        qr_matrix[-i][8] = 1 # vertical bottom left
    return qr_matrix

if __name__ == '__main__':
    # q0 = qr.generate_qr_code('http://cic-health.com', 'ecc', version, mask)
    generate_broken_qr('http://yahoo.at', 'MEDIUM', 2, 7, 'broken_yahoo')
