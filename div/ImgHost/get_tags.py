from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException 
from collections import defaultdict
from pathlib import Path
import csv
import json

importFile = 'C:\\session.csv'
rootPath ='C:\\imghost\\galleries\\'
info_structured = {}

with open(importFile) as f: # import csv and make list of urls
    reader = csv.reader(f)
    galleryUrls = list(reader)

driver = webdriver.Chrome(executable_path='C:\\chromedriver.exe')

for galUrl in galleryUrls: # loops through all galleries in the csv0
    uidTemp = str(galUrl)
    uid = uidTemp[-13:-3] # only the unique identifier at the end of the url
    url = uidTemp[2:-2] # the whole url without padding

    if Path(rootPath + uid + "\\tags.json").is_file():
        print("Skipped", uid)
        continue

    driver.get(url + "?nw=always") # navigates to the the url in chrome

    try:
        name = driver.find_element_by_id('gn') 
    except NoSuchElementException:
        continue
    info_structured['name'] = name.text

    for tag in driver.find_elements_by_class_name('tc'): # finds the tags
        info_structured[tag.text[:-1]] = [] # sets the dictionary key as blank
        for t in tag.find_elements_by_xpath("..//a[starts-with(@id, 'ta_')]"): # finds all id's starting with ta_ one step up
            info_structured[tag.text[:-1]].append(t.text) #adds tag text as values to dictionary key
            
    if not Path(rootPath + uid).is_dir():
        Path(rootPath + uid).mkdir(exist_ok=True)
        print("folder", uid, "created!")

    with open(rootPath + uid + "\\tags.json", 'w',encoding='utf-8') as f: # write info to json file
        json.dump(info_structured, f, ensure_ascii=False)

    print(uid)
    info_structured.clear()

print("Done with task for", len(galleryUrls), "files")
driver.quit()






















