#!/usr/bin/env python3

"""
Download tagged photos from Facebook
700213996
"""

import sys
from os import path
import re
import urllib.parse as urlparse
import urllib.request as request
from datetime import datetime
import piexif
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expect
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By

try:
    fb_id = sys.argv[1]
    if re.match(r'^\d+$', fb_id) is None:
        raise ValueError
except (IndexError, ValueError):
    print('Please supply a numeric Facebook ID as the first argument.')
    print('Find your ID here: https://findmyfbid.in.')
    print('Please note: Facebook is constanly evading ID finding tools.')
    sys.exit(1)

try:
    output_dir = sys.argv[2]
    if not path.isdir(output_dir):
        raise ValueError
    output_dir = path.abspath(output_dir)
    print('Image files will be saved in \'{}\'.'.format(output_dir))
except IndexError:
    output_dir = path.dirname(path.realpath(__file__))
    print('No output directory specified.')
    print('Image files will be saved in \'{}\'.'.format(output_dir))
except ValueError:
    print('Output directory must be directory.')
    sys.exit(1)

def filtered_unique(array):
    """
    Removes duplicates and None from list
    """
    return list(set([x for x in array]))

def create_driver():
    """
    Creates Chrome driver
    Disables notifications
    """
    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_setting_values.notifications': 2}
    options.add_experimental_option('prefs', prefs)
    drv = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=options)
    drv.implicitly_wait(10)
    return drv

def teardown(drv, message):
    """
    Print exit message, close driver
    """
    print(message)
    input('Press Enter to close browser window.')
    try:
        drv.close()
    except: # pylint: disable=W0702
        pass
    sys.exit()

def scroll_to_end(drv):
    """
    Scrolls to the bottom of the page, triggering more images to load
    Waits until end of results is reached
    """
    def scrolled_to_bottom(drv):
        """
        Scroll to the bottom and check for the end or results flag
        """
        try:
            drv.implicitly_wait(0)
            drv.find_element(By.XPATH, '//div[text() = "End of Results"]')
            drv.implicitly_wait(10)
        except NoSuchElementException:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            return False
        return True

    WebDriverWait(drv, 3600, poll_frequency=0.25).until(scrolled_to_bottom)

def extract_asset_ids(drv):
    """
    Finds all asset ids within links
    """
    def extract_id_param(anchor):
        """
        Extract Facebook asset ID from anchor element
        """
        parsed = urlparse.urlparse(anchor.get_attribute('href'))
        try:
            return urlparse.parse_qs(parsed.query)['fbid'][0]
        except (AttributeError, IndexError):
            return None

    elements = drv.find_elements(By.XPATH, '//a[contains(@href, "?fbid=")]')
    return filtered_unique(map(extract_id_param, elements))

def extract_timestamp(drv):
    """
    Get image timestamp from element
    """
    timestamp_xpath = '//div[@data-testid="story-subtitle"]//abbr'
    abbr = drv.find_element(By.XPATH, timestamp_xpath)
    """
    try:
        abbr = drv.find_element(By.XPATH, timestamp_xpath)
    except NoSuchElementException:
        return None
    """
    return int(abbr.get_attribute('data-utime'))

def extract_image_url(drv):
    """
    Get image URL from element
    """
    try:
        img = drv.find_element(By.XPATH, '//img')
    except NoSuchElementException:
        return None
    return img.get_attribute('src')

def download_image(url, out_dir, filename, timestamp):
    """
    Save image to disk
    """
    response = request.urlopen(url)
    img = Image.open(BytesIO(response.read()))
    datetime_format = '%Y-%m-%d %H:%M:%S'

    date_time_original = datetime.utcfromtimestamp(timestamp).strftime(datetime_format)
    exif_dict = {
        '0th': {
            piexif.ImageIFD.DateTime: date_time_original
        },
        'Exif': {
            piexif.ExifIFD.DateTimeOriginal: date_time_original
        }
    }
    exif_bytes = piexif.dump(exif_dict)
    filepath = path.join(out_dir, filename)
    img.save(filepath, 'jpeg', exif=exif_bytes)


def print_progress(complete, total):
    """
    Print progress to same line
    """
    padded = str(complete).zfill(len(str(total)))
    print('\r{}/{} ({:.1f}%)'.format(padded, total, 100*complete/total), end='')

try:
    driver = create_driver()
    driver.get('https://facebook.com')
except (KeyboardInterrupt, TimeoutException):
    teardown(driver, 'Quitting before user logged into Facebook.')

try:
    print('Please login to Facebook. Your credentials are not logged.')
    WebDriverWait(driver, 360).until_not(expect.title_contains('log in'))
except (KeyboardInterrupt, TimeoutException):
    teardown(driver, 'Please log into Facebook within six minutes.')

try:
    driver.get('https://www.facebook.com/search/{}/photos-of/intersect'.format(fb_id))

    print('Loading all tagged photos. This can take some time.')
    scroll_to_end(driver)
    print('Extracting asset IDs')
    asset_ids = extract_asset_ids(driver)
    print('Found {} unique photos.'.format(len(asset_ids)))

    for index, asset_id in enumerate(asset_ids):
        # extract timestamp
        driver.get('https://www.facebook.com/photo.php?fbid={}'.format(asset_id))
        image_timestamp = extract_timestamp(driver)
        driver.get('https://m.facebook.com/photo/view_full_size/?fbid={}'.format(asset_id))
        image_url = extract_image_url(driver)
        download_image(image_url, output_dir, 'fb_{}.jpg'.format(index), image_timestamp)
        print_progress(index+1, len(asset_ids))
    print()
except (KeyboardInterrupt, TimeoutException):
    teardown(driver, 'Quitting due to keyboard interrupt or timeout.')

teardown(driver, 'Done!')
