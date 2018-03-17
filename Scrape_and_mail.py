# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 00:33:54 2018

@author: lordprasun
"""

import urllib.request as ur
from bs4 import BeautifulSoup
import config,re
from email.mime.text import MIMEText
import smtplib,time

def sendmail(messages):
    msg = MIMEText(messages)
    msg['To'] = "wanderer"
    msg['From'] ="wanderer"
    msg['Subject'] = "Web Scrap Report"
    server = smtplib.SMTP(config.Mail_server, config.Port)
    server.starttls()
    server.login(config.From_Mail,config.Password)
    server.sendmail(config.From_Mail, config.To_Mail, msg.as_string())
    server.quit()
    
def findurl(web_content):
    link_address = []
    for keys in config.Keywords:
        for link in web_content.findAll('a', href=True, text=re.compile(keys)):
            link_address.append(link['href'])            
    return set(link_address) 

if __name__=="__main__":    
    
    while(1):
        mail_Text=""
        for urls in config.Url:
            mail_Text= mail_Text+"\n\nInput URL:" + urls
            mail_Text=mail_Text +"\n\tScrapped Url:"
            web_content =BeautifulSoup(ur.urlopen(urls),"lxml")
            updated_links=findurl(web_content)
            for link in updated_links:
                mail_Text=mail_Text +"\n\t"
                mail_Text=mail_Text+link
        print (mail_Text)
        sendmail(mail_Text)
        time.sleep(60)        