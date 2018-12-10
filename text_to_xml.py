import sys
sys.path.append('lib')
import concertcrawler_file

master = concertcrawler_file.loadConcertSchema(r'../../gol/private/data/concert/ConcertSchema.xsd')
concertcrawler_file.scrapeAllFromFile(master, r'../../gol/private/data/concert/concertinfo.txt')
