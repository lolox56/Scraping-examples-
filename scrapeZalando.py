import requests
import os, os.path
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

store = 'images'
if not os.path.exists(store):
    os.makedirs(store)

url = 'https://www.zalando.co.uk/womens-clothing-dresses/'
pages_to_crawl = 15


def download(url):
    r = requests.get(url, stream=True)
    # stream= True is recommended for streaming bytes download, especially into a file.
    # urlparse breaks up the url into a tuple with 6 string elements, some of which may be empty:
    # url = scheme://netloc/path;parameters?query#fragment --- (scheme, netloc, path, params, query, fragment)
    # e.g. o = urlparse('http://www.cwi.nl:80/%7Eguido/Python.html') gives:
    # (scheme='http', netloc='www.cwi.nl:80', path='/%7Eguido/Python.html', params='', query='', fragment='')
    # And each value can be accessed by: o.path, o.scheme etc.
    filename = urlparse(url).path.split('/')[-1]
    print('Downloading to: ', filename)
    # The response object (an image) is in bytes and can thus be accessed by r.content (not r.text).
    # But since we are writing to a file in chunks, we iterate over r.content with r.iter_content
    with open(os.path.join(store, filename), 'wb') as the_image:
        for byte_chunk in r.iter_content(chunk_size=4096*4):
            the_image.write(byte_chunk)


# get the img src links and download the images
for p in range(1, pages_to_crawl+1):
    print('Scraping page: ', p)
    r = requests.get(url, params={'p': p})
    html_soup = BeautifulSoup(r.text, 'html.parser')
    for img in html_soup.select('#z-nvg-cognac-root z-grid-item img'):
        img_src = img.get('src')
        if not img_src:
            continue
        img_url = urljoin(url, img_src)
        download(img_url)