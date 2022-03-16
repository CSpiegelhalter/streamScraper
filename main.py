from asyncio.windows_events import NULL
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from concurrent import futures
from time import sleep
import database


class Moive(object):
    def __init__(self, title, thumbnail, year, rating, maturity, seasons, duration, summary, genres, cast, service):
        self.title = title
        self.thumbnail = thumbnail
        self.year = year
        self.rating = rating
        self.maturity = maturity
        self.seasons = seasons
        self.duration = duration
        self.summary = summary
        self.genres = genres
        self.cast = cast
        self.service = service


movieList = []

options = webdriver.ChromeOptions()
options.add_argument('--disable-notifications')
options.add_argument("--disable-gpu")
options.add_argument("start-maximized")
options.add_argument("enable-automation")
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-browser-side-navigation")
options.headless = False
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

# newTabDriver = webdriver.Chrome(ChromeDriverManager().install(), options=options)


# driver.maximize_window()

database.connectDB()


linkList = []


def putInDB(movieList):

    database.getConnection(movieList)
    database.disableConnection()


def doIt(links):
    # global lastAppended
    global linkList
    driver.get(links["link"])
    last_height = driver.execute_script("return document.body.scrollHeight")


    reached_page_end = False

    while not reached_page_end:
        driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL, Keys.END)
        # driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if last_height == new_height:
                reached_page_end = True
        else:
                last_height = new_height
    
        
    
    
    

    for i in driver.find_elements_by_tag_name("a")[::2]:
        linkList.append(i.get_attribute('href'))
       
        # lastAppended += 1
        # print(i.get_attribute('href'))
    if links["service"] == "netflix":
        linkList = [x for x in linkList if 'https://flixable.com/title/' in x]
    else:
        linkList = [x for x in linkList if 'https://flixable.com/'+ links["service"] +'/title/' in x]
    
    print(linkList)
    for i in linkList:
        # newTab = 'window.open("'+i+'","_blank")'
        # driver.execute_script(newTab)
        driver.get(i)
        parent = []
        # work.append(driver.find_elements_by_tag_name('span'))
        titleHold = driver.find_elements_by_xpath(
            '//h1[@class="title subpage text-left"]')
        parent.append(driver.find_elements_by_xpath(
            '//div[@class="col-lg-8"]'))
        details = (driver.find_elements_by_xpath(
            '//h6[@class="card-category"]//span'))

        findimg = driver.find_element_by_tag_name('img')

        for i in range(len(parent)):
            for j in parent[i]:
                toFilter = (j.text)

        filtered = toFilter.split('\n')

        print("--------------------------------------------------------------------------------------")
        for i in range(len(details)):
            print(details[i].text)
        print("--------------------------------------------------------------------------------------")

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

        if len(details) == 2:
            maturity = NULL
            seasons = details[1].text
            compare = seasons.split(' ')
            if compare[1] == 'MIN':
                seasons = NULL
                duration = details[1].text
            elif compare[1] == 'SEASONS' or compare[1] == 'SEASON': 
                duration = NULL
                seasons = details[1].text
            else:
                duration = NULL
                seasons = NULL
        else:
            maturity = details[1].text


            seasons = details[2].text
            compare = seasons.split(' ')
            if compare[1] == 'MIN':
                seasons = NULL
                duration = details[2].text
            elif compare[1] == 'SEASONS' or compare[1] == 'SEASON': 
                duration = NULL
                seasons = details[2].text
            else:
                duration = NULL
                seasons = NULL

        
        summary = filtered[1]

        if links["service"] == 'disney-plus':
            genres = filtered[3][7:]
        else:
            genres = filtered[2][7:]


        castSep = filtered[3].split(':')
        cast = castSep[1]

        movieList.append(Moive(title, thumbnail, year, rating,
                         maturity, seasons, duration, summary, genres, cast, links["service"]))
        print(movieList)
        
        





links = [
    {
        "link": "https://flixable.com/disney-plus/?min-rating=0&min-year=1920&max-year=2023&order=rating#filterForm",
        "service": "disney-plus"
    },
    
    {
        "link": "https://flixable.com/amazon-prime-video/?min-rating=0&min-year=1920&max-year=2023&order=rating#filterForm",
        "service": "amazon-prime-video"
    },
    {
        "link": "https://flixable.com/?min-rating=0&min-year=1920&max-year=2023&order=rating#filterForm",
        "service": "netflix"
    },
    
    {
        "link": "https://flixable.com/hbo-max/?min-rating=0&min-year=1920&max-year=2023&order=rating#filterForm",
        "service": "hbo-max"
    },
    {
        "link": "https://flixable.com/hulu/?min-rating=0&min-year=1920&max-year=2023&order=rating#filterForm",
        "service": "hulu"
    },
]

# with futures.ThreadPoolExecutor() as executor:  # default/optimized number of threads
#     list(executor.map(doIt, links))
#     for i in range(len(movieList)):
#         print(movieList[i].title)
#         print(movieList[i].service)
#         print(movieList[i].genres)
#         print("---------")


for i in range(len(links)):
    doIt(links[i])
    
    # for i in range(len(movieList)):
    #     print(movieList[i].title)
    #     print(movieList[i].service)
    #     print(movieList[i].genres)
    #     print("---------")
putInDB(movieList)



driver.quit()