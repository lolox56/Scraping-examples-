import requests

articles = []

# Uses the HackerNews API to obtain data instead of writing a script to scrape manually from the ycombinator webpage.
# If there's an API, always use it!

url = 'https://hacker-news.firebaseio.com/v0'

# obtains top 50 item id's for the topstories on ycombinator hacker-news and .json() decodes the returned
# json content into a list of item id's in this case.
top_stories = requests.get(url + '/topstories.json').json()

for story_id in top_stories:
    story_url = url + '/item/{}.json'.format(story_id)  # makes url for obtaining data for each item id
    print('Fetching: ', story_url)
    r = requests.get(story_url)  # obtains the data in json format as suggested by the .json in story_url
    story_dict = r.json()  # decodes the json. json array into python list, json structs into python dicts and so on.
    articles.append(story_dict)  # appends the returned dict to the article list.

for article in articles:
    print(article)