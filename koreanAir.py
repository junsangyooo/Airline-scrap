def main():
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.action_chains import ActionChains
    from time import sleep

    round_trip = True
    leaving = "ICN"
    arriving = "YYZ"
    departure = 20220115
    come_back = 20221224

    ## Set Webdriver Options
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
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

    try:
        ## Run Web Using Selenium
        kurl = "https://www.koreanair.com/kr/ko"
        kdriver.get(kurl)
        kdriver.implicitly_wait(15)
        action = ActionChains(kdriver)

        ## Set From:
        button1 = WebDriverWait(kdriver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "quickbooking__location.-from")))
        button1.click()
        leave = kdriver.find_element(By.XPATH, "/html/body/ke-dynamic-modal/div/ke-airport-layer/div/div/div/div/ke-airport-chooser/div/div[1]/input")
        leave.send_keys(leaving)
        sleep(1)
        leave.send_keys(Keys.ENTER)

        ## Set To:
        button2 = WebDriverWait(kdriver, 2).until(EC.element_to_be_clickable((By.CLASS_NAME, "quickbooking__location.-to")))
        button2.click()
        arrive = kdriver.find_element(By.XPATH, "/html/body/ke-dynamic-modal/div/ke-airport-layer/div/div/div/div/ke-airport-chooser/div/div[1]/input")
        arrive.send_keys(arriving)
        sleep(1)
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
        OWN_TEXT_SCRIPT = "if(arguments[0].hasChildNodes()){var r='';var C=arguments[0].childNodes;for(var n=0;n<C.length;n++){if(C[n].nodeType==Node.TEXT_NODE){r+=' '+C[n].nodeValue}}return r.trim()}else{return arguments[0].innerText}"
        WebDriverWait(kdriver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, "flight__items.ng-star-inserted")))
        length = len(kdriver.find_elements(By.XPATH, "/html/body/app-root/div/ke-selection-flight/ke-basic-layout/div[1]/div/div[2]/div[2]/ke-air-offer-bounds-cont/ke-air-offer-bounds-pres/div/div[2]/ul/li"))
        leaving_time = ["None"] * length
        arriving_time = ["None"] * length
        flight_time = ["None"] * length
        flight_number = ["None"] * length
        flight_norm_price = ["None"] * length
        flight_flex_price = ["None"] * length
        flight_prestige_price = ["None"] * length
        i =0
        flight_list = kdriver.find_elements(By.XPATH, "/html/body/app-root/div/ke-selection-flight/ke-basic-layout/div[1]/div/div[2]/div[2]/ke-air-offer-bounds-cont/ke-air-offer-bounds-pres/div/div[2]/ul/li")
        for flight in flight_list:
            leaving_time[i] = flight.find_element(By.XPATH, "./div[1]/a/div[1]/div/div[1]/div[1]/span[2]").text
            arriving_time[i] = flight.find_element(By.XPATH, "./div[1]/a/div[1]/div/div[1]/div[2]/span[2]").text

            flight_time[i] = flight.find_element(By.XPATH, "./div[1]/a/div[1]/div/div[2]/span[2]").text    # Check Whether the flight is direct or via
            flight_direct = len(flight.find_elements(By.XPATH, "./div[1]/a/div[1]/div/div[3]/div[1]/ke-flight-desc-item/span"))
            if flight_direct == 1:
                flight_number[i] = flight.find_element(By.XPATH, "./div[1]/a/div[1]/div/div[3]/div[1]/ke-flight-desc-item/span").text
            else :
                first_flight = flight.find_element(By.XPATH, "./div[1]/a/div[1]/div/div[3]/div[1]/ke-flight-desc-item/span[1]")
                first_flight_number = kdriver.execute_script(OWN_TEXT_SCRIPT, first_flight)
                second_flight = flight.find_element(By.XPATH, "./div[1]/a/div[1]/div/div[3]/div[1]/ke-flight-desc-item/span[3]")
                second_flight_number = kdriver.execute_script(OWN_TEXT_SCRIPT, second_flight)
                flight_number[i] = first_flight_number + "     " + second_flight_number
                
            ## Scraping Economy Price 
            norm_price = flight.find_element(By.XPATH, "./div[2]/div/ke-fare-family/div[3]/div/ke-fare-info[1]/div/div/span[3]")
            if norm_price.get_attribute("class") == "flight__disabled":     # Check whether the flight is available or not
                flight_norm_price[i] = norm_price.text
            elif len(flight.find_elements(By.XPATH, "./div[2]/div/ke-fare-family/div[3]/div/ke-fare-info[1]/div/div/span[3]/span")) == 1: # Check lowest
                flight_norm_price[i] = flight.find_element(By.XPATH, "./div[2]/div/ke-fare-family/div[3]/div/ke-fare-info[1]/div/div/span[3]/span").text
            else :
                flight_norm_price[i] = flight.find_element(By.XPATH, "./div[2]/div/ke-fare-family/div[3]/div/ke-fare-info[1]/div/div/span[3]/span[2]").text

            ## Scraping Flex Price
            flex_price = flight.find_element(By.XPATH, "./div[2]/div/ke-fare-family/div[3]/div/ke-fare-info[2]/div/div/span[3]")
            if flex_price.get_attribute("class") == "flight__disabled":     # Check whether the flight is available or not
                flight_flex_price[i] = flex_price.text
            elif len(flight.find_elements(By.XPATH, "./div[2]/div/ke-fare-family/div[3]/div/ke-fare-info[2]/div/div/span[3]/span")) == 1: # Check lowest
                flight_flex_price[i] = flight.find_element(By.XPATH, "./div[2]/div/ke-fare-family/div[3]/div/ke-fare-info[2]/div/div/span[3]/span").text
            else :
                flight_flex_price[i] = flight.find_element(By.XPATH, "./div[2]/div/ke-fare-family/div[3]/div/ke-fare-info[2]/div/div/span[3]/span[2]").text

            ## Scraping Prestige Price
            prestige_price = flight.find_element(By.XPATH, "./div[2]/div/ke-fare-family/div[3]/div/ke-fare-info[3]/div/div/span[3]")
            if prestige_price.get_attribute("class") == "flight__disabled":     # Check whether the flight is available or not
                flight_prestige_price[i] = prestige_price.text
            elif len(flight.find_elements(By.XPATH, "./div[2]/div/ke-fare-family/div[3]/div/ke-fare-info[3]/div/div/span[3]/span")) == 1: # Check lowest
                flight_prestige_price[i] = flight.find_element(By.XPATH, "./div[2]/div/ke-fare-family/div[3]/div/ke-fare-info[3]/div/div/span[3]/span").text
            else :
                flight_prestige_price[i] = flight.find_element(By.XPATH, "./div[2]/div/ke-fare-family/div[3]/div/ke-fare-info[3]/div/div/span[3]/span[2]").text

            print(str(i+1) + ":")
            print("flight Num: " + flight_number[i])
            print("leaving time: " + leaving_time[i])
            print("arriving time: " + arriving_time[i])
            print("flight duration: " + flight_time[i])
            print("일반석 스탠다드 가격: " + flight_norm_price[i])
            print("일반석 플렉스 가격: " + flight_flex_price[i])
            print("프레스티지 스탠다드 가격: " + flight_prestige_price[i])
            print()
            i += 1
    except:
        kdriver.quit()
        main()
    else:
        kdriver.quit()

main()