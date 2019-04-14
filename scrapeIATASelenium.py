import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select

url = 'http://www.iata.org/publications/Pages/code-search.aspx'

driver = webdriver.Chrome(executable_path=r'C:\Users\ASUS\Downloads\chromedriver.exe')
driver.implicitly_wait(10)


def get_results(airline_name):
    driver.get(url)
    # Make sure to select the right part of the form
    # This'll make finding elements easier as #aspnetForm wraps the whole page including
    # the search box
    form_div = driver.find_element_by_css_selector('.iataStandardForm')
    select = Select(form_div.find_element_by_css_selector('select'))
    select.select_by_value('ByAirlineName')  # selects ByAirlineName from the drop-down box.
    text = form_div.find_element_by_css_selector('input[type=text]')
    text.send_keys(airline_name)
    submit = form_div.find_element_by_css_selector('input[type=submit]')
    submit.click()
    table = driver.find_element_by_css_selector('table.datatable')
    table_html = table.get_attribute('outerHTML')
    df = pd.read_html(str(table_html))
    return df


df = get_results('Lufthansa')
print(df)

driver.quit()