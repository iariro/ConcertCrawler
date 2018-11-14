import unittest
import sys
sys.path.append('..')
import concertcrawler

class MyTest(unittest.TestCase):
    def test_mytest_01(self):
        self.assertEqual("123", concertcrawler.zenkakuToHankaku('１２３'))

    def test_teikyou201512(self):
        lines = [
            "帝京大学交響楽団/TEIKYO University Symphony Orchestra",
            "Information",
            "Ｃｏｎｃｅｒｔｓ",
            "第32回定期演奏会",
            "2015年12月28日（月）",
            "オリンパスホール八王子",
            "開場　１3：30　開演　14：00",
            "入場無料",
            "Copyright (C) 2014 TEIKYO University Symphony Orchestra　All Rights Reserved."
            ]
        info = concertcrawler.scrape1Orchestra(lines, None)
        print(info)
        self.assertEqual("第32回定期演奏会", info['title'])
        self.assertEqual("2015/12/28", info['date'])
        self.assertEqual("13：30", info['kaijou'])
        self.assertEqual("14：00", info['kaien'])

unittest.main()
