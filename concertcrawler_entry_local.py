#!/usr/local/bin/python3

import concertcrawler

master = concertcrawler.loadConcertSchema('testdata/ConcertSchema.xsd')
urls = concertcrawler.getPastOrchestra()
concertcrawler.scrapeAllFromFile(master, 'testdata/concertinfo.txt')
