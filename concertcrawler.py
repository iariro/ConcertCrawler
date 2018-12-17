import sys
sys.path.append('lib')
import os.path
from xml.etree.ElementTree import tostring
from xml.dom import minidom
import concertcrawler_file
import concertcrawler_db
import concertcrawler_net

if len(sys.argv) < 3:
	print('Usage: schemafilepath fileoutdirpath')
	sys.exit(0)

schemafilepath = sys.argv[1]
fileoutdir = sys.argv[2]
dbhost = sys.argv[3]

master = concertcrawler_file.loadConcertSchema(schemafilepath)
urls = concertcrawler_db.getPastOrchestraFromDB(dbhost)
with open(os.path.join(fileoutdir, 'NewConcert.txt'), 'w') as file:
	root = concertcrawler_net.getTextAllAndOutputFile(master, urls, file)

	with open(os.path.join(fileoutdir, 'NewConcert.xml'), 'w', encoding='utf-8') as xml:
		reparsed = minidom.parseString(tostring(root, 'utf-8'))
		xml.write(reparsed.toprettyxml(indent="  "))
