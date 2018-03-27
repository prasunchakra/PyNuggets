from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests,xlsxwriter
from lxml import html
from selenium.webdriver.firefox.options import Options


def make_request(url):
    r = requests.get(url)
    return r.content, r.status_code

def get_firstpage(url):
    #url = 'http://www.rightmove.co.uk/property-for-sale.html'
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=options)
    driver.get(url)
    driver.find_element_by_xpath('//*[@id="searchLocation"]').send_keys('Bristol')
    driver.find_element_by_xpath('//*[@id="search"]').click()
    url = driver.current_url
    driver.get(url)
    driver.find_element_by_xpath('//*[@id="radius"]/option[text()="This area only"]').click()
    driver.find_element_by_xpath('//*[@id="displayPropertyType"]/option[text()="Any"]').click()
    driver.find_element_by_xpath('//*[@id="maxDaysSinceAdded"]/option[text()="Anytime"]').click()
    driver.find_element_by_xpath('//*[@id="submit"]').click()
    url = driver.current_url
    return url
def get_page(request_content):
    tree = html.fromstring(request_content)
    xp_addresses = """//address[@class="propertyCard-address"]//span/text()"""
    xp_weblinks = """//div[@class="propertyCard-details"]\
    //a[@class="propertyCard-link"]/@href"""
    addresses = tree.xpath(xp_addresses)
    base = "http://www.rightmove.co.uk"
    weblinks = ["{}{}".format(base, tree.xpath(xp_weblinks)[w]) for w in range(len(tree.xpath(xp_weblinks)))]
    data = [addresses, weblinks]
    return weblinks,addresses


def get_old_price(url):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=options)
    driver.get(url)
    time.sleep(10)
    history_tab = driver.find_element_by_xpath('//*[@id="historyMarketTab"]/a')
    driver.execute_script("arguments[0].click()", history_tab)
    time.sleep(10)
    history = driver.find_element_by_xpath('//*[@id="soldHistoryBody"]')
    html = history.get_attribute('outerHTML')
    soup = BeautifulSoup(html, 'html.parser')
    try:
        Old_Price = soup.find_all('td')[1].text.strip()
    except:
        Old_Price = None
    finally:
        driver.close()
    return Old_Price
def read_config():
    pass




if __name__ == '__main__':
    #first_page = 'http://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E219&maxPrice=250000&maxDaysSinceAdded=1&includeSSTC=false'
    print("Infortaiion 22222222222222")
    URL = 'http://www.rightmove.co.uk/property-for-sale.html'
    first_page = get_firstpage(URL)
    print (first_page)
    n = 42
    m = 0
    page_links = [first_page]
    workbook = xlsxwriter.Workbook('Rightmove_P.xlsx')
    worksheet = workbook.add_worksheet('Price Drop')
    row = 0
    col = 0
    worksheet.write(row, col, 'Links')
    worksheet.write(row, col + 1, 'Address')
    row = row + 1
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
            if oldprice:
                print("Price Drop :", plinks,paddrs)
                worksheet.write(row, col, plinks)
                worksheet.write(row, col + 1, paddrs)
                row = row + 1
            else:
                print("No Price Drop", plinks,paddrs)
    workbook.close()
    print ('Data Saved in Rightmove_P.xlsx')


                #print(plinks, paddrs)


