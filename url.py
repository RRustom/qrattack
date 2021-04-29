import requests

# Eric
def is_valid_url(url):
    '''
    Checks vaidity of url; Assumes prefix of http:// or https://

    Args:
        url: string representing a URL
    Returns:
        Boolean indicating validity of url
    '''
    r = requests.get(url)
    return r.status_code == requests.codes.ok # Check for status code 200

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
    url = protocol + '://' + sub_domains + '.' + sl_domain + '.' + tl_domain + '/' + filename
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

    protocol, hostname_filename = url.split('://') # Extract http vs https
    hostname, filename = hostname_filename.split('/', 1) # Separate host from filename
    sub_domains, sl_domain, tl_domain = hostname.rsplit('.',2) # Separate layers of domains
    return protocol, sub_domains, sl_domain, tl_domain, filename


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
    for i in alphabet_string:
        similar.append(sl_domain+i)
    # 2 Duplicate Char in middle of string:
    # 3 Duplicate entire string
    # 4 Add number
    return similar

def generate_similar_urls(url, num_similar, with_sub_domains = False, with_filename = False):
    '''
    Creates a specified number of urls that are similar to the url provided.

    Args:
        url: <Str> a full url, starting with 'http' or 'https'
        num_similar: <int> number of similar urls to create
        with_sub_domains: <bool> Indicates if output urls should have subdomains
        with_filename: <bool> indicates if output urls should have filenames
    Returns:
        output_urls: <list> containing <str> list of similar domain names
    '''
    # TODO (1.0)
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
        else:
            url = build_url(
                            protocol = protocol,
                            sl_domain = new_sl_domain,
                            tl_domain = tl_domain,
                            )

        output_urls.append(url)

    return output_urls

# url = "https://www.geeksforgeeks.org/python-generate-random-string-of-given-length/"
# print(is_valid_url(url))
# print(generate_similar_urls(url, 2))
