import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

## Getting Input Data for Flight
# round_trip = bool(input("Round trip? True/False "))
# leaving = input("From where? ICN/YYZ ")
# arriving = input("To where? ICN/YYZ ")
# departure = input("When is your departure date? YYYYMMDD ")
# come_back = input("When is your return date? If not round trip, just leave 'a'. YYYYMMDD ")
round_trip = True
leaving = "YYZ"
arriving = "ICN"
departure = 20220108
come_back = 20220824

## Set Webdriver Options
options = webdriver.ChromeOptions()
## options.headless = True
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")
kdriver = webdriver.Chrome(options=options)
kdriver.maximize_window

## Run Web Using Selenium
kurl = "https://www.koreanair.com/kr/ko"
kdriver.get(kurl)


## Set From:
kdriver.find_element(By.CLASS_NAME, "quickbooking__location.-from").click()
kdriver.find_element(By.XPATH, "/html/body/ke-dynamic-modal/div/ke-airport-layer/div/div/div/div/ke-airport-chooser/div/div[1]/input").send_keys(leaving)
leave = WebDriverWait(kdriver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#item0")))
leave.click()


## Set To:
kdriver.find_element(By.XPATH, "/html/body/div[7]/div[2]/div/div/div[2]/ke-main/ke-quick-booking/div/div/div/div/div[1]/ke-quick-booking-ow-rt/div[1]/div/ke-airport-selector/button[2]").click()
kdriver.find_element(By.XPATH, "/html/body/ke-dynamic-modal/div/ke-airport-layer/div/div/div/div/ke-airport-chooser/div/div[1]/input").send_keys(arriving)
arrive = WebDriverWait(kdriver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#item0")))
arrive.click()


## Set Departure and Return
kdriver.find_element(By.CLASS_NAME, "quickbooking__datepicker").click()
if round_trip:
    kdriver.find_element(By.ID, "ipt-depature").send_keys(departure)
    kdriver.find_element(By.ID, "ipt-arrival").send_keys(come_back)
    kdriver.find_element(By.XPATH, "/html/body/ke-dynamic-modal/div/ke-calendar/div/div/div/div[4]/div/button[2]").click()
else :
    kdriver.find_element(By.ID, "ipt-depature").send_keys(departure)
    kdriver.find_element(By.XPATH, "/html/body/ke-dynamic-modal/div/ke-calendar/div/div/div/div[4]/div/button[2]").click()
kdriver.find_element(By.ID, "quickbookingOnSearch").click()