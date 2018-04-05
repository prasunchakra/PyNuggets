# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 06:37:55 2018

@author: lordprasun
"""

from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
import time
url = 'http://www.football-lineups.com/tourn/FA_Premier_League_2016-2017/Stats/Players_Used/'
options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(executable_path="geckodriver.exe",firefox_options=options)
driver.get(url)
teams = driver.find_element_by_xpath('//*[@id="mainarea"]/tbody/tr/td[1]/table[2]')
html = teams.get_attribute('outerHTML')
soup = BeautifulSoup(html, 'html.parser')
baseurl = 'http://www.football-lineups.com/'
for tlinks in soup.findAll('a', href=True):
    print(tlinks['href'])
    turl = baseurl + tlinks['href']
    driver.get(turl)
    time.sleep(5)
    players = driver.find_element_by_xpath('//*[@id="mainarea"]/tbody/tr/td[1]/table[2]')
    html = players.get_attribute('outerHTML')
    soup = BeautifulSoup(html, 'html.parser')
    for plinks in soup.findAll('a', href=True):
        if plinks['href'].startswith('/foot'):
            print('\t',plinks['href'])
            purl = baseurl + plinks['href']
            driver.get(purl)
            time.sleep(5)
            players = driver.find_element_by_xpath('//*[@id="sppg"]/table[2]')
            html = players.get_attribute('outerHTML')
            soup = BeautifulSoup(html, 'html.parser')
            for dlinks in soup.findAll('a', href=True):
                print('\t\t', dlinks['href'])
driver.quit()
