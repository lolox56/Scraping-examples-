import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pickle


def get_forum_threads(url, max_pages=None):
    page = 1
    threads = []
    while not max_pages or page <= max_pages:
        print('Scraping forum page: ', page)
        r = requests.get(url, params={'page': page})
        soup = BeautifulSoup(r.text, 'html.parser')
        content = soup.find(class_='content')
        links = content.findAll('a', attrs={'href': re.compile('^\/thread\/')})
        threads_on_page = [a.get('href') for a in links if a.get('href') and 'page=' not in a.get('href')]
        # you want the main thread links not the paginated thread links.
        threads += threads_on_page
        page += 1
        # Below is a clever way to check if the max_pages is greater than the max no of pages on this website.
        # Even if you enter higher pages number, you get redirected to the same last page. So check if the next link
        # in the pagination area is state-disabled - which indicates that it is the last page.
        next_page = soup.find('li', class_='next')
        if 'state-disabled' in next_page.get('class'):
            break
    return threads


def get_thread_posts(url, max_pages=None):
    page = 1
    posts = []
    while not max_pages or page <= max_pages:
        print('Scraping thread url/page: ', url, page)
        r = requests.get(url, params={'page': page})
        soup = BeautifulSoup(r.text, 'html.parser')
        content = soup.find(class_= 'content')
        for post in content.findAll('tr', class_='item'):
            user = post.find('a', class_= 'user-link')
            if not user:
                # User might be deleted, skip...
                continue
            user = user.get_text(strip=True)
            quotes = []
            for quote in post.findAll(class_='quote_header'):
                quoted_user = quote.find('a', class_='user-link')
                if quoted_user:
                    quotes.append(quoted_user.get_text(strip=True))
            posts.append((user, quotes))
        page += 1
        next_page = soup.find('li', class_='next')
        if 'state-disabled' in next_page.get('class'):
            break
    return posts


url = 'http://bpbasecamp.freeforums.net/board/27/gear-closet'

threads = get_forum_threads(url, max_pages=5)
all_posts = []

for thread in threads:
    thread_url = urljoin(url, thread)
    posts = get_thread_posts(thread_url)
    all_posts.append(posts)

with open('forum_posts.pkl', 'wb') as output_file:
    pickle.dump(all_posts, output_file)



#
print(posts)

