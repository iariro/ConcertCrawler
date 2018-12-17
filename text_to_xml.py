import sys
sys.path.append('lib')
import concertcrawler_file

master = concertcrawler_file.loadConcertSchema(r'../../FUSIONGOL/private/data/concert/ConcertSchema.xsd')
concertcrawler_file.scrapeAllFromFile(master, r'../../FUSIONGOL/private/data/concert/NewConcert2.txt',  r'../../FUSIONGOL/private/data/concert/NewConcert.xml')
