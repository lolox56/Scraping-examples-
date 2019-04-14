import requests
from bs4 import BeautifulSoup
import pandas

url = 'http://www.iata.org/publications/Pages/code-search.aspx'
# This url is powered by asp.net so we make our scraping approach more robust
# First we perform a GET request to obtain the important session information and form data.


def get_results(airline_name):
    session = requests.Session()
    # Spoof the user agent as a precaution and indicate that a partial result is wanted
    session.headers.update({'X-MicrosoftAjax': 'Delta=true',
                            'X-Requested-With': 'XMLHttpRequest',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' +
                                          ' (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'})
    # Get the search page
    r = session.get(url)
    html_soup = BeautifulSoup(r.text, 'html.parser')
    form =html_soup.find(id='aspnetForm')

    # Get the form fields
    data = {}
    for inp in form.findAll(['input', 'select']):
        name = inp.get('name')
        value = inp.get('value')
        if not name:
            continue
        # Set your desired search query first:
        # Search by
        if 'ddlImLookingFor' in name:
            value = 'ByAirlineName'
        # Airline name
        if 'txtSearchCriteria:' in name:
            value = airline_name
        data[name] = value if value else ''

    # Now used the collected form data to perform a POST request.
    # Perform a POST
    r = session.post(url, data=data)
    html_soup = BeautifulSoup(r.text, 'html.parser')
    table = html_soup.find('table', class_='datatable')
    df = pandas.read_html(str(table))
    return df


df = get_results('Lufthansa')
print(df)

# NOTE: this returns an error because the html response returned from the POST contains javaScript code that generated
# the main data containing the datatable class. So you obtain no data.  Thus, Selenium is needed here.


#print(data, end='\n\n\n')




