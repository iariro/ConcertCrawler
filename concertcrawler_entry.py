import concertcrawler

master = concertcrawler.loadConcertSchema()
concertcrawler.scrapeAllFromFile(master)
