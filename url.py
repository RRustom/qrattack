from urllib.parse import urlparse
import random
from concurrent.futures import ProcessPoolExecutor

REPLACEMENTS = set(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7',
                '8', '9', '0', '-', '.', ' '])

TL_DOMAINS = set(['com', 'net', 'org', 'dev', 'app', 'inc', 'website', 'io', 'co', 'ai',
                'me', 'biz', 'blog', 'site', 'onl', 'to', 'bz', 'us', 'page'])
# https://www.namecheap.com/domains/new-tlds/explore/

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
        protocol = parsed.scheme
        netloc = parsed.netloc
        path = parsed.path

        domains = netloc.rsplit('.',2) # Separate layers of domains
        return protocol, domains, path

    except:
        print("Failed to Parse URL:" + url)
        return None

# def similar_sl_domains_random(sl_domain, n, n_replace=-1):
#     """
#     Creates n number of similar second level domain names.
#
#     Args:
#         sl_domain: <Str> Second level domain name
#         n: <int> number of second level domain names to create
#         n_replace: <int> number of characters to replace. If < 0, then randomize
#     Returns:
#         similar: <list> List of similar domain names
#     """
#     similar = []
#     REPLACEMENTS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
#                     'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
#                     'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7',
#                     '8', '9', '0', '-', '.', ' ']
#
#     # guarantee n results
#     while len(similar) < n:
#         final = sl_domain
#         if n_replace < 0:
#             n_replace = random.randint(1, len(sl_domain)-1)
#         for j in range(n_replace):
#             replace_index = random.randint(0, len(sl_domain)-1)
#             # choose a random replacement character
#             index = random.randint(0, len(REPLACEMENTS)-1)
#             final = final[:replace_index] + REPLACEMENTS[index] + final[replace_index+1:]
#             if final != sl_domain:  # in the off chance the outcome is the same
#                 similar.append(final)
#     return similar

def b4_after_tld(tld, b4_chars, after_chars, max_mods):
    '''Takes as input a template for what comes before and after the tld'''

    b4_and_after = [] #Intermediate storage
    urls_out = [] #Function Output

    b4_len = len(b4_chars) #extract lengths
    after_len = len(after_chars)

    to_manipulate = b4_chars+after_chars #Concatenate the chars before and after the tld

    def recursive_gen(string, num_to_change, index=0): #Define recurisve func
        out = []
        if index > (len(string)-1): #return empty string if we hit end of input
            return ['']

        elif num_to_change == 0: #Return remainder of string if number left to change is zero
            return [string[index:]]

        elif num_to_change > 0: # either swap whats at this index or dont
            for r in REPLACEMENTS: #swap
                if r != string[index]:
                    for s in recursive_gen(string=string, index=index+1, num_to_change=num_to_change-1):
                        out.append(r + s)

        for s in recursive_gen(string=string, index=index+1, num_to_change=num_to_change): #dont swap
            out.append(string[index]+s)

        return out

    # args = [(to_manipulate, i) for i in list(range(1, max_mods))]
    # workers = 5
    # with ProcessPoolExecutor(workers) as ex:
    #     res = ex.map(recursive_gen, args)
    # res = list(res)

    for i in range(max_mods): #try changing just one mod, then 2, then 3...
        b4_and_after += recursive_gen(to_manipulate, i)

    b4_and_after = set(b4_and_after) #convert to set to eliminate duplicates

    # can only have dots before the tld and only have spaces after if they work their way back from the end
    for each in b4_and_after:
        if each[0] == '.' or each[0]== ' ' or each[0]=='-':
            continue
        else:
            for i in range(1, len(each)+1): # not really sure why this doesnt give index out of range error
                if each[-1] == '-':
                    break
                if '.' in each[i:]:
                    break
                if ' ' in each[:i] and each[-1] != ' ':
                    break # this does not account for spaces that show up when the last char is also a space
                if ' ' in each[i:]:
                    break
                urls_out.append(each[:i]+tld+each[i:]) #add to output if its valid
    return urls_out




def similar_url_brute_force(url,n, max_mods=1):
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
    LEN_URL = len(url)

    if 'http' not in url: #Standardize formating for parsing
        url = "http://" + url

    protocol, domains, path = parse_url(url) #Parse

    url_no_protocol = url.split('://')[1]
    top_level_domain = domains[-1]

    packaged_tld = '.' + top_level_domain + "/"
    split_url = url_no_protocol.split(packaged_tld)

    if len(split_url) == 2: #Get characters before and after the TLD
        b4_tld, after_tld = split_url
    elif len(split_url) == 1:
        b4_tld, after_tld = split_url[0], ''

    for curr_tld in TL_DOMAINS: # We might want to maintain string length such that lengthening tld shortens rest
        packaged_curr_tld = '.' + curr_tld + "/"
        similar += b4_after_tld(packaged_curr_tld, b4_tld, after_tld, max_mods)
    return similar


# url = "https://www.geeksforgeeks.org/python-generate-random-string-of-given-length/"
# print(is_valid_url(url))


# m = 'youtube'
# mes = similar_sl_domains_random(m, 10, 2)
# m = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
# mes = generate_similar_urls(m, 100)
# print(len(mes))
# print(mes)
m = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
m='yahoo.com'
m='http://yahoo.com'
m='http://news.yahoo.com'
m='http://news.yahoo.gg/hello'
n=2
#print(similar_url_brute_force(m,n, max_mods=2))
# o = b4_after_tld(".com/", "yahoo", "news", 2)
# print(o)
