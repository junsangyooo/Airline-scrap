def main():
    import requests
    from bs4 import BeautifulSoup
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.action_chains import ActionChains
    from time import sleep


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
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")
    kdriver = webdriver.Chrome(options=options)
    kdriver.maximize_window

    ## Run Web Using Selenium
    try:
        kurl = "https://www.koreanair.com/kr/ko"
        kdriver.get(kurl)
        kdriver.implicitly_wait(15)
        action = ActionChains(kdriver)

        ## Set From:
        button1 = WebDriverWait(kdriver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "quickbooking__location.-from")))
        button1.click()
        leave = kdriver.find_element(By.XPATH, "/html/body/ke-dynamic-modal/div/ke-airport-layer/div/div/div/div/ke-airport-chooser/div/div[1]/input")
        leave.send_keys(leaving)
        leave.send_keys(Keys.ENTER)

        ## Set To:
        button2 = WebDriverWait(kdriver, 2).until(EC.element_to_be_clickable((By.CLASS_NAME, "quickbooking__location.-to")))
        button2.click()
        arrive = kdriver.find_element(By.XPATH, "/html/body/ke-dynamic-modal/div/ke-airport-layer/div/div/div/div/ke-airport-chooser/div/div[1]/input")
        arrive.send_keys(arriving)
        arrive.send_keys(Keys.ENTER)



        ## Set Departure and Return
        button3 = WebDriverWait(kdriver, 2).until(EC.element_to_be_clickable((By.CLASS_NAME, "quickbooking__datepicker")))
        button3.click()
        if round_trip:
            kdriver.find_element(By.ID, "ipt-depature").send_keys(departure)
            kdriver.find_element(By.ID, "ipt-arrival").send_keys(come_back)
            kdriver.find_element(By.XPATH, "/html/body/ke-dynamic-modal/div/ke-calendar/div/div/div/div[4]/div/button[2]").click()
        else :
            kdriver.find_element(By.ID, "ipt-depature").send_keys(departure)
            kdriver.find_element(By.XPATH, "/html/body/ke-dynamic-modal/div/ke-calendar/div/div/div/div[4]/div/button[2]").click()

        ## Search Flights
        button = WebDriverWait(kdriver, 2).until(EC.element_to_be_clickable((By.CLASS_NAME, "quickbooking__find")))
        action.move_to_element(button)
        button.click()
        kdriver.implicitly_wait(20)

        ## Print Flights
        WebDriverWait(kdriver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, "flight__items.ng-star-inserted")))
        flight_list = kdriver.find_elements(By.CLASS_NAME, "flight__item.ng-star-inserted")
        for flight in flight_list:
            leaving_time = flight.find_element(By.XPATH, "./div[1]/a/div[1]/div/div[1]/div[1]/span[2]").text
            arriving_time = flight.find_element(By.XPATH, "./div[1]/a/div[1]/div/div[1]/div[2]/span[2]").text
            flight_time = flight.find_element(By.XPATH, "./div[1]/a/div[1]/div/div[2]/span[2]").text
            flight_number = flight.find_element(By.XPATH, "./div[1]/a/div[1]/div/div[3]/div[1]/ke-flight-desc-item/span").text
            try:
                flight_norm_price = flight.flind_element(By.XPATH, "./div[2]/div/ke-fare-family/div[3]/div/ke-fare-info[1]/div/div/span[3]/span").text
            except:
                flight_norm_price = flight.find_element(By.XPATH, "./div[2]/div/ke-fare-family/div[3]/div/ke-fare-info[1]/div/div[1]/span[3]").text
            
            try:
                flight_flex_price = flight.find_element(By.XPATH, "./div[2]/div/ke-fare-family/div[3]/div/ke-fare-info[2]/div/div/span[3]/span").text
            except:
                flight_flex_price = flight.find_element(By.XPATH, "./div[2]/div/ke-fare-family/div[3]/div/ke-fare-info[2]/div/div[1]/span[3]").text

            try:
                flight_prestige_price = flight.flind_element(By.XPATH, "./div[2]/div/ke-fare-family/div[3]/div/ke-fare-info[3]/div/div/span[3]/span").text
            except:
                flight_prestige_price = flight.find_element(By.XPATH, "./div[2]/div/ke-fare-family/div[3]/div/ke-fare-info[3]/div/div[1]/span[3]").text
            print("flight Num: " + flight_number)
            print("leaving time: " + leaving_time)
            print("arriving time: " + arriving_time)
            print("flight duration: " + flight_time)
            print("일반석 스탠다드 가격: " + flight_norm_price)
            print("일반석 플렉스 가격: " + flight_flex_price)
            print("프레스티지 스탠다드 가격: " + flight_prestige_price)
    except:
        kdriver.quit
        main()
    else:
        kdriver.quit
        quit()

main()