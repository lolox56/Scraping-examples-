import requests
from bs4 import BeautifulSoup


url = 'http://www.iata.org/publications/Pages/code-search.aspx'
# This url is powered by asp.net so we make our scraping approach more robust
# First we perform a GET request to obtain the important session information and form data.

session = requests.Session()
# Spoof the user agent as a precaution
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' +
                                      ' (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'})

# Get the search page
r = session.get(url)
html_soup = BeautifulSoup(r.text, 'html.parser')
form = html_soup.find(id='aspnetForm')

# Get the form fields
data = {}
for inp in form.findAll(['input', 'select']):
    name = inp.get('name')
    value = inp.get('value')
    if not name:
        continue
    data[name] = value if value else ''

print(data, end='\n\n\n')


# Set your desired search query first:
# Here we used the collected form data to perform a POST request.
for name in data.keys():
    # Search by
    if 'ddlImLookingFor' in name:
        data[name] = 'ByAirlineName'
    # Airline name
    if 'txtSearchCriteria:' in name:
        data[name] = 'Lufthansa'
        
# Perform a POST
r = session.post(url, data=data)
print(r.text)












