import sys
sys.path.append('lib')
import concertcrawler_file

master = concertcrawler.loadConcertSchema('testdata/ConcertSchema.xsd')
concertcrawler.scrapeAllFromFile(master, 'testdata/concertinfo.txt')
