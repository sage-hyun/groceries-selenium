import chromedriver_autoinstaller
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from datetime import datetime
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
time.sleep(3)

data = []

page_num = 1
search_start = "2019-01-01"
search_end = "2020-01-01"

while True:
    driver.get(f"https://pay.ssg.com/myssg/orderInfo.ssg?searchType=5&searchCheckBox=&page={page_num}&searchInfloSiteNo=&searchStartDt={search_start}&searchEndDt={search_end}&searchKeyword=")
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    if soup.find("div", {"class":"codr_no"}):
        break   # exceeded max page

    for order in soup.find_all("div", {"class":"codr_odrdeliv"}):
        # get date
        date_str = order.find("span", {"class":"codr_odrdeliv_odrdate"}).text
        date = datetime.strptime(date_str, '%Y.%m.%d')  # datetime object

        # get product names
        for product in order.find_all("span", {"class":"codr_unit_name"}):
            p_name = product.text.strip()

            # check existance ("list comprehension")
            existance = [(idx, elem) for idx, elem in enumerate(data) if elem['name'] == p_name]

            if not existance:
                # create new
                data.append({'name':p_name, 'date_list':[date]})
            else:
                idx, _ = existance[0]
                if date not in data[idx]['date_list']:
                    data[idx]['date_list'].append(date)
    
    page_num += 1



#################
for elem in data:
    print(elem['name'])
    print([x.strftime('%Y.%m.%d') for x in elem['date_list']])