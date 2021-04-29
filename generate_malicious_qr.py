from qrcodegen import *
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image
import qreader.qreader as qreader
# from urllib.request import urlopen

import qr
import url

def generate_malicious_qr(image_path):
    # 1. Scan the QR code (Q0) with a mobile device capable of decoding QR codes
    # and re- trieve the corresponding Message M0.
    # For the rest of the paper we assume that M0 is a URL to a website.

    try:
        m0 = qr.decode_qr_image(image_path)
    except:
        return "Error reading from " + image_path

    m0 = m0.decode("utf-8")

    # TODO: verify URL
    if not url.is_valid_url(m0):
        return "Not a valid URL"

    print("m0: ", m0)

    # TODO: get Error correction of m0: https://github.com/ewino/qreader

    # original QR code (QrCode object)
    version = 4
    mask= 0
    q0 = qr.generate_qr_code(m0, "MEDIUM", version, mask)
    ecc = qr.get_ecc_level(q0) # TODO: or just use whatever we decode?
    print("ecc level: ", ecc)

    print("q0 size: ", q0.get_size())
    print("q0 size: ", q0.get_size())
    print("q0 version: ", q0.get_version())
    print("q0 mask: ", q0.get_mask())
    print("q0 ecc: ", qr.get_ecc_level(q0))

    # 2. Generate several messages Mi, i = 1,...,n, that contain URLs to possible
    # phishing sites (the new messages are generated in a way to make them look
    # similar to the origi- nal one, e.g. by systematically changing characters
    # in the original URL).
    messages = url.generate_similar_urls(m0, 10, True, True) #[:10]
    print("# messages: ", messages)


    #print("similar messages: ", messages)

    # 3. Generate the corresponding QR codes Qi for the messages Mi, i = 1,...,n.
    # The new QR codes should use the same version and mask as the original QR code,
    # so no changes in these regions of the Code need to be done.
    qr_codes = [qr.generate_qr_code(message, ecc, version, mask) for message in messages]
    #print("qr codes: ", qr_codes)
    # for qi in qr_codes[:5]:
    #     print("     qi size: ", qi.get_size())
    #     print("     qi version: ", qi.get_version())
    #     print("     qi mask: ", qi.get_mask())
    #     print("     qi ecc: ", qr.get_ecc_level(qi))
    #     print("\n")

    # 4. Construct the symmetric difference Di of the generated QR code to the original,
    # for each q_i in qr_codes
    symmetric_diffs = [symmetric_diff(q0, q_i) for q_i in qr_codes]
    #print("symmetric diffs: ", symmetric_diffs)

    # 5. Calculate the ratios ri of modules in the symmetric differences that
    # indicate a change from white to black
    symmetric_diff_ratios = [calculate_difference_ratio(sd) for sd in symmetric_diffs]
    #print("symmetric diffs ratios: ", symmetric_diff_ratios)

    # 6. Order the QR codes by ratio ri, descending. Codes where the number of codewords
    # (not modules) that need to get changed from black to white is higher than the error-
    # correcting capacity of the code can be omitted
    ordered_codes = order_codes_by_ratio(qr_codes, symmetric_diff_ratios, ecc)
    #print("ordered codes: ", ordered_codes)

    # 7. Start with the first QR code Q1 (now sorted) and color white modules of Q0 that are black in Q1 black.
    # Check after every module, whether the meaning of the QR code can be decoded
    # and results in a different message than the original. Repeat this until a valid
    # coloring is found (for the first b elements the check can be omitted,
    # where b denotes the number of errors the BCH-encoding is capable of correcting plus one.
    # If the resulting code Q′i can get decoded to message Mi, a solution was found.
    # In step seven, the following optimization can be used:
    # Instead of coloring module by module, we simply change all modules that can be
    # changed by only using black color at once and thus generate Q′x by applying
    # the fast and simple element-wise OR-function: Q'x = Q0 OR Rx, (OR = element-wise OR)
    # Q0 = target code,
    # Q'x = generated code,
    # Rx = Qx AND Dx (AND = element-wise AND)
    # Dx = Q0 XOR Qx,
    # Qx = code in qr_codes

    valid_codes = verify_solution(q0, m0, ordered_codes)
    print("valid codes: ", valid_codes)

    # 8. The last step can be repeated for all Qi where the number of black
    # modules in the symmetric difference Di is greater than the number of errors
    # that can be corrected by the BCH-encoding (b).

    return

# Lindsey
def symmetric_diff(qr_0, qr_i):
    """Calculates symmetric difference between 2 QR codes

    Symmetric difference is the set of modules that are different colors at the
    same position on both QrCodes q_0 and q_i

    Args:
        qr_0: A QrCode object of size nxn
        qr_i: A QrCode object also of size nxn
    Returns:
        A list diffs of two lists of tuples that represent (x,y) positions on
        the qr odes. The first list diffs[0] contains tuples representing
        all of the positions where the qr_0 module was white and qr_i module
        was black, while the second list diffs[1] contains tuples representing
        the opposite: positions where qr_0 was black and qr_i was white. All
        (x,y) pairs in range (n,n) not included in either list are the same
        color in both qr_0 and qr_i.
    """
    symmetric_diffs = [[],[]]
    for y in range(qr_0.get_size()):
        for x in range(qr_0.get_size()):
            qr_0_color = qr_0.get_module(x, y)
            qr_i_color = qr_i.get_module(x, y)
            if qr_0_color != qr_i_color:
                symmetric_diffs[qr_0_color].append((x,y)) # make sure black/white interpretation is correct here linds!
    return symmetric_diffs

# Lindsey
def calculate_difference_ratio(symmetric_diffs):
    """Calculates ratio of size of symmetric_diff[0] to total elems in symmetric_diff

    From two lists of unique length-2 tuples of integers that do not overlap,
    calculates the ratio of the number of elements in the first list to the
    total number of elements included in both lists.

    Args:
        symmetric_diff: A list containing two lists of unique length-2 tuples
        of integers that do not overlap
    Returns:
        the ratio of the first list length to length of the combined lists
        if both lists are empty, returns 1
    """
    combined_lists = [pair for sublist in symmetric_diffs for pair in sublist]
    return len(symmetric_diffs[0])/len(combined_lists)

# Rami (step 6)
def order_codes_by_ratio(qr_codes, symmetric_diff_ratios, ecc):
    """Order qr_codes by symmetric_diff ratio r_i in descending order

    Args:
        qr_codes: list of QrCode objects
        symmetric_diff_ratios: list of ratios r_i
        ecc: error correction capacity of target QR code
    Returns:
        A list of ordered QrCode objects
    """

    # order qr_codes by symmetric_diff_ratios in descending order
    zipped = zip(symmetric_diff_ratios, qr_codes)
    ordered = [(ri, qr_code) for ri, qr_code in sorted(zipped, key = lambda x: x[0], reverse=True)]

    # omit qr codes where r_i is less than the error correcting capacity of target qr code
    ecc = qr.get_ecc_level_value(ecc)
    valid = []
    for (ri, qr_code) in ordered:
        if ri >= ecc:
            valid.append(qr_code)
    return valid

# Rami
def verify_solution(q0, m0, ordered_qr_codes):
    """

    Args:
        q0: a QrCode object
        m0: the message in q0
        ordered_qr_codes: a list of QrCode objects produced by order_codes_by_ratio()
    Returns:
        A list of valid QR code matrices
    """
    # 7. Start with the first QR code Q1 (now sorted) and color white modules of Q0 that are black in Q1 black.
    # Check after every module, whether the meaning of the QR code can be decoded
    # and results in a different message than the original. Repeat this until a valid
    # coloring is found (for the first b elements the check can be omitted,
    # where b denotes the number of errors the BCH-encoding is capable of correcting plus one.
    # If the resulting code Q′i can get decoded to message Mi, a solution was found.
    # In step seven, the following optimization can be used:
    # Instead of coloring module by module, we simply change all modules that can be
    # changed by only using black color at once and thus generate Q′x by applying
    # the fast and simple element-wise OR-function: Q'x = Q0 OR Rx, (OR = element-wise OR)
    # Q0 = target code,
    # Q'x = generated code,
    # Rx = Qx AND Dx (AND = element-wise AND)
    # Dx = Q0 XOR Qx,
    # Qx = code in qr_codes

    q0 = qr.qr_matrix(q0)

    valid_codes = []

    for qi in ordered_qr_codes:
        # rgb = qr.qr_matrix_rgb(qi)
        # img = Image.fromarray(rgb)
        # img.show()
        # color white modules of Q0 that are black in Q1 black. (element wise OR)
        qx = qr.qr_matrix(qi)
        # img = Image.fromarray(qx)
        # img.show()
        dx = np.logical_xor(q0, qx)
        rx = np.logical_and(qx, dx)
        qx_prime = np.logical_or(q0, rx)

        # Check after every module, whether the meaning of the QR code can be decoded
        # and results in a different message than the original.
        decoded = qr.decode_qr_matrix(qx_prime)
        if not decoded:
            continue
        if decoded != m0:
            valid_codes.append(qx_prime)

    return valid_codes


#

# url = 'https://upload.wikimedia.org/wikipedia/commons/8/8f/Qr-2.png'
# data = qreader.read(urlopen(url))
#
# #data = qreader.read('./tests/target/rickroll.png')
#
# print(data)

# a = getattr(QrCode.Ecc, "LOW")
# b = getattr(QrCode.Ecc, "MEDIUM")
# c = getattr(QrCode.Ecc, "QUARTILE")
# d = getattr(QrCode.Ecc, "HIGH")
#
# print(a.ordinal)
# print(b.ordinal)
# print(c.ordinal)
# print(d.ordinal)

generate_malicious_qr('./tests/target/rickroll.png')
