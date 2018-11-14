import unittest
import sys
sys.path.append('..')
import concertcrawler

class MyTest(unittest.TestCase):
    def test_mytest_01(self):
        self.assertEqual("123", concertcrawler.zenkakuToHankaku('１２３'))

unittest.main()
