#!/usr/local/bin/python3

import concertcrawler

master = concertcrawler.loadConcertSchema('testdata/ConcertSchema.xsd')
urls = concertcrawler.getPastOrchestra()
with open('concertinfo.txt', 'w') as file:
	concertcrawler.getTextAllAndOutputFile(master, urls, file)
