import sys
from os import path
import time #
import re
import urllib.parse as urlparse
import urllib.request as request
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expect
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By

def teardown(drv, message):
    #
    #Print exit message, close driver
    #
    print(message)
    input('Press Enter to close browser window.')
    try:
        drv.close()
    except: # pylint: disable=W0702
        pass
    sys.exit()

def create_driver():
    #
    #Creates Chrome driver
    #Disables notifications
    #
    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_setting_values.notifications': 2}
    options.add_experimental_option('prefs', prefs)
    drv = webdriver.Chrome('/chromedriver/chromedriver.exe', chrome_options=options)
    drv.implicitly_wait(10)
    return drv

def scroll_to_end(drv):
    #
    #Scrolls to the bottom of the page, triggering more images to load
    #Waits until end of results is reached
    #
    def scrolled_to_bottom(drv):
        #
        #Scroll to the bottom and check for the end or results flag
        #
        try:
            drv.implicitly_wait(0)
            drv.find_element(By.XPATH, '//div[text() = "End of Results"]')
            drv.implicitly_wait(10)
        except NoSuchElementException:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            return False
        return True

    WebDriverWait(drv, 3600, poll_frequency=0.25).until(scrolled_to_bottom)

try:
    driver = create_driver()
    driver.get('https://the100meterscroll.com/')
except (KeyboardInterrupt, TimeoutException):
    teardown(driver, 'Quitting before user logged into Facebook.')

try:
    print('Run!')
    scroll_to_end(driver)
    
except (KeyboardInterrupt, TimeoutException):
    teardown(driver, 'Quitting due to keyboard interrupt or timeout.')

teardown(driver, 'Done!')