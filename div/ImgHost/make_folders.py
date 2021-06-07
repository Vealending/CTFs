from pathlib import Path
import csv

importFile = 'C:\\session.csv'
rootPath ='C:\\imghost\\galleries\\'
uids = list()

with open(importFile) as f:
    reader = csv.reader(f)
    galleryUrls = list(reader)

for url in galleryUrls:
    print(url)
    uid = str(url)
    uids.append(uid[-13:-3])

print(uids)

for folder in uids:
    Path(rootPath + str(folder)).mkdir(exist_ok=True)
