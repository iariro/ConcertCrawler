#!/usr/local/bin/python3

import os.path
import sys
from xml.etree.ElementTree import tostring
from xml.dom import minidom
import concertcrawler

if len(sys.argv) < 3:
	print('Usage: schemafilepath fileoutdirpath')
	sys.exit(0)

schemafilepath = sys.argv[1]
fileoutdir = sys.argv[2]

master = concertcrawler.loadConcertSchema(schemafilepath)
urls = concertcrawler.getPastOrchestraFromDB()
with open(os.path.join(fileoutdir, 'NewConcert.txt'), 'w') as file:
	root = concertcrawler.getTextAllAndOutputFile(master, urls, file)

	with open(os.path.join(fileoutdir, 'NewConcert.xml'), 'w', encoding='utf-8') as xml:
		reparsed = minidom.parseString(tostring(root, 'utf-8'))
		xml.write(reparsed.toprettyxml(indent="  "))
