from itertools import chain, combinations, product
from urllib.parse import urlparse
import re

# https://codereview.stackexchange.com/questions/88912/create-a-list-of-all-strings-within-hamming-distance-of-a-reference-string-with

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k','l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v','w', 'x', 'y', 'z']
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
characters = ['-']#['.', '-']
replacements = alphabet + numbers + characters

def is_valid_domain(domain, top_level):
    # https://www.geeksforgeeks.org/how-to-validate-a-domain-name-using-regular-expression/
    regex = "^((?!-)[A-Za-z0-9-]{1,63}(?<!-)\\.)+[A-Za-z]{2,6}"
    # Compile the ReGex
    p = re.compile(regex)

    str = domain + '.' + top_level

    # If the string is empty
    # return false
    if (str == None):
        return False

    # Return if the string
    # matched the ReGex
    if(re.search(p, str)):
        return True
    else:
        return False
    return

def hamming_circle(protocol, domain, top_level, path, n, alphabet, scramble_path):
    """Generate strings over alphabet whose Hamming distance from s is
    exactly n.

    >>> sorted(hamming_circle('abc', 0, 'abc'))
    ['abc']
    >>> sorted(hamming_circle('abc', 1, 'abc'))
    ['aac', 'aba', 'abb', 'acc', 'bbc', 'cbc']
    >>> sorted(hamming_circle('aaa', 2, 'ab'))
    ['abb', 'bab', 'bba']

    """
    seed = domain #specify which text to scramble
    if len(path) > 1 and scramble_path: #Its not empty string or just a slash
        seed = domain+path[1:] #cut off slash

    for positions in combinations(range(len(seed)), n):
        for replacements in product(range(len(alphabet)-1), repeat=n):
            cousin = list(seed)
            for p, r in zip(positions, replacements):
                if cousin[p] == alphabet[r]:
                    cousin[p] = alphabet[-1]
                else:
                    cousin[p] = alphabet[r]
            word = ''.join(cousin)
            if is_valid_domain(word, top_level):
                if len(path) > 1 and scramble_path: #we scrambled the path too
                    sd = word[:len(domain)]
                    path = '/' + word[len(domain):]
                    to_yield = protocol + word + '.' + top_level + path
                else:
                    sd = word
                    to_yield = protocol + word + '.' + top_level + path
                yield to_yield

def url_extraction(url):

    protocol = ''
    url_without_protocol = url
    if '://' in url:
        protocol, url_without_protocol = url.split('://')
        protocol = protocol + '://' #add this to protocol

    path = ''
    domains = url_without_protocol
    if '/' in url_without_protocol:
        domains, path = url_without_protocol.split('/', 1)
        path = '/' + path #only want slash after tld if it showed up in original

    subdomains = ''
    tld = domains
    if '.' in domains:
        subdomains, tld = domains.rsplit('.', 1)
    else:
        raise ValueError('url has no TLD')

    return [protocol, subdomains, tld, path]


def generate_messages(url, distance, scramble_path = False):
    p, sd, tld, path = url_extraction(url)
    print('DOMAIN: ', sd)
    print('TOP_LEVEL: ', tld)
    messages = list(hamming_circle(p, sd, tld, path, distance, ''.join(replacements), scramble_path))
    #print(messages)
    return messages

# m = generate_messages("yahoo.com/", 2, True)
# print(m)
# print(len(set(m)))

# m0='yahoo.com'
# m1='http://yahoo.com'
# m2='http://news.yahoo.com'
# m3='http://news.yahoo.com/hello'
#
# url_extraction('a.com')
