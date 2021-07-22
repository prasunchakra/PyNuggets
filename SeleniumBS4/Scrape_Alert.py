# -*- coding: utf-8 -*-
"""
@author: prasunchakra
"""

import urllib.request as ur
from bs4 import BeautifulSoup
import config,re
import ctypes,time
import winsound

def sendalert(messages):
    duration = 1000
    freq = 440
    winsound.Beep(freq, duration)
    ctypes.windll.user32.MessageBoxW(0, messages, "Web Scrap Report", 1)
    

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
            print (urls)
            web = ur.urlopen(urls)
            time.sleep(15)
            content = web.read()
            web_content =BeautifulSoup(content,"lxml")
            updated_links=findurl(web_content)
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