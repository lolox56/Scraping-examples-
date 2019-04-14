import requests
from bs4 import BeautifulSoup

session = requests.Session()

url = 'https://github.com/{}'
username = 'Macuyiko'

# Visit login page
r = session.get(url.format('login'))
html_soup = BeautifulSoup(r.text, 'html.parser')

data = {}

for form in html_soup.findAll('form'):
    # Get ot the hidden form fields
    for inp in form.select('input[type=hidden]'):
        data[inp.get('name')] = inp.get('value')

# Set your Login details:
data.update({'login': '', 'password': ''})

print("Going to login with the following POST data: ")
print(data)

if input('Do you want to login(y/n): ') == 'y':
    # Perform the login
    r = session.post(url.format('session'), data=data)
    # Get the profile page
    r = session.get(url.format(username))
    html_soup = BeautifulSoup(r.text, 'html.parser')
    user_info = html_soup.find(class_='vcard-details')
    print(user_info.text)
