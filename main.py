from qrcodegen import *
from pyzbar.pyzbar import decode
from PIL import Image



def generate_malicious_qr(image_path):
    [decoded] = decode(Image.open(image_path))
    # 1. Scan the QR code (Q0) with a mobile device capable of decoding QR codes
    # and re- trieve the corresponding Message M0.
    # For the rest of the paper we assume that M0 is a URL to a website.
    m0 = decoded.data

    # TODO: verify URL
    if not is_valid_url(m0):
        return

    # 2. Generate several messages Mi, i = 1,...,n, that contain URLs to possible
    # phishing sites (the new messages are generated in a way to make them look
    # similar to the origi- nal one, e.g. by systematically changing characters
    # in the original URL).
    messages = generate_similar_urls(m0)

    # 3. Generate the corresponding QR codes Qi for the messages Mi, i = 1,...,n.
    # The new QR codes should use the same version and mask as the original QR code,
    # so no changes in these regions of the Code need to be done.
    qr_codes = [generate_qr_code(message) for message in messages]

    # 4. Construct the symmetric difference Di of the generated QR code to the original:
    # Di = Q0 △Qi, i = 1,...,n. The symmetric difference is defined as the set of
    # modules on the same positions in their respective QR codes that differ in color.
    symmetric_diff()

    # 5. Calculate the ratios ri of modules in the symmetric differences that
    # indicate a change from white to black (thus fulfilling our initial condition):
    calculate_difference_ratio()

    # 6. Order the QR codes by ratio ri, descending. Codes where the number of codewords
    # (not modules) that need to get changed from black to white is higher than the error-
    # correcting capacity of the code can be omitted.
    # non trivial?
    step_6()

    # 7. Start with the first QR code Q1 (now sorted) and color white modules of Q0 that are black in Q1 black.
    # Check after every module, whether the meaning of the QR code can be decoded
    # and results in a different message than the original. Repeat this until a valid
    # coloring is found (for the first b elements the check can be omitted,
    # where b denotes the number of errors the BCH-encoding is capable of correcting plus one.
    # If the resulting code Q′i can get decoded to message Mi, a solution was found.
    verify_solution()

    # 8. The last step can be repeated for all Qi where the number of black
    # modules in the symmetric difference Di is greater than the number of errors
    # that can be corrected by the BCH-encoding (b).

    return

# Eric
def is_valid_url(url):
    # TODO
    return

# Eric
def generate_similar_urls(url):
    # TODO: non-trivial
    # TODO (1.0)
    # constraints:
    #   - same length
    #   - same top level domain
    #   - play around with subdomains? maybe NO subdomains?
    #   - restricted characters
    #   - maybe check if URL is available?
    return

def generate_similar_strings(url):
    # TODO (1.1)
    return

def generate_similar_payloads(url):
    # TODO (2.0)
    return

def generate_qr_code(message):
    """Generates QR code corresponding to message

    Args:
        message: a string containing desired message
    Returns:
        A QrCode object that encodes message.
    """
    return

# Rami
def symmetric_diff(q_0, q_i):
    """Calculates symmetric difference between 2 QR codes

    Symmetric difference is the set of modules that are different colors at the
    same position on both QrCodes q_0 and q_i

    Args:
        q_0: A QrCode object
        q_i: A QrCode object
    Returns:
        A ???[set?list?other?] that contains all the modules that at the same
        locations in q_0 and q_1 are not the same color.
    """
    # TODO: non-trivial
    return

# Lindsey
def calculate_difference_ratio():
    """Calculates ratio of white to black module changes

    From the ???[set?list?other?] of modules that differed between two QrCodes,
    finds the ratio of the chages that where changed from white to black

    Args:
        q_0: A QrCode object
        q_i: A QrCode object
    Returns:
        A ???[set?list?other?] that contains all the modules that at the same
        locations in q_0 and q_1 are not the same color.
    """
    return

# Lindsey
def step_6():
    return

# Rami
def verify_solution():
    # TODO: non-trivial
    return


# qr0 = QrCode.encode_text("Hello, world!", QrCode.Ecc.MEDIUM)
# svg = qr0.to_svg_str(4)
#
# output_file = open("qr0.txt", 'w+')
#
# output_file.write(svg)
#
# output_file.close()
#

generate_malicious_qr('test_qrcode.png')
