from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import urllib.request as ur
from http.cookiejar import CookieJar
from bs4 import BeautifulSoup
import pdb
base_url = 'https://www.mouseprice.com/house-prices/helme+lane,+meltham'
page = 1
url = base_url
while(1):
    print(url)
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(executable_path="geckodriver.exe",firefox_options=options)
    driver.get(url)
    html = driver.page_source
    driver.close()
    soup = BeautifulSoup(html, "lxml")
    for all_elems in soup.find_all(id='LVSearch'):
        print (all_elems.find('a').contents[0])
        print (all_elems.find('span',{'class':"lv_date_basic_nl"}).contents[0])
        print (all_elems.find('span', {'class': "lv_price"}).contents[0])
    page = page +1
    url = base_url +'/{}'.format(page)
