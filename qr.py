from qrcodegen.qrcodegen import *
import numpy as np
from PIL import Image
import cv2
import tempfile
import zxingcpp
import time

ECC = ["LOW", "MEDIUM", "QUARTILE", "HIGH"]

ECC_VALUES = {
    "LOW": 0.07,
    "MEDIUM": 0.15,
    "QUARTILE": 0.25,
    "HIGH": 0.3
}

QR_CODE_MIN_VERSION = 1
QR_CODE_MAX_VERSION = 40
QR_CODE_MIN_MASK = 0
QR_CODE_MAX_MASK = 7

def get_qr_info(image_path):
    """Get Error Correction leve, QR Code Version, and Mask from QR image

    Args:
        image_path: path of image (png)
    Returns:
        ecc: one of ECC_VALUES
		version: version between QR_CODE_MIN_VERSION and QR_CODE_MAX_VERSION (inclusive)
		mask: mask between QR_CODE_MIN_MASK and QR_CODE_MAX_MASK (inclusive)
    """
    result = zxingcpp.read_barcode(cv2.imread(image_path))
    message = result.text
    image = Image.open(image_path)
    q0 = np.asarray(image)

    for ecc in ["LOW", "MEDIUM", "QUARTILE", "HIGH"]:
        for version in range(QR_CODE_MIN_VERSION, QR_CODE_MAX_VERSION + 1):
            for mask in range(QR_CODE_MIN_MASK, QR_CODE_MAX_MASK + 1):
                try:
                    qi = generate_qr_code(message, ecc, version, mask)
                    qi_matrix = qr_matrix_rgb(qi)
                    if np.array_equal(q0, qi_matrix):
                        return ecc, version, mask
                except:
                    continue
    return "Could not parse info"

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
    img = cv2.imread(image_path)
    result = zxingcpp.read_barcode(img)
    return result.text

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

def qr_matrix_rgb_from_matrix(qr_matrix):
    size = qr_matrix.size
    qr_matrix = (1 - qr_matrix)*255
    m = qr_matrix.astype('uint8')
    return cv2.resize(m, dsize=(1000, 1000), interpolation=cv2.INTER_NEAREST)

def decode_qr_matrix(qr_matrix):
    """Decode a binary matrix representation of a QR code (entries 0 or 1)

    Args:
        qr_matrix: np.ndarray matrix representation of QR code
    Returns:
        A bytestring of data in QR code.
    """
    qr_matrix_rgb = qr_matrix_rgb_from_matrix(qr_matrix)

    # image = Image.fromarray(qr_matrix_rgb)
	#
    # fp = tempfile.NamedTemporaryFile(suffix=".png")
    # image.save(fp.name)
	#
    # img = cv2.imread(fp.name)
    result = zxingcpp.read_barcode(qr_matrix_rgb)
    if result.valid:
        #print("Found barcode with value '{}' (format: {})".format(result.text, str(result.format)))
        #fp.close()
        return result.text

    #fp.close()
    return False

def qr_matrix_image(qr_matrix, image_path, show=False):
    """Save a PNG of qr_matrix at image_path

    Args:
        qr_matrix: np.ndarray matrix representation of QR code
		image_path: path to PNG
		show: boolean to open image
    """
    rgb_matrix = qr_matrix_rgb_from_matrix(qr_matrix)
    img = Image.fromarray(rgb_matrix)
    img.save(image_path)
    if show:
        img.show()

def qr_diff(qr0_matrix, qr1_matrix):
    """Calculate the difference between two QR code matrixes

    Args:
        qr0_matrix: np.ndarray matrix representation of QR code
		qr1_matrix: np.ndarray matrix representation of QR code
    Returns:
        qr1_matrix - qr0_matrix
    """
    size = qr0_matrix.size
    qr0_matrix = (1 - qr0_matrix)*255
    qr1_matrix = (1 - qr1_matrix)*255
    black_diff = 255 - qr0_matrix + qr1_matrix
    #return black_diff
    m = black_diff.astype('uint8')
    return cv2.resize(m, dsize=(1000, 1000), interpolation=cv2.INTER_NEAREST)
# # TEST
#
# m = 'http://mit.edu'
# ecc = "MEDIUM"
# mask = 7
# version = 1
# q = generate_qr_code(m, ecc, version, mask)
# q0 = qr_matrix(q)
# rgb_matrix = qr_matrix_rgb_from_matrix(q0)
# img1 = Image.fromarray(rgb_matrix)
# img1.save('tests/target/mit.png')
# #img1.show()
#
# # m1 = ''
# # qi = generate_qr_code(m1, ecc, version, mask)
# # q1 = qr_matrix(qi)
# # rgb_matrix1 = qr_matrix_rgb_from_matrix(q1)
# # img2 = Image.fromarray(rgb_matrix1)
# # img2.save('yahoo1.png')
# # #img2.show()
# #
# # diff = qr_diff(q0, q1)
# # img = Image.fromarray(diff)
# # img.save('yahoo_diff.png')
# # img.show()
# # #
# p = 'tests/target/mit.png'
# print(get_qr_info(p))



# #print(m)
# rgb = qr_matrix_rgb_from_matrix(m)
# #print(rgb)
# img = Image.fromarray(rgb)
# img.show()


#
#
# # # svg = qr0.to_svg_str(4)
# # #
# # output_file = open("qr_test.txt", 'w+')
# #
# # for y in range(qr.get_size()):
# #     for x in range(qr.get_size()):
# #         module = qr.get_module(x, y)
# #         b = 1 if module else 0
# #         output_file.write(str(b) + " ")
# #     output_file.write("\n")
# #
# # output_file.close()
#
#
# p = 'tests/target/rickroll_large.png'
# start = time.time()
# print(get_qr_info(p))
# print("TIME: ", time.time() - start)
#
# # m = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
# # ecc = "MEDIUM"
# # mask = 7
# # version = 39
# # q = generate_qr_code(m, ecc, version, mask)
# # qm = qr_matrix(q)
# # qr_matrix_image(qm, 'tests/target/rickroll_1.png')
#
#
# # #m0 = qr.decode_qr_image(image_path)
# # img = cv2.imread(p)
# # img_matrix = np.resize(img, (1000, 1000))
# # print("OLD SHAPE: ", img_matrix.shape)
# # #print(img_matrix)
# #
# # image = Image.open(p)
# # old = np.asarray(image)
# # print(old)
# #
# # version = 1
# # mask= 7
# # m0 = "http://yahoo.at"
# # q0 = generate_qr_code(m0, "LOW", version, mask)
# # q0_matrix = qr_matrix_rgb(q0)
# # #qr_matrix_image(q0_matrix, 'tests/malicious/yahoo_m.png')
# # print("NEW SHAPE: ", q0_matrix.shape)
# # print(q0_matrix)
# #
# # print("EQUAL: ", np.array_equal(q0_matrix, old))
#
# #return result.text
