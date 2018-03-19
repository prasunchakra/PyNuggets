# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 00:33:54 2018

@author: lordprasun
"""
from bs4 import BeautifulSoup
import config,re
import ctypes,time
import winsound
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def sendalert(messages):
    duration = 1000
    freq = 440
    winsound.Beep(freq, duration)
    ctypes.windll.user32.MessageBoxW(0, messages, "Web Scrap Report", 1)
    
def getpage(url):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=options)
    driver.get('http://tech.sina.com.cn/apple/')
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    return soup
def findurl(web_content):
    link_address = []
    for keys in config.Keywords:
        print(keys)
        for link in web_content.findAll('a', href=True, text=re.compile(keys)):
            print (link.contents)
            link_address.append({link['href']:link.contents})            
    return link_address

if __name__=="__main__":   
    old_links=[]
    while(1):
        new_list=[]
        for urls in config.Url:
            web_content = getpage(urls)
            updated_links = findurl(web_content)
            for link in updated_links:
                new_list.append(list(link.keys())[0])
            
        if old_links != new_list:
            old_links = new_list
            messages=""
            count = 0
            for items in updated_links:
                key = list(items.keys())[0]
                count = count + 1
                messages= messages+ "\n\n{0} {1}".format(count,key)
                messages= messages+ "\nAnchor: "+items[key][0].strip()
            sendalert(messages)
            print ("New Items found Alert Sent")
        else:
            print("\nSame Links: No Alert")
        time.sleep(60)        