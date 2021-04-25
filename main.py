from qrcodegen import *
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image

def generate_malicious_qr(image_path):
    # [decoded] = decode(Image.open(image_path))
    # 1. Scan the QR code (Q0) with a mobile device capable of decoding QR codes
    # and re- trieve the corresponding Message M0.
    # For the rest of the paper we assume that M0 is a URL to a website.
    # m0 = decoded.data
    m0 = 0

    # TODO: verify URL
    if not is_valid_url(m0):
        return

    # original QR code (QrCode object)
    q0 = generate_qr_code(m0)
    ecc = q0.get_error_correction_level() # TODO: or just use whatever we decode?

    # 2. Generate several messages Mi, i = 1,...,n, that contain URLs to possible
    # phishing sites (the new messages are generated in a way to make them look
    # similar to the origi- nal one, e.g. by systematically changing characters
    # in the original URL).
    messages = generate_similar_urls(m0)

    # 3. Generate the corresponding QR codes Qi for the messages Mi, i = 1,...,n.
    # The new QR codes should use the same version and mask as the original QR code,
    # so no changes in these regions of the Code need to be done.
    qr_codes = [generate_qr_code(message) for message in messages]

    # 4. Construct the symmetric difference Di of the generated QR code to the original,
    # for each q_i in qr_codes
    symmetric_diffs = [symmetric_diff(q_0, q_i) for q_i in qr_codes]

    # 5. Calculate the ratios ri of modules in the symmetric differences that
    # indicate a change from white to black
    symmetric_diff_ratios = [calculate_difference_ratio(sd) for sd in symmetric_diffs]

    # 6. Order the QR codes by ratio ri, descending. Codes where the number of codewords
    # (not modules) that need to get changed from black to white is higher than the error-
    # correcting capacity of the code can be omitted
    ordered_codes = order_codes_by_ratio(qr_codes, symmetric_diff_ratios, ecc)

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

    verify_solution()

    # 8. The last step can be repeated for all Qi where the number of black
    # modules in the symmetric difference Di is greater than the number of errors
    # that can be corrected by the BCH-encoding (b).

    return

# Eric
def is_valid_url(url):
    '''
    Checks vaidity of url using parse_url helper function.

    Args:
        url: string representing a URL
    Returns:
        Boolean indicating validity of url
    '''
    valid = False
    if parse_url(url) is not None:
        valid = True
    return valid

# Eric

def build_url(protocol, sl_domain, tl_domain, sub_domains='', filename=''):
    '''
    Constructs URL given protocol, second level domain, top level domain, any
    subdomain (optional), and any filename (optional).

    Args:
        protocol: <str> either 'http' or 'https'
        sl_domain: <str> Second level domain name, i.e. website name
        tl_domain: <str> Top Level domain name, i.e. 'com', 'org', 'net'
        subdomains: <str> a subdomain, i.e. 'blog' or 'blog.home'
        filename: <str> any filename on the website
    Returns:
        url: <str> a url
    '''
    if sub_domains: #things like www
        url = protocol + '://' + sub_domains + '.' + sl_domain + '.' + tl_domain + '/' + filename
    else: #eliminnates www.
        url = protocol + '://' + sl_domain + '.' + tl_domain + '/' + filename
    return url

def parse_url(url):
    '''
    Constructs URL given protocol, second level domain, top level domain, any
    subdomain (optional), and any filename (optional).

    Args:
        url: <str> a url
    Returns:
        <list> containing the following...
            protocol: <str> either 'http' or 'https'
            subdomains: <str> a subdomain, i.e. 'blog' or 'blog.home'
            sl_domain: <str> Second level domain name, i.e. website name
            tl_domain: <str> Top Level domain name, i.e. 'com', 'org', 'net'
            filename: <str> any filename on the website
    '''
    try:
        protocol, hostname_filename = url.split('://') # Extract http vs https
        hostname, filename = hostname_filename.split('/', 1) # Separate host from filename
        sub_domains, sl_domain, tl_domain = hostname.rsplit('.',2) # Separate layers of domains
        return protocol, sub_domains, sl_domain, tl_domain, filename

    except:
        print("Failed to Parse URL:" + url)
        return None



def similar_sl_domains(sl_domain, n):
    '''
    Creates n number of similar second level domain names.

    Args:
        sl_domain: <Str> Second level domain name
        n: <int> number of second level domain names to create
    Returns:
        similar: <list> List of similar domain names
    '''
    similar = []
    # 1 Insert random alphabetic char:
    alphabet_string = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                        'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                        'w', 'x', 'y', 'z']
    number_list = [1,2,3,4,5,6,7,8,9]
    for i in alphabet_string:
        similar.append(sl_domain+i)
    # 2 Duplicate Char in middle of string:
    for i in range(len(sl_domain)-1):
        toAdd = sl_domain[:i] + sl_domain[i] + sl_domain[i+1:]
        similar.append(toAdd)
    # 3 Duplicate entire string
    # 4 Add number
    for i in number_list:
        similar.append(sl_domain+str(i))

    #Could do more sophisticated things like replace letters with look alike numbers
    return similar

def generate_similar_urls(url, num_similar, with_sub_domains = False, with_filename = False):
    '''
    Creates a specified number of urls that are similar to the url provided; assumes
    url provided has been checked for validity.

    Args:
        url: <Str> a full url, starting with 'http' or 'https'
        num_similar: <int> number of similar urls to create
        with_sub_domains: <bool> Indicates if output urls should have subdomains
        with_filename: <bool> indicates if output urls should have filenames
    Returns:
        output_urls: <list> containing <str> list of similar domain names
    '''
    # constraints:
    #   - same length
    #   - same top level domain: https://www.icann.org/resources/pages/tlds-2012-02-25-en
    #   - play around with subdomains? maybe NO subdomains?
    #   - restricted characters
    #   - maybe check if URL is available?

    #Split url input into key components
    protocol, sub_domains, sl_domain, tl_domain, filename = parse_url(url)

    #Init empty list to store output
    output_urls = []

    #Generate similar sl_domains
    similar = similar_sl_domains(sl_domain = sl_domain, n = num_similar)

    # iterate through similar urls
    for i in similar:
        new_sl_domain = i

        if with_sub_domains and with_filename: #inefficient to check every time
            url = build_url(
                            protocol = protocol,
                            sl_domain = new_sl_domain,
                            tl_domain = tl_domain,
                            sub_domains=sub_domains,
                            filename=filename
                            )
        elif with_sub_domains:
            url = build_url(
                            protocol = protocol,
                            sl_domain = new_sl_domain,
                            tl_domain = tl_domain,
                            sub_domains=sub_domains,
                            )
        elif with_filename:
            url = build_url(
                            protocol = protocol,
                            sl_domain = new_sl_domain,
                            tl_domain = tl_domain,
                            filename=filename
                            )
        else: #Default
            url = build_url(
                            protocol = protocol,
                            sl_domain = new_sl_domain,
                            tl_domain = tl_domain,
                            )

        output_urls.append(url)

    return output_urls

url = "https://www.geeksforgeeks.org/python-generate-random-string-of-given-length/"
print(is_valid_url(url))
print(generate_similar_urls(url, 2))

def generate_similar_strings(url):
    # TODO (1.1)
    return

def generate_similar_payloads(url):
    # TODO (2.0)
    return

def generate_qr_code(message, ecc):
    """Generates QR code corresponding to message

    Args:
        message: a string containing desired message
        ecc: a string Error correction level: "LOW", "MEDIUM", "QUARTILE", "HIGH"
    Returns:
        A QrCode object that encodes message.
    """
    return QrCode.encode_text(message, getattr(QrCode.Ecc, ecc))

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
    # LOW = 0.07
    # MEDIUM = 0.15
    # QUARTILE = 0.25
    # HIGH = 0.3

    # order qr_codes by symmetric_diff_ratios in descending order
    ordered = [qr for ri, qr in sorted(zip(symmetric_diff_ratios, qr_codes), reverse=True)]

    # omit qr codes where r_i is less than the error correcting capacity of target qr code
    return list(filter(lambda x: ri <= ecc, ordered))

# Rami
def verify_solution(q0, m0, ordered_qr_codes):
    """TODO
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

    q0 = qr_matrix(q0)

    valid_codes = []

    for qi in ordered_qr_codes:
        # color white modules of Q0 that are black in Q1 black. (element wise OR)
        qx = qr_matrix(qi)
        dx = np.logical_xor(q0, qx)
        rx = np.logical_and(qx, dx)
        qx_prime = np.logical_or(q0, rx)

        # Check after every module, whether the meaning of the QR code can be decoded
        # and results in a different message than the original.

        # TODO: manually generate QR code
        # qx_prime = generate_qr_from_matrix(qx_prime_matrix)

        if can_be_decoded(qx_prime):
            valid_codes.append(qx_prime)

    return valid_codes

def generate_qr_from_matrix(qr_matrix):
    # TODO
    return

def can_be_decoded(qr_matrix):
    """
    """
    (height, width) = qr_matrix.shape
    try:
        decoded = decode(qr_matrix, width, height)
        return True
    except:
        return False


def qr_matrix(qr):
    """
    TODO
    """
    matrix = []
    for y in range(qr.get_size()):
        row = []
        for x in range(qr.get_size()):
            row.append(qr.get_module(x, y))
        matrix.append(row)
    return np.array(matrix)



# qr = QrCode.encode_text("Hello, world!", QrCode.Ecc.MEDIUM)
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
#

#generate_malicious_qr('test_qrcode.png')
