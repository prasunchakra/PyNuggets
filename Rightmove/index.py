from selenium import webdriver
import time,sys,configparser
from bs4 import BeautifulSoup
import requests,xlsxwriter
from lxml import html
from selenium.webdriver.firefox.options import Options
configfile = ''
def make_request(url):
    r = requests.get(url)
    return r.content, r.status_code

def get_firstpage(url,parameters):
    #url = 'http://www.rightmove.co.uk/property-for-sale.html'
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=options)
    driver.get(url)
    driver.find_element_by_xpath('//*[@id="searchLocation"]').send_keys(parameters['Location'])
    driver.find_element_by_xpath('//*[@id="search"]').click()
    url = driver.current_url
    driver.get(url)
    xpath = '//*[@id="radius"]/option[text()="{}"]'.format(parameters['Radius'])
    driver.find_element_by_xpath(xpath).click()
    xpath = '//*[@id="displayPropertyType"]/option[text()="{}"]'.format(parameters['Property_Type'])
    driver.find_element_by_xpath(xpath).click()
    xpath = '//*[@id="maxDaysSinceAdded"]/option[text()="{}"]'.format(parameters['Days_Added'])
    driver.find_element_by_xpath(xpath).click()
    time.sleep(14)
    driver.find_element_by_xpath('//*[@id="submit"]').click()
    url = driver.current_url
    driver.quit()
    return url
def get_page(request_content):
    tree = html.fromstring(request_content)
    xp_prices = """//div[@class="propertyCard-priceValue"]/text()"""
    xp_addresses = """//address[@class="propertyCard-address"]//span/text()"""
    xp_weblinks = """//div[@class="propertyCard-details"]\
    //a[@class="propertyCard-link"]/@href"""
    prices = tree.xpath(xp_prices)
    addresses = tree.xpath(xp_addresses)
    base = "http://www.rightmove.co.uk"
    weblinks = ["{}{}".format(base, tree.xpath(xp_weblinks)[w]) for w in range(len(tree.xpath(xp_weblinks)))]
    data = [addresses, weblinks]
    return weblinks,addresses,prices


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
        driver.quit()
    return Old_Price


def get_config():
    global configfile
    parameters = {}
    radius = {"0.0": "This area only",
              "0.25": "Within ¼ mile",
              "0.5": "Within ½ mile",
              "1.0": "Within 1 mile",
              "3.0": "Within 3 miles",
              "5.0": "Within 5 miles",
              "10.0": "Within 10 miles",
              "15.0": "Within 15 miles",
              "20.0": "Within 20 miles",
              "30.0": "Within 30 miles",
              "40.0": "Within 40 miles"}
    daysadded = {"Anytime": "Anytime",
                 "1": "Last 24 hours",
                 "3": "Last 3 days",
                 "7": "Last 7 days",
                 "14": "Last 14 days"
                 }
    propertype = {"Any": "Any",
                  "houses": "Houses",
                  "flats": "Flats / Apartments",
                  "bungalows": "Bungalows",
                  "land": "Land",
                  "commercial": "Commercial Property",
                  "other": "Other"
                  }
    config = configparser.ConfigParser()
    configfile=sys.argv[1]
    config.read(configfile)
    parameters.update({'Location': config['RM']['Location']})
    parameters.update({'Radius': radius.get(config['RM']['Radius_in_miles'], "This area only")})
    parameters.update({'Days_Added': daysadded.get(config['RM']['DaysAdded'], "Last 24 hours")})
    parameters.update({'Property_Type': propertype.get(config['RM']['Property_Type'].lower(), "Any")})

    return parameters

if __name__ == '__main__':
    #first_page = 'http://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E219&maxPrice=250000&maxDaysSinceAdded=1&includeSSTC=false'
    URL = 'http://www.rightmove.co.uk/property-for-sale.html'
    parameters = get_config()
    first_page = get_firstpage(URL,parameters)
    n = 42
    m = 0
    page_links = [first_page]
    filename = 'Rightmove_{}.xlsx'.format(parameters['Location'])
    #sheetname = parameters['Property_Type'] +','+ parameters['Days_Added'] +','+ parameters['Radius']
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet('Sheet 0')
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
        page,property,price = get_page(content)
        for plinks, paddrs, ppricce in zip(page, property,price):
            oldprice = get_old_price(plinks)
            if oldprice:
                oldprice = int(oldprice[1:].replace(',', ''))
                newprice = int(ppricce[1:].replace(',', ''))
                if oldprice > newprice:
                    print("Price Drop :", plinks,paddrs)
                    worksheet.write(row, col, plinks)
                    worksheet.write(row, col + 1, paddrs)
                    row = row + 1
                else:
                    print("Price Rise")
            else:
                print("No Price Drop", plinks,paddrs)
    workbook.close()
    print ('Data Saved in {}'.format(filename))
