import chromedriver_autoinstaller
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from datetime import datetime
import os
from dotenv import load_dotenv

# .env
load_dotenv(verbose=True)

driver = None

def driver_init():
    global driver
    chromedriver_autoinstaller.install()    # Check if the current version of chromedriver exists
                                            # and if it doesn't exist, download it automatically,
                                            # then add chromedriver to path

    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)


def standalone_driver_init():
    global driver

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Remote(os.getenv('REMOTE_SERVER_URL'), options=options)


def driver_close():
    global driver
    try:
        driver.close()
    except:
        print("no driver to close")


def login():
    global driver
    ID = os.getenv('ID')
    PW = os.getenv('PW')
   
    driver.get("https://pay.ssg.com/myssg/orderInfo.ssg?viewType=Ssg")
    driver.find_element_by_name('mbrLoginId').send_keys(ID)
    driver.find_element_by_name('password').send_keys(PW)
    driver.find_element_by_xpath("//button[@id='loginBtn']").click()
    time.sleep(3)


def search(collection, search_start, search_end):
    global driver

    page_num = 1
    while True:
        driver.get(f"https://pay.ssg.com/myssg/orderInfo.ssg?searchType=5&searchCheckBox=&page={page_num}&searchInfloSiteNo=&searchStartDt={search_start}&searchEndDt={search_end}&searchKeyword=")
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        if soup.find("div", {"class":"codr_no"}):
            break   # exceeded max page
        
        print(f"scraping {search_start} ~ {search_end}: page {page_num}")  # log

        for order in soup.find_all("div", {"class":"codr_odrdeliv"}):
            # get date
            date_str = order.find("span", {"class":"codr_odrdeliv_odrdate"}).text
            # date = datetime.strptime(date_str, '%Y.%m.%d')  # datetime object

            # get product names
            for product in order.find_all("span", {"class":"codr_unit_name"}):
                p_name = product.text.strip().replace("\n","").replace("\t","")

                # check existance
                pre_existence = collection.find_one({'name': p_name})

                if not pre_existence:
                    # create new
                    collection.insert_one({'name':p_name, 'date_list':[date_str]})
                else:
                    # append date_str to date_list (avoid duplicate)
                    collection.update_one({'name': p_name}, {"$addToSet": {'date_list': date_str}})

        page_num += 1


def get_groceries_data(db):
    if os.getenv('SERVER_ENV') == "NAS":
        standalone_driver_init()
    else:
        driver_init()

    login()
    today = datetime.now().strftime('%Y-%m-%d')
    search(db.recipt, "2022-01-01", today)
    # search(db.recipt, "2021-01-01", "2021-12-31")
    # search(db.recipt, "2020-01-01", "2020-12-31")
    # search(db.recipt, "2019-01-01", "2019-12-31")
    driver_close()


if __name__ == '__main__':
    get_groceries_data()