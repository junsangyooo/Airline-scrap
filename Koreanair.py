import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

## 여행정보 input 받기
round_trip = bool(input("Round trip? True/False "))
leaving = str(input("From where? ICN/YYZ "))
arriving = str(input("To where? ICN/YYZ "))
departure = input("When is your departure date? YYYYMMDD ")
come_back = input("When is your return date? If not round trip, just leave 'a'. YYYYMMDD ")

## 웹을오픈하지않고 안에서 돌리는거로 설정
options = webdriver.ChromeOptions()
## options.headless = True
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")

kurl = "https://www.koreanair.com/kr/ko"
# curl = "https://www.aircanada.com/kr/en/aco/home.html"

kdriver = webdriver.Chrome(options=options)
# cdriver = webdriver.Chrome(options=options)
# cdriver.maximize_window

## Selenium 사용해서 웹 실행
kdriver.get(kurl)
# cdriver.get(curl)


## 출발지 도착지 설정
kdriver.find_element(By.CLASS_NAME, "quickbooking__location.-from").click()
kdriver.find_element(By.XPATH, "/html/body/ke-dynamic-modal/div/ke-airport-layer/div/div/div/div/ke-airport-chooser/div/div[2]/ul").send_keys(leaving)
kdriver.find_element(By.CLASS_NAME, "combobox__item.auto-complete-item").click()
kdriver.find_element(By.CLASS_NAME, "quickbooking__location.-to").click()
kdriver.find_element(By.XPATH, "/html/body/ke-dynamic-modal/div/ke-airport-layer/div/div/div/div/ke-airport-chooser/div/div[1]/input").send_keys(arriving)
kdriver.find_element(By.CLASS_NAME, "combobox__item.auto-complete-item").click()


## 출국일 입국일 설정
kdriver.find_element(By.CLASS_NAME, "quickbooking__datepicker").click()
if round_trip:
    kdriver.find_element(By.ID, "ipt-depature").send_keys(departure)
    kdriver.find_element(By.ID, "ipt-arrival").send_keys(come_back)
    kdriver.find_element(By.XPATH, "/html/body/ke-dynamic-modal/div/ke-calendar/div/div/div/div[4]/div/button[2]").click()
else :
    kdriver.find_element(By.ID, "ipt-depature").send_keys(departure)
    kdriver.find_element(By.XPATH, "/html/body/ke-dynamic-modal/div/ke-calendar/div/div/div/div[4]/div/button[2]").click()
kdriver.find_element(By.ID, "quickbookingOnSearch").click()