#!/usr/local/bin/python3

import re
import pandas as pd
from datetime import datetime, timedelta
import pymssql
import urllib
import urllib.parse
import urllib.request as urllib2
from xml.etree.ElementTree import ElementTree, Element, SubElement, Comment, tostring
from xml.dom import minidom
from bs4 import BeautifulSoup

def getPastOrchestraFromDB(host):
	sql = '''select Player.name as title, Player.siteurl as url, Player.siteencoding, Player.active, max(Concert.date) as lastdate from Concert
	join Shutsuen on Shutsuen.concertId=Concert.id
	join Player on Player.id=Shutsuen.playerId
	where Shutsuen.partId=1 and len(Player.siteurl)>0 and Player.active=1
	group by player.id, Player.name, Player.siteurl, Player.siteencoding, Player.active
	having max(Concert.date) < getdate() order by max(Concert.date)
	'''
	connect = pymssql.connect(host='%s:2144' % (host), user='sa', password='p@ssw0rd', database='concert', charset='sjis')
	df = pd.io.sql.read_sql(sql, connect)
	connect.close()

	urls = []
	for index, row in df.iterrows():
		urls.append({
			'title': row['title'],
			'url': row['url'],
			'siteencoding': row['siteencoding'],
			'active': row['active'],
			'lastdate': row['lastdate'].strftime('%Y/%m/%d')})
	return urls

def getPastOrchestraFromDB_HTTP(host):
	url = 'http://{}:8080/kumagai/pastorchestralist'.format(host)
	ua = 'concertcrawler'

	req = urllib.request.Request(url, headers={'User-Agent': ua})
	html = urllib.request.urlopen(req).read().decode("utf-8")

	urls = []
	for line in html.split('\n'):
		csv = line.split(',')
		if len(csv) == 5:
			urls.append({
				'title': csv[0],
				'url': csv[1],
				'siteencoding': csv[2],
				'active': csv[3],
				'lastdate': csv[4]})
	return urls

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

def zenkakuToHankaku(zenkaku):
	digitMap = {}
	digitMap['０'] = '0'
	digitMap['１'] = '1'
	digitMap['２'] = '2'
	digitMap['３'] = '3'
	digitMap['４'] = '4'
	digitMap['５'] = '5'
	digitMap['６'] = '6'
	digitMap['７'] = '7'
	digitMap['８'] = '8'
	digitMap['９'] = '9'
	digitMap['：'] = ':'

	hankaku = ""
	for c in zenkaku:
		if c in digitMap:
			hankaku += digitMap[c]
		else:
			hankaku += c
	return hankaku

class ConcertInformation:
	def __init__(self):
		self.info = {}
		self.info['kyoku'] = []
		self.info['player'] = {}

	def set(self, key, value):
		if key not in self.info:
			self.info[key] = value

	def setDate(self, value):
		if ('date' not in self.info) or (value > self.info['date']):
			self.info['date'] = value

	def get(self, key):
		return self.info[key]

	def getName(self):
		if 'name' in self.info:
			return self.info['name']
		else:
			return ''

	def getDate(self):
		if 'date' in self.info:
			return self.info['date']
		else:
			return '12:00'

	def getKaijou(self):
		if 'kaijou' in self.info:
			return self.info['kaijou']
		elif 'kaien' in self.info:
			kaien2 = datetime.strptime(self.info['kaien'], "%H:%M")
			kaijou = kaien2 - timedelta(minutes=30)
			return kaijou.strftime('%H:%M')
		else:
			return '12:00'

	def getKaien(self):
		if 'kaien' in self.info:
			return self.info['kaien']
		else:
			return '12:00'

	def getHall(self):
		if 'hall' in self.info:
			return self.info['hall']
		else:
			return ''

	def getRyoukin(self):
		if 'ryoukin' in self.info:
			return self.info['ryoukin']
		else:
			return ''

	def getTitle(self):
		if 'title' in self.info:
			return self.info['title']
		else:
			return ''

def scrape1Orchestra(orchestra, lines, master):
	info = ConcertInformation()
	for line in lines:
		date11 = re.search('（*([0-9]{4}) *年）* *([0-9]*) *月 *([0-9]*) *日', line)
		date12 = re.search('（*([０-９]{4}) *年）* *([０-９]*) *月 *([０-９]*) *日', line)
		date2 = re.search('平成([０-９]*)年([０-９]*)月([０-９]*)日', line)
		date31 = re.search('([0-9]{2})/([0-9]*)/([0-9]{1-2})', line)
		date32 = re.search('([0-9]{4})/([0-9]{1-2})/([0-9]{1-2})', line)
		date4 = re.search('([0-9]{4})\.([0-9]{1-2})\.([0-9]{1-2})', line)
		date5 = re.search('([0-9]{4})-([0-9]{1-2})-([0-9]{1-2})', line)

		year = None
		month = None
		day = None
		if date11:
			year = zenkakuToHankaku(date11.group(1))
			month = zenkakuToHankaku(date11.group(2))
			day = zenkakuToHankaku(date11.group(3))
		elif date12:
			year = zenkakuToHankaku(date12.group(1))
			month = zenkakuToHankaku(date12.group(2))
			day = zenkakuToHankaku(date12.group(3))
		elif date2:
			year = int(zenkakuToHankaku(date2.group(1))) + 1988
			month = int(zenkakuToHankaku(date2.group(2)))
			day = int(zenkakuToHankaku(date2.group(3)))
		elif date31:
			year = int(zenkakuToHankaku(date31.group(1))) + 2000
			month = int(zenkakuToHankaku(date31.group(2)))
			day = int(zenkakuToHankaku(date31.group(3)))
		elif date32:
			year = int(zenkakuToHankaku(date32.group(1)))
			month = int(zenkakuToHankaku(date32.group(2)))
			day = int(zenkakuToHankaku(date32.group(3)))
		elif date4:
			year = int(zenkakuToHankaku(date4.group(1)))
			month = int(zenkakuToHankaku(date4.group(2)))
			day = int(zenkakuToHankaku(date4.group(3)))
		elif date5:
			year = int(zenkakuToHankaku(date5.group(1)))
			month = int(zenkakuToHankaku(date5.group(2)))
			day = int(zenkakuToHankaku(date5.group(3)))

		if year and month and day:
			info.setDate("%04d/%02d/%02d" % (int(year), int(month), int(day)))

		kaijou0 = re.search('午後([0-9０-９]*)時([0-9０-９]*)分開場', line)
		kaijou1 = re.search('([0-9０-９]{2}[:：][0-9０-９]{2})[ 　]*開場', line)
		kaijou21 = re.search('開場：*　*([0-9０-９]*[:：][0-9０-９]*)', line)
		kaijou22 = re.search('開場 PM *([0-9０-９]*)[:：]([0-9０-９]*)', line)
		kaijou3 = re.search('([0-9０-９]*)時開場', line)
		kaijou4 = re.search('([0-9０-９]*)時([0-9０-９]*)分 *開場', line)

		kaien0 = re.search('午後([0-9０-９]*)時開演', line)
		kaien1 = re.search('([0-9０-９]{2}[:：][0-9０-９]{2})[ 　]*開演', line)
		kaien21 = re.search('開演：*　*([0-9０-９]*[:：][0-9０-９]*)', line)
		kaien22 = re.search('開演 PM *([0-9０-９]*)[:：]([0-9０-９]*)', line)
		kaien3 = re.search('([0-9０-９]*)時開演', line)
		kaien4 = re.search('([0-9０-９]*)時([0-9０-９]*)分 *開演', line)

		if kaijou0:
			hour = int(zenkakuToHankaku(kaijou0.group(1))) + 12
			minute = zenkakuToHankaku(kaijou0.group(2))
			info.set('kaijou', "%2d:%s" % (hour, minute))
		elif kaijou1:
			info.set('kaijou', zenkakuToHankaku(kaijou1.group(1)))
		elif kaijou21:
			info.set('kaijou', zenkakuToHankaku(kaijou21.group(1)))
		elif kaijou22:
			hour = int(zenkakuToHankaku(kaijou22.group(1))) + 12
			minute = zenkakuToHankaku(kaijou22.group(2))
			info.set('kaijou', "%2d:%s" % (hour, minute))
		elif kaijou3:
			info.set('kaijou', zenkakuToHankaku(kaijou3.group(1)) + ":00")
		elif kaijou4:
			info.set('kaijou', zenkakuToHankaku(kaijou4.group(1) + ":" + kaijou4.group(2)))

		if kaien0:
			info.set('kaien', "%02d:00" % (int(zenkakuToHankaku(kaien0.group(1))) + 12))
		elif kaien21:
			info.set('kaien', zenkakuToHankaku(kaien21.group(1)))
		elif kaien22:
			hour = int(zenkakuToHankaku(kaien22.group(1))) + 12
			minute = zenkakuToHankaku(kaien22.group(2))
			info.set('kaien', "%2d:%s" % (hour, minute))
		elif kaien1:
			info.set('kaien', zenkakuToHankaku(kaien1.group(1)))
		elif kaien3:
			info.set('kaien', zenkakuToHankaku(kaien3.group(1)) + ":00")
		elif kaien4:
			info.set('kaien', zenkakuToHankaku(kaien4.group(1) + ":" + kaien4.group(2)))

		titles = []
		titles.append(re.search('.*(第.*回 *演奏会).*', line))
		titles.append(re.search('(第.*回 *公演)', line))
		titles.append(re.search('(第.*回定期公演)', line))
		titles.append(re.search('(第[0-9０-９]*回定期演奏会).*', line))
		titles.append(re.search('(第.*回特別演奏会)', line))
		titles.append(re.search('(第.*回.*コンサート)', line))
		titles.append(re.search('(.*特別演奏会)', line))
		titles.append(re.search('(.*[^ ]* Concert)', line))

		for title in titles:
			if title:
				info.set('title', title.group(1))
				break

		for hall in master['hallName']:
			if hall in line:
				info.set('hall', hall)
			else:
				hallkeywords = hall.split()
				if len([hallkeyword for hallkeyword in hallkeywords if hallkeyword in line]) == len(hallkeywords):
					info.set('hall', hall)

		ryoukin1 = re.search('(全席指定.*円)', line)
		ryoukin2 = re.search('入場料：(.*円)', line)

		if '入場無料' in line:
			info.set('ryoukin', '入場無料')
		elif ryoukin1:
			info.set('ryoukin', ryoukin1.group(1))
		elif ryoukin2:
			info.set('ryoukin', ryoukin2.group(1))

		for composer in master['composerName']:
			if composer in line:
				kyokumoku1 = re.search(composer + "[ 　]*[:：/／][ 　]*(.*)", line)
				kyokumoku2 = re.search("(.*)[ 　]*[:：/／][ 　]" + composer, line)
				kyokumoku3 = re.search(composer + "[ 　]*(.*)", line)

				if kyokumoku1:
					title = kyokumoku1.group(1)
					if len(title) > 50:
						title2 = []
						for titleparts in title.split():
							if len(" ".join(title2)) > 50:
								break
							title2.append(titleparts)
						title = " ".join(title2)
					info.info['kyoku'].append({'composer': composer, 'title': title})
					break
				elif kyokumoku2:
					title = kyokumoku2.group(1)
					info.info['kyoku'].append({'composer': composer, 'title': title})
					break
				elif kyokumoku3:
					title = kyokumoku3.group(1)
					info.info['kyoku'].append({'composer': composer, 'title': title})
					break

		conductor = re.search("指揮[  :：](.*)", line)
		if conductor:
			info.info['player']['指揮'] = conductor.group(1)
		info.info['player']['管弦楽'] = orchestra

	return info

def scrapeAllFromFile(master, concertinfofilepath):
	totalCount = 0
	dateCount = 0
	titleCount = 0
	kaijouCount = 0
	kaienCount = 0
	root = Element('Concert')
	tree = ElementTree(element=root)

#        Element top = createElement("c:concertCollection");
#        appendChild(top);
#        top.setAttributeNS("http://www.w3.org/2000/xmlns/", "xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance");
#        top.setAttributeNS("http://www.w3.org/2000/xmlns/", "xmlns:c", "concert");
#        top.setAttributeNS("http://www.w3.org/2001/XMLSchema-instance", "xsi:schemaLocation", "concert Concert.xsd");

	with open(concertinfofilepath, encoding='utf-8') as file:
		lines = []
		lineFlag = False
		orchestra = None
		for line in file:
			line = line.strip()

			if lineFlag:
				orchestra = line
				lineFlag = False
			else:
				if line == '----------------------------------------------':
					lineFlag = True
					if len(lines) > 0:
						info = scrape1Orchestra(orchestra, lines, master)
						totalCount += 1
						if 'date' in info:
							dateCount += 1
						if 'kaijou' in info:
							kaijouCount += 1
						if 'kaien' in info:
							kaienCount += 1
						if 'title' in info:
							titleCount +=1
						print("%s %s" % (orchestra, info))
						attr = {}
						if 'date' in info:
							attr['date'] = info['date']
						if 'kaijou' in info:
							attr['kaijou'] = info['kaijou']
						if 'kaien' in info:
							attr['kaien'] = info['kaien']
						if 'title' in info:
							attr['title'] = info['title']
						if 'ryoukin' in info:
							attr['ryoukin'] = info['ryoukin']
						concertElement = SubElement(root, 'concert', attr)
						kyokuCollectionElement = SubElement(concertElement , 'kyokuCollection')
						for kyoku in info['kyoku']:
							kyokuElement = SubElement(kyokuCollectionElement, 'kyoku', {'composer': kyoku['composer'], 'title': kyoku['title']})
						playerCollectionElement = SubElement(concertElement , 'playerCollection')
						for player in info['player']:
							playerElement = SubElement(playerCollectionElement, 'player', {'part': player, 'player': info['player'][player]})
						lines = []
				else:
					lines.append(line)

	print("total:%d date:%d kaijou:%d kaien:%d title:%d" % (totalCount, dateCount, kaijouCount, kaienCount, titleCount))

	with open('concertinfo.xml', 'w') as xml:
		rough_string = tostring(root, 'utf-8')
		reparsed = minidom.parseString(rough_string)
		xml.write(reparsed.toprettyxml(indent="  "))

def getTextAllAndOutputFile(master, urls, textfile):
	ns = {'xmlns:c': 'concert',
		'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
		'xsi:schemaLocation': 'concert Concert.xsd'}

	root = Element('c:concertCollection', ns)
	tree = ElementTree(element=root)
	for url in urls:
		try:
			textfile.write('----------------------------------------------' + '\n')
			textfile.write(url['title'] + '\n')
		except Exception as e:
			textfile.write('Output1:' + str(e) + '\n')

		lines = getTextFromOrchestraSite(url, textfile)
		if lines:
			info = scrape1Orchestra(url['title'], lines, master)
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

def loadConcertSchema(filepath):
	master = {}
	tree = ElementTree(file=filepath)
	for item in ('hallName', 'playerName', 'partName', 'composerName'):
		master[item] = []
		for element in tree.findall('xsd:simpleType[@name="%s"]/xsd:restriction/xsd:enumeration' % item, {'xsd': 'http://www.w3.org/2001/XMLSchema'}):
			master[item].append(element.attrib['value'])
	return master
