#!/usr/local/bin/python3

import re
from datetime import datetime, timedelta
import urllib
import urllib.parse
import urllib.request as urllib2
from xml.etree.ElementTree import ElementTree, Element, SubElement, Comment, tostring
from xml.dom import minidom
from bs4 import BeautifulSoup
import concertcrawler_file

def getPastOrchestraFromSite():
	urls = []
	
	url = 'http://www2.gol.com/users/ip0601170243/private/web/concert/pastorchestra.htm'
	ua = 'concertcrawler'

	req = urllib.request.Request(url, headers={'User-Agent':ua})
	html = urllib.request.urlopen(req)
	soup = BeautifulSoup(html, "html.parser")

	urls = []
	for tr in soup.find_all('tr'):
		tds = tr.find_all('td')
		if tds[0].a == None:
			continue
		urls.append({
			'title':tds[0].a.string.strip(),
			'url':tds[0].a.get('href'),
			'lastdate':tds[1].string.split()[0]})
	return urls

def getTextFromOrchestraSite(url, file):
	req = urllib.request.Request(url['url'], headers={'User-Agent': 'concertcrawler'})
	try:
		html = urllib.request.urlopen(req)
		if url['siteencoding']:
			soup = BeautifulSoup(html, "html.parser", fromEncoding=url['siteencoding'])
		else:
			soup = BeautifulSoup(html, "html.parser")

		[s.extract() for s in soup('style')]
		[s.extract() for s in soup('script')]

		lines = []
		for line in soup.text.split('\n'):
			line = line.strip()
			if len(line) > 0:
				lines.append(line)
		return lines
	except Exception as e:
		file.write('Scrape:' + str(e) + '\n')

def getTextAllAndOutputFile(master, urls, textfile):
	ns = {'xmlns:c': 'concert',
		'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
		'xsi:schemaLocation': 'concert Concert.xsd'}

	root = Element('c:concertCollection', ns)
	tree = ElementTree(element=root)
	comment = Comment(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
	root.append(comment)

	for url in urls:
		print(url['title'])
		try:
			textfile.write('----------------------------------------------' + '\n')
			textfile.write(url['title'] + '\n')
		except Exception as e:
			textfile.write('Output1:' + str(e) + '\n')

		lines = getTextFromOrchestraSite(url, textfile)
		if lines:
			info = concertcrawler_file.scrape1Orchestra(url['title'], lines, master)
			if 'date' in info.info:
				if info.getDate() > url['lastdate']:
					textfile.write('%s <- %s\n' % (info.getDate(), url['lastdate']))
					try:
						textfile.write(str(info.info) + '\n')
					except Exception as e:
						textfile.write('Output2:' + str(e) + '\n')

					attr = {}
					attr['date'] = info.getDate()
					attr['kaijou'] = info.getKaijou()
					attr['kaien'] = info.getKaien()
					attr['hall'] = info.getHall()
					attr['name'] = info.getTitle()
					attr['ryoukin'] = info.getRyoukin()
					concertElement = SubElement(root, 'concert', attr)
					kyokuCollectionElement = SubElement(concertElement , 'kyokuCollection')
					for kyoku in info.info['kyoku']:
						kyokuElement = SubElement(kyokuCollectionElement, 'kyoku', {'composer': kyoku['composer'], 'title': kyoku['title']})
					playerCollectionElement = SubElement(concertElement , 'playerCollection')
					for player in info.info['player']:
						playerElement = SubElement(playerCollectionElement, 'player', {'part': player, 'name': info.info['player'][player]})
			else:
				textfile.write('date not found\n')

			for line in lines:
				try:
					textfile.write(line + '\n')
				except Exception as e:
					textfile.write('Output3:' + str(e) + '\n')

	return root
