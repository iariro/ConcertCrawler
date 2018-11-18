import concertcrawler

master = concertcrawler.loadConcertSchema('testdata/ConcertSchema.xsd')
concertcrawler.scrapeAllFromFile(master, 'testdata/concertinfo.txt')
