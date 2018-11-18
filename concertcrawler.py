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

class ConcertInformation:
    def __init__(self):
        self.info = {}
        self.info['kyoku'] = []
        self.info['player'] = {}

    def set(self, key, value):
        if key not in self.info:
            self.info[key] = value

    def get(self, key):
        return self.info[key]

def scrape1Orchestra(lines, master):
    info = ConcertInformation()
    for line in lines:
        date11 = re.search('（*([0-9]{4}) *年）* *([0-9]*) *月 *([0-9]*) *日', line)
        date12 = re.search('（*([０-９]{4}) *年）* *([０-９]*) *月 *([０-９]*) *日', line)
        date2 = re.search('平成([０-９]*)年([０-９]*)月([０-９]*)日', line)
        date31 = re.search('([0-9]{2})/([0-9]*)/([0-9]{1-2})', line)
        date32 = re.search('([0-9]{4})/([0-9]{1-2})/([0-9]{1-2})', line)
        date4 = re.search('([0-9]{4})\.([0-9]{1-2})\.([0-9]{1-2})', line)
        date5 = re.search('([0-9]{4})-([0-9]{1-2})-([0-9]{1-2})', line)

        if date11:
            info.set('date', "%s/%s/%s" % (date11.group(1), date11.group(2), date11.group(3)))
        elif date12:
            year = zenkakuToHankaku(date12.group(1))
            month = zenkakuToHankaku(date12.group(2))
            day = zenkakuToHankaku(date12.group(3))
            info.set('date', "%s/%s/%s" % (year, month, day))
        elif date2:
            year = int(zenkakuToHankaku(date2.group(1))) + 1988
            month = int(zenkakuToHankaku(date2.group(2)))
            day = int(zenkakuToHankaku(date2.group(3)))
            info.set('date', "%s/%s/%s" % (year, month, day))
        elif date31:
            year = int(zenkakuToHankaku(date31.group(1))) + 2000
            month = int(zenkakuToHankaku(date31.group(2)))
            day = int(zenkakuToHankaku(date31.group(3)))
            info.set('date', "%s/%s/%s" % (year, month, day))
        elif date32:
            info.set('date', "%s/%s/%s" % (date32.group(1), date32.group(2), date32.group(3)))
        elif date4:
            info.set('date', "%s/%s/%s" % (date4.group(1), date4.group(2), date4.group(3)))
        elif date5:
            info.set('date', "%s/%s/%s" % (date5.group(1), date5.group(2), date5.group(3)))

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
                kyokumoku1 = re.search(composer + "[  ]*[:：/／][  ]*(.*)", line)
                kyokumoku2 = re.search("(.*)[  ]*[:：/／][  ]" + composer, line)

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

        conductor = re.search("指揮[  :：](.*)", line)
        if conductor:
            info.info['player']['指揮'] = conductor.group(1)

    return info.info

def scrapeAllFromFile(master, concertinfofilepath):
    totalCount = 0
    dateCount = 0
    titleCount = 0
    kaijouCount = 0
    kaienCount = 0
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
    with open('testdata\\concertinfo.txt', 'w') as file:
        for url in urls:
            print(url)
            lines = getTextFromOrchestraSite(url, file)

            for line in lines:
                try:
                    file.write(line + '\n')
                except UnicodeEncodeError:
                    file.write('UnicodeEncodeError\n')

def loadConcertSchema(filepath):
    master = {}
    tree = ET.ElementTree(file=filepath)
    for item in ('hallName', 'playerName', 'partName', 'composerName'):
        master[item] = []
        for element in tree.findall('xsd:simpleType[@name="%s"]/xsd:restriction/xsd:enumeration' % item, {'xsd': 'http://www.w3.org/2001/XMLSchema'}):
            master[item].append(element.attrib['value'])
    return master
