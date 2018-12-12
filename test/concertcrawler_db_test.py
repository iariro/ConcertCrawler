import unittest
import sys
sys.path.append('../lib')
import concertcrawler_db

class MyTest(unittest.TestCase):

    def test_getPastOrchestraFromDB(self):
        orchestras = concertcrawler_db.getPastOrchestraFromDB('192.168.10.10')
        self.assertTrue(len(orchestras) > 0)

unittest.main()
