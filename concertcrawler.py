#!/usr/bin/python3

import sys
import os.path
from xml.etree.ElementTree import tostring
from xml.dom import minidom
import lib.concertcrawler_file as concertcrawler_file
import lib.concertcrawler_db as concertcrawler_db
import lib.concertcrawler_net as concertcrawler_net
from ftplib import FTP

if len(sys.argv) < 3:
	print('Usage: schemafilepath fileoutdirpath')
	sys.exit(0)

schemafilepath = sys.argv[1]
fileoutdir = sys.argv[2]
dbhost = sys.argv[3]

crawl = True
upload = True

if crawl:
	master = concertcrawler_file.loadConcertSchema(schemafilepath)
	urls = concertcrawler_db.getPastOrchestraFromDB(dbhost)
	with open(os.path.join(fileoutdir, 'NewConcert.txt'), 'w', encoding='utf-8') as file:
		root = concertcrawler_net.getTextAllAndOutputFile(master, urls, file)

	with open(os.path.join(fileoutdir, 'NewConcert.xml'), 'w', encoding='utf-8') as xml:
		reparsed = minidom.parseString(tostring(root, 'utf-8'))
		xml.write(reparsed.toprettyxml(indent="  "))

if upload:
	FTP.encoding = "utf-8"
	FTP.maxline = 16384
	ftp = FTP("www2.gol.com", "ip0601170243", passwd="Z#5uqBpt")
	with open(os.path.join(fileoutdir, 'NewConcert.txt'), "rb") as f:
		ftp.storlines("STOR /private/data/concert/NewConcert.txt", f)
	with open(os.path.join(fileoutdir, 'NewConcert.xml'), "rb") as f:
		ftp.storlines("STOR /private/data/concert/NewConcert.xml", f)
