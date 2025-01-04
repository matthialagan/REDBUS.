# import required packages
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import mysql.connector as sconn
from mysql.connector import Error

#------------------------------------------------------------------------selenium webscraping---------------------------------------------------------------------------------------#

def open_url(url):
    # this function will open the redbus website
    try:
        # Configure Chrome to run in headless mode (without opening a visible browser window)
        no_page=Options()
        no_page.add_argument('--headless')
        # driver=webdriver.Chrome(options=no_page)   #runs the code with headless(chrome window will not popup)
        driver=webdriver.Chrome()   #run the code without headleass (chrome window will popup)
        driver.get(url)
        print("url opened successfully")

    except Exception as e:
        print("Error occurred when initializing Webdriver:",e)

    return driver


def maximize_window(driver):
    # this function will maximize the browser window
    try:
        driver.maximize_window()
        print("window maximized")

    except Exception as e:
        print("Error occurred when maximize the window:",e)

def scrolling(driver):
    # the function will Scroll down through the page
    try:
        driver.find_element(By.TAG_NAME,"body").send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        print("page scrolled")

    except Exception as e:
        print("Error occurred when scrolling the page:",e)

def press_viewall(driver):
    # this function will find the view all button and select the view all button
    try:
        view_all = driver.find_elements(By.XPATH,"//a[@class='OfferSection__ViewAllText-sc-16xojcc-1 eVcjqm']")
        ref=view_all[1].get_attribute('href')
        time.sleep(2)
        driver.get(ref) # get rtc-directory
        print("viewall button pressed")

    except Exception as e:
        print("Error occured when selecting viewall button:",e)

    return driver

def fetch_state_names(driver):
    # this function will fetch the state name in the rtc-directory
    state_name=[]
    state_links=[]
    try:
        state_elements=driver.find_elements(By.XPATH,"//div[@class='D113_ul_rtc']/ul/li/a")
        for element in state_elements:
            state_name.append(element.text)
            state_links.append(element.get_attribute('href'))  #instead of fetch name , here i am fetching reference
        print(f"State names fetched: {len(state_links)}")
    except Exception as e:
        print("Error when fetching state name:",e)

    return state_links,state_name


def route_name_ref(driver,state_links,state_name):
    # this function will fetch the route name and route link from all the pages
    route_name_link=[]
    route_link=[]
    route_num=[]
    # bus_datas=[]
    count=0
    route_no=1
    state_index=0
    wait = WebDriverWait(driver, 10)
    try:
        # calling the website using the link
        for link in state_links:
            if count >=11: #change to 11 after testing , to fetch all the route data remove (if condition)
                break

            driver.get(link)
            time.sleep(2)

            page_no=driver.find_elements(By.XPATH,"//div[@class='DC_117_paginationTable']/div")
            print(f'{link} - page count - {len(page_no)}')

            if len(page_no)!=0 and count<11: #change to 11 after testing , to fetch all the route data remove (and count<3)
                try:
                    # scraping the 1st page route_name and route_link
                    route=driver.find_elements(By.XPATH,"//div[@class='route_link']/div/a")
                    for j in route:
                        route_l=j.get_attribute('href')
                        route_link.append(route_l)
                        route_nl=(route_no,state_name[state_index],j.get_attribute('title'),j.get_attribute('href'))
                        route_name_link.append(route_nl)
                        route_num.append(route_no)
                        route_no +=1
                except Exception as e:
                    pass

                no=0
                page_number=0
                # scraping other pages data
                while no < len(page_no):
                    try:
                        pagination_container=wait.until(EC.presence_of_element_located((By.XPATH,"//div[@id='root']/div/div[4]/div[12]")))
                        next_page_button=pagination_container.find_element(By.XPATH,f'//div[contains(@class,"DC_117_pageTabs") and text()="{page_number + 1}"]')
                        driver.execute_script("arguments[0].scrollIntoView();",next_page_button)
                        next_page_button.click()
                        wait.until(EC.text_to_be_present_in_element((By.XPATH, "//div[@class='DC_117_pageTabs DC_117_pageActive']"), str(page_number + 1)))
                        time.sleep(1)
                        route=driver.find_elements(By.XPATH,"//div[@class='route_link']/div/a")
                        for j in route:
                            route_l=j.get_attribute('href')
                            route_link.append(route_l)
                            route_nl=(route_no,state_name[state_index],j.get_attribute('title'),j.get_attribute('href'))
                            route_name_link.append(route_nl)
                            route_num.append(route_no)
                            route_no +=1

                    except Exception as e:
                        pass

                    no += 1
                    page_number +=1
                count += 1
            state_index += 1
        print(f"Route names and links fetched: {len(route_name_link)}", "length of route link:",len(route_link))
        print("total route_no",route_num)
    except Exception as e:
        print("Error occured when scraping bus route and link:",e)
    
    return route_name_link,route_link,route_num

def fetch_bus_datas(driver,route_link,no_route):
    # scroll and fetch all the bus details of each routes
    wait = WebDriverWait(driver, 10)
    bus_datas=[]
    reference=0
    bus_no=0
    while reference<len(route_link):
        driver.get(route_link[reference])
        print(f"Fetching data from route: {route_link[reference]}")
        time.sleep(1)

        try:
            # click the viewall button in reverse order
            goverment_buses=wait.until(EC.visibility_of_element_located((By.XPATH,"//div[@class='button']")))
            buttons=driver.find_elements(By.XPATH,"//div[@class='button']")
            print("Button length",len(buttons))
            button_index = len(buttons)-1
            if len(buttons)!=0:
                for _ in buttons:
                    buttons[button_index].click()  
                    time.sleep(3)
                    button_index -= 1

        except Exception as e:
            pass  
            
        # scrolling page from top to bottom
        old_page=""
        looping=True
        while looping:
            driver.find_element(By.TAG_NAME,'body').send_keys(Keys.END)
            time.sleep(1)

            new_page=driver.page_source
            if new_page==old_page:
                looping=False
            else:
                old_page=new_page

            total_bus=driver.find_elements(By.XPATH,"//div[@class='clearfix row-one']")
            time.sleep(1)

        # fetching bus betails like busname, bustype, departing time, duration, reachingtime, starrating, price, seatavailable and append it to an list
        for bus_l in total_bus:
            try:
                bus_name=bus_l.find_element(By.CSS_SELECTOR, "div.travels.lh-24.f-bold.d-color")

                bus_type=bus_l.find_element(By.CSS_SELECTOR, "div.bus-type.f-12.m-top-16.l-color.evBus")

                departing_time=bus_l.find_element(By.CSS_SELECTOR,"div.dp-time.f-19.d-color.f-bold")

                duration=bus_l.find_element(By.CSS_SELECTOR,"div.dur.l-color.lh-24")

                reaching_time=bus_l.find_element(By.CSS_SELECTOR,"div.bp-time.f-19.d-color.disp-Inline")

                star_rating=bus_l.find_element(By.CSS_SELECTOR,"div.rating-sec span")

                price=bus_l.find_element(By.CSS_SELECTOR,"span.f-19.f-bold")

                total_seat_availability=bus_l.find_element(By.CSS_SELECTOR,".seat-left").text
                seat_availability=total_seat_availability.split()[0]

                bus_datas.append((no_route[bus_no],bus_name.text,bus_type.text,departing_time.text,duration.text,reaching_time.text,star_rating.text,price.text,seat_availability))
                
            except Exception as e:
                continue

        print("bus_no",bus_no,"==","route_no",no_route[bus_no])
        bus_no += 1  

        reference += 1
        print(f"Total bus data entries fetched: {len(bus_datas)}")

    return bus_datas

def quit_driver(driver):
    #this function will quit the driver
    driver.quit()

url = "https://www.redbus.in/"  # website url

driver = open_url(url) #call the open_url function (this will open the website)

maximize_window(driver) #call the maximize_window function(this will maximize the window)

scrolling(driver)  #call the scrolling function (this will scroll the page once)

driver=press_viewall(driver) #calls the press_viewall function (this will press the viewall button)

link_states,state_name=fetch_state_names(driver) #calls the fetch_state_names function (this will scrape the state name and links)

name_link_state,route_ref,route_number=route_name_ref(driver,link_states,state_name) #calls the route_name_ref function (this will scrape the route name and route link )

bus_details=fetch_bus_datas(driver,route_ref,route_number) #calls the fetch_bus_data (this will scrape the bus details of the specific routes)

quit_driver(driver) #quitting the driver after fetching the data


# convert the bus_details into dataframe 
bus_data=pd.DataFrame(data=bus_details,columns=['bus_no','bus_name','bus_type','departing_time','duration','reaching_time','star_rating','price','seat_availability'])
bus_data['star_rating'] = bus_data['star_rating'].fillna(0)


# convert the route_details into dataframe 
normal_route_data=pd.DataFrame(data=name_link_state,columns=['route_no','state_name','route_name','route_ref'])
print("length of route_data",len(normal_route_data))

#check whether the bus_no and route_no is same
unique_bus_no = bus_data['bus_no'].unique()
route_data= normal_route_data[normal_route_data['route_no'].isin(unique_bus_no)]


# write the route_data and bus_data in .csv file for reference
route_data.to_csv('route_data.csv',index=False,mode='w')
bus_data.to_csv('bus_data.csv',index=False,mode='w')


#check both bus_no from bus_data and route_no from route_data is same (--------------testing------------)
unique_bus_no = bus_data['bus_no'].unique()
unique_route_no = route_data['route_no'].unique()

if set(unique_bus_no) == set(unique_route_no):
    print("The unique bus numbers and route numbers match.")
else:
    print("The unique bus numbers and route numbers do not match.")
