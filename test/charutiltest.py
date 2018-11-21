import unittest
import sys
sys.path.append('..')
import concertcrawler

from datetime import datetime, timedelta

class MyTest(unittest.TestCase):

	def testZenkakuToHankaku(self):
		self.assertEqual("123", concertcrawler.zenkakuToHankaku('１２３'))

	def testGetKaijouFromKaien(self):
		info = concertcrawler.ConcertInformation()
		info.set('kaien', "14:00")
		self.assertEqual("13:30", info.getKaijou())

unittest.main()
