from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep

options = webdriver.ChromeOptions()
options.add_argument('--disable-notifications')

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

driver.maximize_window()

driver.get("https://flixable.com/?min-rating=0&min-year=1920&max-year=2023&order=rating#filterForm")

driver.implicitly_wait(10)

reached_page_end = False
last_height = driver.execute_script("return document.body.scrollHeight")
linkList = []

def doIt():
    for i in driver.find_elements_by_tag_name("a")[::2]:
        linkList.append(i.get_attribute('href'))
        # print(i.get_attribute('href'))



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
work = []
for i in linkList:

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



    title = titleHold[0].text
    thumbnail = findimg.get_attribute('src')
    year = details[0].text
    rating = details[4].text
    maturity = details[1].text
    seasons = details[2].text
    summary = filtered[1]
    generes = filtered[2][7:]
    cast = filtered[3][5:]

    print(title)
    print(thumbnail)
    print(year)
    print(rating)
    print(maturity)
    print(seasons)
    print(summary)
    print(generes)
    print(cast)
    print('------------------------------------')


driver.quit()