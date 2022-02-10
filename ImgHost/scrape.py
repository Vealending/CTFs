from pathlib import Path
import urllib.request
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException 
import csv

importFile = 'C:\\session.csv'
rootPath ='C:\\imghost\\galleries\\'
photoUrls = list()
pages = []
i = 0
j = 0

with open(importFile) as f: # import csv and make list of urls
    reader = csv.reader(f)
    galleryUrls = list(reader)

driver = webdriver.Chrome(executable_path='C:\\chromedriver.exe')

for galUrl in galleryUrls:
    uidTemp = str(galUrl)
    uid = uidTemp[-13:-3]
    actUrl = uidTemp[2:-2]
    preliminaryPath =  rootPath + uid + "\\1.jpg"

    if not Path(rootPath + uid).is_dir(): # create folder if it doesn't exist
        Path(rootPath + uid).mkdir(exist_ok=True)
        print("folder", uid, "created!")

    if Path(preliminaryPath).is_file(): # skips gallery if there are files in the folder
        print(uid, "folder is empty")
        continue

    driver.get(actUrl + "?nw=always") # navigates to the the url in chrome    
    pagesClass = (driver.find_elements_by_class_name('ptt'))
    print(pagesClass)

    for page in pagesClass: # gets number of pages
        pages = page.find_elements_by_tag_name('td')
    pageNumber = len(pages) - 2 # minus 2 because of the arrow buttons

    j = 0 # to iterate the pages

    for x in range(pageNumber):
        actUrl = uidTemp[2:-2]+ '?p=' + str(x)
        print(actUrl)
        driver.get(actUrl)
        ids = (driver.find_elements_by_class_name('gdtm')) # gets image links from gallery
        photoUrls.clear()

        for cl in ids:
            photoUrls.append(cl.find_element_by_tag_name("a").get_attribute('href'))

        for imgUrl in photoUrls: # opens and saves the images from the gallery
            j += 1
            imgPath = rootPath + uid + '\\' + str(j) + '.jpg'
            print(imgPath)
            pathTest = Path(imgPath)
            driver.get(imgUrl)
            img = driver.find_element_by_id('img')
            if not pathTest.is_file():
                urllib.request.urlretrieve(img.get_attribute('src'), imgPath)
    print("Finished with", uid)


print("Done downloading", len(galleryUrls), "items")
driver.quit()