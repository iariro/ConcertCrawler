import unittest
import sys
sys.path.append('../lib')
import concertcrawler_db

class MyTest(unittest.TestCase):

    def test_getPastOrchestraFromDB_HTTP(self):
        orchestras = concertcrawler_db.getPastOrchestraFromDB_HTTP('192.168.10.10')
        print(orchestras)
        self.assertTrue(len(orchestras) > 0)

    #def test_getPastOrchestraFromDB(self):
        #orchestras = concertcrawler_db.getPastOrchestraFromDB('192.168.10.10')
        #self.assertTrue(len(orchestras) > 0)

unittest.main()
