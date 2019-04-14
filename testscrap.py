import requests

"""
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
              "1y Target Est":[]} """

indicators = {"Previous Close":[],
              "Open":[],
              "Bid":[],
              "Ask":[],
              "Day's Range":[],
              "52 Week Range":[],
              "Volume":[],
              "Avg. Volume":[],
              "Market Cap":[],
              "Beta":[],
              "PE Ratio (TTM)":[],
              "EPS (TTM)":[],
              "Earnings Date":[],
              "Dividend & Yield":[],
              "Ex-Dividend Date":[],
              "1y Target Est":[]}

indicatorTag = ["PREV_CLOSE-value",
                "OPEN-value",
                "BID-value",
                "ASK-value",
                "DAYS_RANGE-value",
                "FIFTY_TWO_WK_RANGE-value",
                "TD_VOLUME-value",
                "AVERAGE_VOLUME_3MONTH-value",
                "MARKET_CAP-value",
                "BETA_3Y-value",
                "PE_RATIO-value",
                "EPS_RATIO-value",
                "EARNINGS_DATE-value",
                "DIVIDEND_AND_YIELD-value",
                "EX_DIVIDEND_DATE-value",
                "ONE_YEAR_TARGET_PRICE-value"]

url = "https://finance.yahoo.com/quote/AAPL?p=AAPL"
response = requests.get(url)
#print(response.status_code) #HTTP status codes# ... read up. 200 means all is fine.
htmlText = response.text
counter = 1
spltList = htmlText.split("Trade prices are not sourced from all markets")[0].split("-value")
#print(spltList)
for indicator in indicators:
    #print(indicator)
    dataTag = spltList[counter]
    counter += 1
    #print(spltList)
    #break
    afterFrstSplt = dataTag.split("\">")[1]
    afterScdSplt = afterFrstSplt.split("</td")[0]
    if len(afterScdSplt) > 20:
        afterFrstSplt = dataTag.split("\">")[2]
        afterScdSplt = afterFrstSplt.split("</span")[0]
    #print(afterScdSplt)
    indicators[indicator].append(afterScdSplt)

print(indicators)
