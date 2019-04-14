import requests

url = 'https://www.barclays.co.uk/dss/service/co.uk/mortgages/' + 'costcalculator/productservice'

session = requests.Session()

session.headers.update({
    # These are non-typical headers, we have to include them.
    'currentState': 'default_current_state',
    'action': 'default',
    'Origin': 'https://www.barclays.co.uk',
    # Spoof referer, user agent, and X-Requested-With
    'Referer': 'https://www.barclays.co.uk/mortgages/mortgage-calculator/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' + ' (KHTML, like Gecko) \
    Chrome/62.0.3202.62 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
})

estimatedPropertyValue = 200000
repaymentAmount = 150000
months = 240
data = {'header': {'flowId': '0'},
        'body': {
            'wantTo': 'FTBP',
            'estimatedPropertyValue': estimatedPropertyValue,
            'borrowAmount': repaymentAmount,
            'interestOnlyAmount': 0,
            'repaymentAmount': repaymentAmount,
            'ltv': round(repaymentAmount/estimatedPropertyValue*100),
            'totalTerm': months,
            'purchaseType': 'Repayment'
        }}

r = session.post(url, json=data)

# Only print header to avoid text overload
print(r.json()['header'])