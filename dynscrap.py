# Note that webdrivers are in general slower than Requests. That's why you use webdrivers only for dynamic websites.

from selenium import webdriver
import json
import pandas as pd
# import os

url = "https://finance.yahoo.com/quote/AAPL/key-statistics?p=AAPL"

# y=os.environ['phanthomPATH']  # added to environmental variables and can be assessed like this
# print(y) #Output (w/out quotes) -- 'C://Users//ASUS//Desktop//phantomjs-2.1.1-windows//bin//phantomjs.exe'

# creates a webdriver element, a headless browser in this case.
browser = webdriver.PhantomJS(executable_path='C://Users//ASUS//Desktop//phantomjs-2.1.1-windows//bin//phantomjs.exe')

browser.get(url)  # browser accesses given URL.

# print(browser.page_source) -- prints out all html+css+scripting source code from website.

# Quick XML Path (XPATH) TUTORIAL
# ----------------------------------------------------------------------------------------------------------------------
"""
#element = browser.find_element_by_xpath("html") -- returns a web-element object, an html node in this case.
elements = browser.find_elements_by_xpath("html/*") #returns list of web-element objects, all child nodes of html node - head and body.

for element in elements:
    print(element.tag_name + "\n")  # self-explanatory - prints head and body
    newElements = element.find_elements_by_xpath("./*") #goes deeper - obtains all child nodes of head and body
    for newElement in newElements:
        print(newElement.tag_name) # prints all tags under head and body each
    print("\n")
"""
# ----------------------------------------------------------------------------------------------------------------------

# print(element.text) # note that this doesn't print out ALL text
# print(element.get_attribute("textContent"))
# ------------------------------------------------------------------------------------------------------------------
# Recursive Function to obtain the xpath of our targets:
# def findXPath(element,target,path):
#     if target in element.get_attribute("textContent") and element.tag_name == "script":
#         return path  # path is an element tag name.
#     newElements = element.find_elements_by_xpath("./*")  # if target not in current tag, go deeper
#     for newElement in newElements:
#         print(path + "/" + newElement.tag_name)
#         final = findXPath(newElement,target, path + "/" + newElement.tag_name)  # path slightly changed
#         if final != "":
#             return final
#     return ""


# starting element and thus, path:
# element = browser.find_element_by_xpath("html")
# print("The final path is: ", findXPath(element,"trailingPE",element.tag_name)) result : html/body/script
# -------------------------------------------------------------------------------------------------------------------
# Similar recursive function to obtain the json path of our target:

def findJsonPath(jsonObject, target, path, matchType):
    if type(jsonObject) == matchType:
        if target in jsonObject:  # to ensure we are still in json/dict structure
            return path
        for newKey in jsonObject:
            print(path)
            final = findJsonPath(jsonObject[newKey],target,path + "/" + newKey,matchType)
            if final != "":
                return final
    return ""

# ---------------------------------------------------------------------------------------------------------------------


# To determine which script tag our target lies in: It is important to note that html indexing starts from 1, not 0.
elements = browser.find_elements_by_xpath("html/body/script")
counter = 1
for element in elements:
    if "trailingPE" in element.get_attribute("textContent"):
        print(counter)
        # break
    counter += 1
# Result is that target resides only in first script, so exact element script in elements: html/body/script[1]
# --------------------------------------------------------------------------------------------------------------------

element = browser.find_element_by_xpath("html/body/script[1]")
tempData = element.get_attribute("textContent").strip("(this));\n")  # removing this part so it looks like a json/dict.
tempData = tempData.split("root.App.main = ")[1][:-3]  # getting rid of last few stuff to make the string format tidy.
jsonData = json.loads(tempData)  # converts from string format to json/dict format
# print(jsonData.keys())
matchType = type(jsonData)
# print("The final path is: ", findJsonPath(jsonData,"trailingPE","",matchType))  # result: /context/dispatcher/stores/QuoteSummaryStore/summaryDetail

finalData = jsonData["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["summaryDetail"] # contains all the targets we want.
df = pd.DataFrame(data=finalData)
print(df)
browser.quit()

