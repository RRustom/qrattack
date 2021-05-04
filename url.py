from urllib.parse import urlparse
import random

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
        parsed = urlparse(url)
        print("PARSED: ", parsed)
        protocol = parsed.scheme
        netloc = parsed.netloc
        path = parsed.path

        domains = netloc.rsplit('.',2) # Separate layers of domains
        return protocol, domains, path

    except:
        print("Failed to Parse URL:" + url)
        return None

def similar_sl_domains_random(sl_domain, n, n_replace=-1):
    """
    Creates n number of similar second level domain names.

    Args:
        sl_domain: <Str> Second level domain name
        n: <int> number of second level domain names to create
        n_replace: <int> number of characters to replace. If < 0, then randomize
    Returns:
        similar: <list> List of similar domain names
    """
    similar = []
    replacements = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                    'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                    'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7',
                    '8', '9', '0', '-', '']

    # guarantee n results
    while len(similar) < n:
        final = sl_domain
        if n_replace < 0:
            n_replace = random.randint(1, len(sl_domain)-1)
        for j in range(n_replace):
            replace_index = random.randint(0, len(sl_domain)-1)
            # choose a random replacement character
            index = random.randint(0, len(replacements)-1)
            final = final[:replace_index] + replacements[index] + final[replace_index+1:]
            if final != sl_domain:  # in the off chance the outcome is the same
                similar.append(final)
    return similar



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

    alphabet_string = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                        'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                        'w', 'x', 'y', 'z']
    number_list = [1,2,3,4,5,6,7,8,9]

    # 1 Insert random alphabetic char @ end:
    for i in alphabet_string:
        similar.append(sl_domain+i)

    # 2 Duplicate Char in middle of string:
    for i in range(len(sl_domain)-1):
        toAdd = sl_domain[:i+1] + sl_domain[i] + sl_domain[i+1:]
        similar.append(toAdd)

    # 3 Duplicate entire string?

    # 4 Add number @ end
    for i in number_list:
        similar.append(sl_domain+str(i))

    # 5 Look alike numbers and letters
    for i in range(len(sl_domain)-1):
        if sl_domain[i] == '0':
            #Replace zeros with Os
            toAdd = sl_domain[:i] + "O" + sl_domain[i+1:]
            similar.append(toAdd)
        elif sl_domain[i] == 'o' or sl_domain[i] == 'O': #Capital or lower case
            #Replace Os and os with zeros
            toAdd = sl_domain[:i] + "0" + sl_domain[i+1:]
            similar.append(toAdd)


    for i in range(len(sl_domain)-1):
        if sl_domain[i] == '1':
            #Replace ones with l
            toAdd = sl_domain[:i] + "l" + sl_domain[i+1:]
            similar.append(toAdd)
        elif sl_domain[i] == 'l' or sl_domain[i] == 'L': #Capital or lower case
            #Replace l and L with ones
            toAdd = sl_domain[:i] + "1" + sl_domain[i+1:]
            similar.append(toAdd)

    # We change at most 1 character in a url...

    return similar[:min(len(similar), n)]

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
    protocol, domains, filename = parse_url(url)

    if len(domains) == 3:
        sub_domains, sl_domain, tl_domain = domains
    elif len(domains) == 2:
        sl_domain, tl_domain = domains
        sub_domains = ""


    #Init empty list to store output
    output_urls = []

    #Generate similar sl_domains
    similar = similar_sl_domains_random(sl_domain, num_similar)

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

def generate_similar_strings(url):
    # TODO (1.1)
    return

def generate_similar_payloads(url):
    # TODO (2.0)
    return

# url = "https://www.geeksforgeeks.org/python-generate-random-string-of-given-length/"
# print(is_valid_url(url))

#
# m = 'youtube'
# mes = similar_sl_domains_random(m, 10, 2)
# m = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
# mes = generate_similar_urls(m, 100)
# print(len(mes))
# print(mes)
