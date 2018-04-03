import selenium
#from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

EXECUTABLE_PATH = "geckodriver.exe"
USER_NAME = "trzenje@housing.si"
PASSWORD = "housingkabi2017"


#firefox_driver = 'geckodriver.exe'
def login2sprout(driver):
    driver.find_element_by_id("user_session_email").send_keys(USER_NAME)
    driver.find_element_by_id("user_session_password").send_keys(PASSWORD)
    driver.find_element_by_name("commit").click()
    return driver
def add_new_logins(driver):
    driver.get('https://sproutvideo.com/logins')
    driver.find_element_by_id("import-logins-button").click()
    driver.implicitly_wait(15)
    driver.find_element_by_id("logins").send_keys("anja.zumer@gmail.com:housingtecaji\ncara@duck2.club:housingtecaji")
    driver.find_element_by_name("commit").click()
def grant_access(driver):
    driver.get('https://sproutvideo.com/videos')
    driver.find_element_by_id("video_selection_all").is_selected()
'''
time.sleep(15)
    browser.switch_to.active_element()
    
    
parent_h = browser.current_window_handle
handles = browser.window_handles # before the pop-up window closes
print "handles",handles
handles.remove(parent_h)
print "handles",handles
browser.switch_to.window(handles.pop())
browser.find_element_by_id("login_email").send_keys("anja.zumer@gmail.com")
browser.find_element_by_id("login_password").send_keys("housingtecaji")
browser.find_element_by_id("login_password_confirmation").send_keys("housingtecaji")
browser.find_element_by_name("commit").click()
browser.switch_to.window(parent_h)
'''
if __name__=="__main__":
    browser = selenium.webdriver.Firefox(executable_path=EXECUTABLE_PATH)
    browser.get('https://sproutvideo.com/login')
    browser=login2sprout(browser)
    #browser=add_new_logins(browser)
    browser = grant_access(browser)