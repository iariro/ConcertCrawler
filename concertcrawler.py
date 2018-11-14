#!/usr/bin/python

import re
import urllib
import urllib.parse
import urllib.request as urllib2
import xml.etree.ElementTree as ET
#from bs4 import BeautifulSoup

def getPastOrchestra():
    urls = []
    
    url = 'http://www2.gol.com/users/ip0601170243/private/web/concert/pastorchestra.htm'
    ua = 'concertcrawler'

    req = urllib.request.Request(url, headers={'User-Agent':ua})
    html = urllib.request.urlopen(req)
    soup = BeautifulSoup(html, "html.parser")

    for url in soup.find_all('a'):
        urls.append({'title':url.get_text().strip(), 'url':url.get('href')})
    return urls

def getTextFromOrchestraSite(url, file):
    req = urllib.request.Request(url['url'], headers={'User-Agent': 'concertcrawler'})
    try:
        file.write('----------------------------------------------' + '\n')
        file.write(url['title'] + '\n')

        html = urllib.request.urlopen(req)
        soup = BeautifulSoup(html, "html.parser")

        [s.extract() for s in soup('style')]
        [s.extract() for s in soup('script')]

        lines = []
        for line in soup.text.split('\n'):
            line = line.strip()
            if len(line) > 0:
                lines.append(line)
                try:
                    file.write(line + '\n')
                except UnicodeEncodeError:
                    file.write('UnicodeEncodeError\n')
        return lines
    except Exception:
        file.write('Exception\n')

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

    hankaku = ""
    for c in zenkaku:
        if c in digitMap:
            hankaku += digitMap[c]
        else:
            hankaku += c
    return hankaku

def scrape1Orchestra(lines, master):
    info = {}
    for line in lines:
        date11 = re.search('（*([0-9]*) *年）* *([0-9]*) *月 *([0-9]*) *日', line)
        date12 = re.search('（*([０-９]*) *年）* *([０-９]*) *月 *([０-９]*) *日', line)
        date2 = re.search('平成([０-９]*)年([０-９]*)月([０-９]*)日', line)
        date31 = re.search('([0-9]{2})/([0-9]*)/([0-9]*)', line)
        date32 = re.search('([0-9]{4})/([0-9]*)/([0-9]*)', line)
        date4 = re.search('([0-9]{4})\.([0-9]*)\.([0-9]*)', line)
        date5 = re.search('([0-9]{4})-([0-9]*)-([0-9]*)', line)

        kaijou1 = re.search('([0-9０-９]*[:：][0-9０-９]*)開場', line)
        kaijou2 = re.search('開場　*([0-9０-９]*[:：][0-9０-９]*)', line)
        kaien1 = re.search('([0-9０-９]*[:：][0-9０-９]*)開演', line)
        kaien2 = re.search('開演　*([0-9０-９]*[:：][0-9０-９]*)', line)

        titles = []
        titles.append(re.search('(第.*回 *演奏会)', line))
        titles.append(re.search('(第.*回 *公演)', line))
        titles.append(re.search('(第.*回定期公演)', line))
        titles.append(re.search('(第.*回定期演奏会)', line))
        titles.append(re.search('(第.*回特別演奏会)', line))
        titles.append(re.search('(第.*回.*コンサート)', line))
        titles.append(re.search('(.*特別演奏会)', line))
        titles.append(re.search('(.*[^ ]* Concert)', line))

        if date11:
            info['date'] = "%s/%s/%s" % (date11.group(1), date11.group(2), date11.group(3))
        elif date12:
            year = zenkakuToHankaku(date12.group(1))
            month = zenkakuToHankaku(date12.group(2))
            day = zenkakuToHankaku(date12.group(3))
            info['date'] = "%s/%s/%s" % (year, month, day)
        elif date2:
            year = int(zenkakuToHankaku(date2.group(1))) + 1988
            month = int(zenkakuToHankaku(date2.group(2)))
            day = int(zenkakuToHankaku(date2.group(3)))
            info['date'] = "%s/%s/%s" % (year, month, day)
        elif date31:
            year = int(zenkakuToHankaku(date31.group(1))) + 2000
            month = int(zenkakuToHankaku(date31.group(2)))
            day = int(zenkakuToHankaku(date31.group(3)))
            info['date'] = "%s/%s/%s" % (year, month, day)
        elif date32:
            info['date'] = "%s/%s/%s" % (date32.group(1), date32.group(2), date32.group(3))
        elif date4:
            info['date'] = "%s/%s/%s" % (date4.group(1), date4.group(2), date4.group(3))
        elif date5:
            info['date'] = "%s/%s/%s" % (date5.group(1), date5.group(2), date5.group(3))

        if kaijou1:
            info['kaijou'] = zenkakuToHankaku(kaijou1.group(1))
        elif kaijou2:
            info['kaijou'] = zenkakuToHankaku(kaijou2.group(1))

        if kaien1:
            info['kaien'] = zenkakuToHankaku(kaien1.group(1))
        elif kaien2:
            info['kaien'] = zenkakuToHankaku(kaien2.group(1))

        for title in titles:
            if title:
                info['title'] = title.group(1)
                break
    return info

def scrapeAllFromFile(master):
    totalCount = 0
    dateCount = 0
    titleCount = 0
    kaijouCount = 0
    kaienCount = 0
    with open('concertinfo.txt') as file:
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
                        info = scrape1Orchestra(lines, master)
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
                        lines = []
                else:
                    lines.append(line)

    print("total:%d date:%d kaijou:%d kaien:%d title:%d" % (totalCount, dateCount, kaijouCount, kaienCount, titleCount))

def getTextAllAndOutputFile():
    urls = getPastOrchestra()
    with open('concertinfo.txt', 'w') as file:
        for url in urls:
            print(url)
            lines = getTextFromOrchestraSite(url, file)

            for line in lines:
                try:
                    file.write(line + '\n')
                except UnicodeEncodeError:
                    file.write('UnicodeEncodeError\n')

def loadConcertSchema():
    master = {}
    tree = ET.ElementTree(file='ConcertSchema.xsd')
    for item in ('hallName', 'playerName', 'partName', 'composerName'):
        master[item] = []
        for element in tree.findall('xsd:simpleType[@name="%s"]/xsd:restriction/xsd:enumeration' % item, {'xsd': 'http://www.w3.org/2001/XMLSchema'}):
            master[item].append(element.attrib['value'])
    return master
