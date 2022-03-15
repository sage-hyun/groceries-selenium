import chromedriver_autoinstaller
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os
from dotenv import load_dotenv

# .env
load_dotenv(verbose=True)
ID = os.getenv('ID')
PW = os.getenv('PW')

chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)

driver.get("https://pay.ssg.com/myssg/orderInfo.ssg?viewType=Ssg")
driver.find_element_by_name('mbrLoginId').send_keys(ID)
driver.find_element_by_name('password').send_keys(PW)
driver.find_element_by_xpath("//button[@id='loginBtn']").click()

