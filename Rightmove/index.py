from selenium import webdriver
import time,pdb
import urllib.request as ur
from bs4 import BeautifulSoup
from rightmove_webscraper import _GetDataFromURL
from rightmove_webscraper import rightmove_data
import pandas as pd
import requests
from lxml import html
details=[]
url1 = 'http://www.rightmove.co.uk/property-for-sale/find.html?searchType=SALE&locationIdentifier=REGION%5E61326&insId=1&radius=0.0&minPrice=50000&maxPrice=100000&minBedrooms=&maxBedrooms=&displayPropertyType=&maxDaysSinceAdded=1&_includeSSTC=on&sortByPriceDescending=&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&newHome=&auction=false'
url2 = 'http://www.rightmove.co.uk/property-for-sale/find.html?searchType=SALE&locationIdentifier=REGION%5E61326&insId=1&radius=0.0&minPrice=50000&maxPrice=100000&minBedrooms=&maxBedrooms=&displayPropertyType=&maxDaysSinceAdded=14&_includeSSTC=on&sortByPriceDescending=&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&newHome=&auction=false'

def make_request(url):
    r = requests.get(url)
    return r.content, r.status_code
def page_count():
    tree = html.fromstring(url2)
    xpath = """//span[@class="searchHeader-resultCount"]/text()"""
    results_count =  int(tree.xpath(xpath)[0].replace(",", ""))
    page_count = results_count // 24
    if results_count % 24 > 0: page_count += 1
    if page_count > 42: page_count = 42
    return page_count
def get_page(request_content):
    tree = html.fromstring(request_content)
    xp_titles = """//div[@class="propertyCard-details"]\
    //a[@class="propertyCard-link"]\
    //h2[@class="propertyCard-title"]/text()"""
    xp_addresses = """//address[@class="propertyCard-address"]//span/text()"""
    xp_weblinks = """//div[@class="propertyCard-details"]\
    //a[@class="propertyCard-link"]/@href"""
    titles = tree.xpath(xp_titles)
    addresses = tree.xpath(xp_addresses)
    base = "http://www.rightmove.co.uk"
    weblinks = ["{}{}".format(base, tree.xpath(xp_weblinks)[w]) for w in range(len(tree.xpath(xp_weblinks)))]
    data = [titles, addresses, weblinks]
    return data
'''
url = 'http://www.rightmove.co.uk/property-for-sale.html'
driver = webdriver.Firefox()
driver.get(url)
driver.find_element_by_xpath('//*[@id="searchLocation"]').send_keys('Yorkshire')
xx = driver.find_element_by_xpath('//*[@id="search"]').click()
url = driver.current_url
driver.get(url)
driver.find_element_by_xpath('//*[@id="radius"]/option[text()="Within 1 mile"]').click()
driver.find_element_by_xpath('//*[@id="displayPropertyType"]/option[text()="Flats / Apartments"]').click()
driver.find_element_by_xpath('//*[@id="maxDaysSinceAdded"]/option[text()="Last 14 days"]').click()
driver.find_element_by_xpath('//*[@id="submit"]').click()
url = driver.current_url
'''
#pc = page_count()
for p in range(1, 24 + 1, 1):
    p_url = "{}&index={}".format(str(url1), str((p * 24)))
    print (p_url)
#first_page = make_request(url2)
#results = get_page(first_page[0])


'''
while(1):
    url = driver.current_url
    driver.get(url)
    html = ur.urlopen(url)
    soup = BeautifulSoup(html, "lxml")
    for link in soup.findAll('div', href=True, text=re.compile(keys)):

for ads in driver.find_element_by_xpath('//*[@id="l-searchResults"]'):
    ad = ads.find_element_by_xpath('//*[@id="l-searchResult is-list"]').click()
    url2 =ad.current_url
    print(url2)
driver.close()

url = 'http://www.rightmove.co.uk/property-for-sale/property-63878365.html'
driver = webdriver.Firefox()
driver.get(url)
time.sleep(60)
driver.find_element_by_xpath('//*[@id="historyMarketTab"]').click()
xx = driver.find_element_by_xpath('//*[@id="soldHistoryBody"]/table/tbody/tr[1]')
print (xx.text)
driver.close()
'''