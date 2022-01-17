#!/usr/bin/python3

import sys
import os.path
from xml.etree.ElementTree import tostring
from xml.dom import minidom
import lib.concertcrawler_file as concertcrawler_file
import lib.concertcrawler_db as concertcrawler_db
import lib.concertcrawler_net as concertcrawler_net
from ftplib import FTP
import ftplib
import requests

if len(sys.argv) < 3:
    print('Usage: schemafilepath fileoutdirpath [-crawl=True|False] [-upload=True|False]')
    sys.exit(0)

schemafilepath = sys.argv[1]
fileoutdir = sys.argv[2]
dbhost = sys.argv[3]

crawl = True
upload = True

for arg in sys.argv:
    if arg == '-crawl=False':
        crawl = False
    elif arg == '-upload=False':
        upload = False

if crawl:
    master = concertcrawler_file.loadConcertSchema(schemafilepath)
    urls = concertcrawler_db.getPastOrchestraFromDB_HTTP(dbhost)
    with open(os.path.join(fileoutdir, 'NewConcert.txt'), 'w', encoding='utf-8') as file:
        root = concertcrawler_net.getTextAllAndOutputFile(master, urls, file)

    with open(os.path.join(fileoutdir, 'NewConcert.xml'), 'w', encoding='utf-8') as xml:
        reparsed = minidom.parseString(tostring(root, 'utf-8'))
        xml.write(reparsed.toprettyxml(indent="  "))

    # notify to LINE
    token = "nPQEoC190nfvydJRbQmY75SY00Ygvt0CxsaXWoLTUUH"
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": "Bearer " + token}
    payload = {"message": "コンサート情報{}件を収集しました".format(len(root))}
    requests.post(url, headers=headers, data=payload)

if upload:
    FTP.encoding = "utf-8"
    FTP.maxline = 16384
    ftp = FTP("www2.gol.com", "ip0601170243", passwd="Z#5uqBpt")
    try:
        with open(os.path.join(fileoutdir, 'NewConcert.xml'), "rb") as f:
            ftp.storlines("STOR /private/data/concert/NewConcert.xml", f)
    except ftplib.all_errors as e:
        print(f.name, e)

    try:
        with open(os.path.join(fileoutdir, 'NewConcert.txt'), "rb") as f:
            ftp.storlines("STOR /private/data/concert/NewConcert.txt", f)
    except ftplib.all_errors as e:
        print(f.name, e)
