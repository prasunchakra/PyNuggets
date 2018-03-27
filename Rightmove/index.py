from selenium import webdriver
import time, pdb
import xlsxwriter
from bs4 import BeautifulSoup
import requests
from lxml import html
from selenium.webdriver.firefox.options import Options


def make_request(url):
    print ("Requesting Page :",url)
    r = requests.get(url)
    return r.content, r.status_code


def get_page(request_content):
    tree = html.fromstring(request_content)
    xp_prices = """//div[@class="propertyCard-priceValue"]/text()"""
    xp_titles = """//div[@class="propertyCard-details"]\
    //a[@class="propertyCard-link"]\
    //h2[@class="propertyCard-title"]/text()"""
    xp_addresses = """//address[@class="propertyCard-address"]//span/text()"""
    xp_weblinks = """//div[@class="propertyCard-details"]\
    //a[@class="propertyCard-link"]/@href"""
    price_pcm = tree.xpath(xp_prices)
    titles = tree.xpath(xp_titles)
    addresses = tree.xpath(xp_addresses)
    base = "http://www.rightmove.co.uk"
    weblinks = ["{}{}".format(base, tree.xpath(xp_weblinks)[w]) for w in range(len(tree.xpath(xp_weblinks)))]
    data = [titles, addresses, weblinks]
    return weblinks,addresses


def get_old_price(url):
    options = Options()
    options.add_argument("--headless")
    # url = 'http://www.rightmove.co.uk/property-for-sale/property-63878375.html'
    driver = webdriver.Firefox(firefox_options=options)
    driver.get(url)
    time.sleep(10)
    #print("Page Loaded:", url)
    history_tab = driver.find_element_by_xpath('//*[@id="historyMarketTab"]/a')
    driver.execute_script("arguments[0].click()", history_tab)
    #print("Item clicked")
    time.sleep(10)
    history = driver.find_element_by_xpath('//*[@id="soldHistoryBody"]')
    #print("History Found")
    html = history.get_attribute('outerHTML')
    soup = BeautifulSoup(html, 'html.parser')
    try:
        Old_Price = soup.find_all('td')[1].text.strip()
    except:
        Old_Price = None
    finally:
        driver.close()
    return Old_Price

if __name__ == '__main__':
    #first_page = 'http://www.rightmove.co.uk/property-for-sale/find.html?searchType=SALE&locationIdentifier=REGION%5E61326&insId=1&radius=0.0&minPrice=&maxPrice=&minBedrooms=&maxBedrooms=&displayPropertyType=&maxDaysSinceAdded=1&_includeSSTC=on&sortByPriceDescending=&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&newHome=&auction=false'
    first_page = 'http://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E219&maxPrice=250000&maxDaysSinceAdded=1&includeSSTC=false'
    n = 42
    m = 0
    page_links = [first_page]
    for p in range(1, n + 1, 1):
        p_url = "{}&index={}".format(str(first_page), str((p * 24)))
        page_links.append(p_url)
        m = m + 1
    for links in page_links:
        content, status = make_request(links)
        if status!=200:
            print("All links traversed ")
            break
        page,property = get_page(content)
        for plinks, paddrs in zip(page, property):
            oldprice = get_old_price(plinks)
            m = m+1
            if oldprice:
                print("Price Drop :", plinks,paddrs)
            else:
                print("No Price Drop :",plinks,paddrs)
    print("Total Links Traversed:",m)

                #print(plinks, paddrs)


