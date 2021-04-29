from qrcodegen.qrcodegen import *
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image
import cv2

ECC = ["LOW", "MEDIUM", "QUARTILE", "HIGH"]

ECC_VALUES = {
    "LOW": 0.07,
    "MEDIUM": 0.15,
    "QUARTILE": 0.25,
    "HIGH": 0.3
}

def get_ecc_level(qr):
    return ECC[qr.get_error_correction_level().ordinal]

def get_ecc_level_value(ecc):
    return ECC_VALUES[ecc]


def decode_qr_image(image_path):
    """Decodes the QR code at image_path

    Args:
        image_path: path of image (png)
    Returns:
        A bytestring of data in QR code.
    """
    return decode(Image.open(image_path))[0].data

# m = 'Hello, world!'
# ecc = "QUARTILE"
# mask = 0
# version = 4

def generate_qr_code(message, ecc, version, mask):
    """Generates QR code corresponding to message

    Args:
        message: a string containing desired message
        ecc: a string Error correction level: "LOW", "MEDIUM", "QUARTILE", "HIGH"
    Returns:
        A QrCode object that encodes message.
    """
    if type(message) is str:
        pass
    if type(message) is bytes:
        message = message.decode("utf-8")

    return QrCode.encode_text(message, getattr(QrCode.Ecc, ecc), version, mask)

# q = generate_qr_code(m, ecc, version, mask)

def qr_matrix_rgb(qr):
    """Create an np.ndarray matrix from a QrCode object with RGB values
        that is interpolated to a 1000x1000 matrix.

    Args:
        qr: a QrCode object
    Returns:
        An np.ndarray matrix of size (1000,1000) with 0 for black, 255 for white
    """
    matrix = []
    size = qr.get_size()
    for y in range(size):
        for x in range(size):
            value = 0 if qr.get_module(x, y) else 255
            matrix.append(value)
    m = np.array(matrix).reshape((size, size)).astype('uint8')
    return cv2.resize(m, dsize=(1000, 1000), interpolation=cv2.INTER_NEAREST)

def qr_matrix(qr):
    """Create a binary np.ndarray matrix from a QrCode object

    Args:
        qr: a QrCode object
    Returns:
        An np.ndarray matrix with 0s and 1s
    """
    matrix = []
    for y in range(qr.get_size()):
        row = []
        for x in range(qr.get_size()):
            value = 1 if qr.get_module(x, y) else 0
            row.append(value)
        matrix.append(row)
    return np.array(matrix)

# m = qr_matrix(q)
#
# print(m)

def qr_matrix_rgb_from_matrix(qr_matrix):
    size = qr_matrix.size
    qr_matrix = (1 - qr_matrix)*255
    m = qr_matrix.astype('uint8')
    return cv2.resize(m, dsize=(1000, 1000), interpolation=cv2.INTER_NEAREST)

# rgb = qr_matrix_rgb_from_matrix(m)
#
# print(rgb)

def decode_qr_matrix(qr_matrix):
    """Decode a binary matrix representation of a QR code (entries 0 or 1)

    Args:
        qr_matrix: np.ndarray matrix representation of QR code
    Returns:
        A bytestring of data in QR code.
    """
    qr_matrix = qr_matrix_rgb_from_matrix(qr_matrix)
    # img = Image.fromarray(qr_matrix)
    # img.show()
    try:
        [decoded] = decode(qr_matrix)
        if decoded.data:
            return decoded.data
    except:
        return False
    return False

# def can_be_decoded(qr_matrix):
#     """
#     """
#     #(height, width) = qr_matrix.shape
#     if generate_qr_from_matrix(qr_matrix):
#         return True
#     return False

def qr_to_svg(qr):
    # TODO
    return

def show_qr_diff(qr0, qr1):
    # TODO
    return

# img = Image.fromarray(rgb)
# img.show()


# # svg = qr0.to_svg_str(4)
# #
# output_file = open("qr_test.txt", 'w+')
#
# for y in range(qr.get_size()):
#     for x in range(qr.get_size()):
#         module = qr.get_module(x, y)
#         b = 1 if module else 0
#         output_file.write(str(b) + " ")
#     output_file.write("\n")
#
# output_file.close()