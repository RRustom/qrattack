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

def hamming_circle(domain, top_level, n, alphabet):
    """Generate strings over alphabet whose Hamming distance from s is
    exactly n.

    >>> sorted(hamming_circle('abc', 0, 'abc'))
    ['abc']
    >>> sorted(hamming_circle('abc', 1, 'abc'))
    ['aac', 'aba', 'abb', 'acc', 'bbc', 'cbc']
    >>> sorted(hamming_circle('aaa', 2, 'ab'))
    ['abb', 'bab', 'bba']

    """
    for positions in combinations(range(len(domain)), n):
        for replacements in product(range(len(alphabet)-1), repeat=n):
            cousin = list(domain)
            for p, r in zip(positions, replacements):
                if cousin[p] == alphabet[r]:
                    cousin[p] = alphabet[-1]
                else:
                    cousin[p] = alphabet[r]
            word = ''.join(cousin)
            if is_valid_domain(word, top_level):
                yield word + '.' + top_level#"http://" + word + '.' + top_level

def generate_messages(url, distance):
    parsed = urlparse(url)
    print("PARSED: ", parsed)
    domain, top_level = parsed.path.rsplit('.', 2)
    print('DOMAIN: ', domain)
    print('TOP_LEVEL: ', top_level)
    messages = list(hamming_circle(domain, top_level, distance, ''.join(replacements)))
    #print(messages)
    return messages

# m = generate_messages("web.mit", 2)
# print(len(m))
# print(len(set(m)))
