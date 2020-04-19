
import argparse, sys, os, time, wget, json, piexif, ssl, urllib
from os import path
import time #
import re
import urllib.parse as urlparse
import urllib.request as request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expect
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By


def start_session(username, password):
    print("Opening Browser...")
    wd_options = Options()
    wd_options.add_argument("--disable-notifications")
    wd_options.add_argument("--disable-infobars")
    wd_options.add_argument("--mute-audio")
    wd_options.add_argument("--start-maximized")
    driver = webdriver.Chrome('/chromedriver/chromedriver.exe', chrome_options=wd_options)

    #Login
    driver.get("https://www.facebook.com/")
    print("Logging In...")
    email_id = driver.find_element_by_id("email")
    pass_id = driver.find_element_by_id("pass")
    email_id.send_keys(username)
    pass_id.send_keys(password)
    driver.find_element_by_id("loginbutton").click()

    return driver
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Facebook Scraper')
    parser.add_argument('-u', type = str,help='FB Username')
    parser.add_argument('-p', type = str,help='FB Password')
    parser.add_argument('--download', action='store_true', help='Download photos only')
#   parser.add_argument('--index', action='store_true', help='Index photos')
    args = parser.parse_args()
    try:
        if args.download:
            print('aqui seria a execução do download_photos')
        else:
            if not (args.u and args.p):
                print('Please try again with FB credentials (use -u -p)')
            else:
                driver = start_session(args.u,args.p)
                print('aqui seria a execução do index_photos')
                if not args.index:
                    print('aqui seria a execução do download_photos')
    except KeyboardInterrupt:
        print('\nThanks for using the script! Please raise any issues at: https://github.com/jcontini/fb-photo-downloader/issues/new')
        pass