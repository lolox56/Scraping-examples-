import requests

wikiURL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
wikiResponse = requests.get(wikiURL)

data = {"Company":[]}
wikiFirstParse = wikiResponse.text.split("0001555280")[0].split("Component Stocks")[3]
hyperLinkSplitWiki = wikiFirstParse.split("href=")
start = 8

for position in range(len(hyperLinkSplitWiki)):
    if position >= start:
        if "nyse" in hyperLinkSplitWiki[position] and "quote" in hyperLinkSplitWiki[position]:
            val = hyperLinkSplitWiki[position].split('">')[1].split('</a')[0]
            data["Company"].append(val)
        elif "nasdaq" in hyperLinkSplitWiki[position] and "symbol" in hyperLinkSplitWiki[position]:
            val = hyperLinkSplitWiki[position].split('">')[1].split('</a')[0]
            data["Company"].append(val)
print(len(data["Company"]))

indicators = {"Previous Close":[],
              "Open":[],
              "Bid":[],
              "Ask":[],
              "Day&#x27;s Range":[],
              "52 Week Range":[],
              "Volume":[],
              "Avg. Volume":[],
              "Market Cap":[],
              "Beta":[],
              "PE Ratio (TTM)":[],
              "EPS (TTM)":[],
              "Earnings Date":[],
              "Dividend &amp; Yield":[],
              "Ex-Dividend Date":[],
              "1y Target Est":[]}


#url = "https://finance.yahoo.com/quote/AAPL?p=AAPL&.tsrc=fin-srch"
#response = requests.get(url)
#print(response.status_code) #HTTP status codes# ... read up. 200 means all is fine.
for symbol in data["Company"]:
    url = "https://finance.yahoo.com/quote/" + symbol + "?p=" + symbol
    response = requests.get(url)
    htmlText = response.text
    spltList = htmlText.split("Trade prices are not sourced from all markets")[0].split("-value")
    counter = 1
    #print(symbol)
    try:
        for indicator in indicators:
            #print(indicator)
            dataTag = spltList[counter]
            counter += 1
            afterFrstSplt = dataTag.split("\">")[1]
            afterScdSplt = afterFrstSplt.split("</td")[0]
            if len(afterScdSplt) > 25:
                afterFrstSplt = dataTag.split("\">")[2]
                afterScdSplt = afterFrstSplt.split("</span")[0]
            #print(afterScdSplt)
            indicators[indicator].append(afterScdSplt)
    except IndexError:
        indicators[indicator].append("N/A")

print(len(indicators["Previous Close"]))

""" for symbol in data["Company"]:
    url = "https://finance.yahoo.com/quote/" + symbol + "?p=" + symbol
    response = requests.get(url)
    htmlText = response.text
    #print(symbol)
    try:
        for indicator in indicators:
            #print(indicator)
            spltList = htmlText.split(indicator)
            afterFrstSplt = spltList[1].split("\">")[1]
            afterScdSplt = afterFrstSplt.split("</td")[0]
            if len(afterScdSplt) > 25:
                afterFrstSplt = spltList[1].split("\">")[2]
                afterScdSplt = afterFrstSplt.split("</span")[0]
            #print(afterScdSplt)
            indicators[indicator].append(afterScdSplt)
    except IndexError:
        continue
print(len(indicators["Previous Close"]))"""
