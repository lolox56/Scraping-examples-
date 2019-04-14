import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.bookdepository.com'
r = requests.get(url)
soup = BeautifulSoup(r.content,'html.parser')

data = {"bookTitles": [],
        "bookAuthor": [],
        "pubDates": []}

btTags = soup.select('.title a')
bookTitles = []
for btTag in btTags:
    bookTitles.append(btTag.text.strip())

baTagsSpan = soup.select('.author span a > span')
#print(baTagsSpan)
#baTags = baTagsSpan.select('a > span')
bookAuthors = []
for baTag in baTagsSpan:
    bookAuthors.append(baTag.text.strip())

pdTags = soup.select('.published')
pubDates = []
for pdTag in pdTags:
    pubDates.append(pdTag.text.strip('\n'))



"""
#print(bookTitles)
#print(bookAuthors)
#print(pubDates)
"""


data['bookTitles'].extend(bookTitles)
data['bookAuthor'].extend(bookAuthors)
data['pubDates'].extend(pubDates)


data['bookAuthor'].append('N/A')
#print(len(bookTitles), len(bookAuthors), len(pubDates), len(baTagsSpan))
df = pd.DataFrame(data=data)

print(df.head())

"""
# Code that does the same::

url = ""

f = open('books.txt,'w')

r = requests.get(url)
data_list = []
new_item = []
soup = BeautifulSoup(r.content,'html.parser')

for item in soup.findAll('', {'itemprop':'name'}):
    new_item.append(item.get('content'))
data_list.append(new_item)

new_item = []
for item in soup.findAll('', {'itemprop':'contributor'}):
    new_item.append(item.get('content'))
data_list.append(new_item)

new_item = []
for item in soup.findAll('', {'class':'published'}):
    new_item.append(str(item)[-15:-4])
data_list.append(new_item)

f.write('{0:60} {1:25} {2:10}\n\n.format("Book name", "Author",
"Publication Date"))
for i in range(len(data_list[0])):
    f.write('{0:60} {1:25} {2:10}\n\n.format(data_list[0][i], data_list[1][i],
data_list[2][i]))
f.close
"""
