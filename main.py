from asyncio.windows_events import NULL
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from multiprocessing import Event, Process
from time import sleep
import database 

options = webdriver.ChromeOptions()
options.add_argument('--disable-notifications')
options.headless = True

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
# newTabDriver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

driver.maximize_window()

database.connectDB()

driver.get("https://flixable.com/?min-rating=0&min-year=1920&max-year=2023&order=rating#filterForm")
linkList = []

def putInDB(linkList):
    linkList = [x for x in linkList if 'https://flixable.com/title/' in x]
    for i in linkList:
        # newTab = 'window.open("'+i+'","_blank")'
        # driver.execute_script(newTab)
        driver.get(i)
        parent = []
        # work.append(driver.find_elements_by_tag_name('span'))
        titleHold = driver.find_elements_by_xpath('//h1[@class="title subpage text-left"]')
        parent.append(driver.find_elements_by_xpath('//div[@class="col-lg-8"]'))
        details = (driver.find_elements_by_xpath('//h6[@class="card-category"]//span'))

        findimg = driver.find_element_by_tag_name('img')



        for i in range(len(parent)):
            for j in parent[i]:
                toFilter = (j.text)

        filtered = toFilter.split('\n')

        print(details)

        title = titleHold[0].text
        thumbnail = findimg.get_attribute('src')
        year = details[0].text

        if (len(details) == 5):
            rating = details[4].text
        elif (len(details) == 4):
            rating = details[3].text
        else:
            rating = NULL
        # rating = details[4].text
        maturity = details[1].text
        seasons = details[2].text
        summary = filtered[1]
        generes = filtered[2][7:]
        castSep = filtered[3].split(':')
        cast = castSep[1]

        database.getConnection(title, thumbnail, year, rating, maturity, seasons, summary, generes, cast)




def doIt():
    global lastAppended
    global linkList
    for i in driver.find_elements_by_tag_name("a")[::2]:
            linkList.append(i.get_attribute('href'))
        # lastAppended += 1
        # print(i.get_attribute('href'))
    putInDB(linkList)
    


last_height = driver.execute_script("return document.body.scrollHeight")


reached_page_end = False

while not reached_page_end:
    driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL, Keys.END); 
    # driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') 
    sleep(1.5)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if last_height == new_height:
            reached_page_end = True
            doIt()
    else:
            last_height = new_height

# doIt()









driver.quit()
database.disableConnection()