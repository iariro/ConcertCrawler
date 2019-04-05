import unittest
import sys
sys.path.append('../lib')
import concertcrawler_file

from datetime import datetime, timedelta

class MyTest(unittest.TestCase):

	def testZenkakuToHankaku(self):
		self.assertEqual("123", concertcrawler_file.zenkakuToHankaku('１２３'))

	def testGetKaijouFromKaien(self):
		info = concertcrawler_file.ConcertInformation()
		info.set('kaien', "14:00")
		self.assertEqual("13:30", info.getKaijou())

unittest.main()
