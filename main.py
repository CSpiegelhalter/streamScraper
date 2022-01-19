from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
driver = webdriver.Chrome(ChromeDriverManager().install())

driver.maximize_window()

driver.get("https://flixable.com/?min-rating=0&min-year=1920&max-year=2023&order=rating#filterForm")

driver.implicitly_wait(10)

reached_page_end = False
last_height = driver.execute_script("return document.body.scrollHeight")
linkList = []

def doIt():
    for i in driver.find_elements_by_tag_name("a")[::2]:
        linkList.append(i.get_attribute('href'))
        print(i.get_attribute('href'))



# while not reached_page_end:
#       driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL, Keys.END);  
#       sleep(2)
#       new_height = driver.execute_script("return document.body.scrollHeight")
#       if last_height == new_height:
#             reached_page_end = True
#             doIt()
#       else:
#             last_height = new_height

doIt()
linkList = [x for x in linkList if 'https://flixable.com/title/' in x]
print("--------*******------------")
print(linkList)
driver.quit()