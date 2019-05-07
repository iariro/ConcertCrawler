import unittest
import sys
sys.path.append('../lib')
import concertcrawler_file

class MyTest(unittest.TestCase):
    def setUp(self):
        self.master = concertcrawler_file.loadConcertSchema(r'../testdata/ConcertSchema.xsd')

    def test_serena201908(self):
        lines = [
			'次回演奏会のご案内',
			'第10回演奏会',
			'2019.8.11(日祝)　午後開催',
			'at 杉並公会堂 大ホール （荻窪駅北口より徒歩7分：地図）',
			'指揮',
			'中田 延亮',
			'ドヴォルザーク：交響曲第9番 ホ短調 op.95「新世界より」　他',
			'トピックス',
			'第9回演奏会は終了いたしました。ご来場いただき、ありがとうございました。（2018.8.20）'
            ]
        info = concertcrawler_file.scrape1Orchestra('オーケストラ・セレーナ', lines, self.master)
        self.assertEqual('第10回演奏会', info.info['title'])
        self.assertEqual('2019/08/11', info.info['date'])
        self.assertEqual('杉並公会堂', info.info['hall'])

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
        info = concertcrawler_file.scrape1Orchestra('帝京大学交響楽団', lines, self.master)
        self.assertEqual("第32回定期演奏会", info.info['title'])
        self.assertEqual("2015/12/28", info.info['date'])
        self.assertEqual("13:30", info.info['kaijou'])
        self.assertEqual("14:00", info.info['kaien'])
        self.assertEqual("オリンパスホール八王子", info.info['hall'])
        self.assertEqual("入場無料", info.info['ryoukin'])

    def test_zennihonika201804(self):
        lines2 = [
            "本文へスキップ",
            "全日本医家管弦楽団　Doctors' Orchestra of Japan",
            "全日本医家管弦楽団",
            "次回演奏会のご案内information",
            "全日本医家管弦楽団 第28回定期演奏会",
            "2018年4月1日（日）午後2時開演",
            "曲目　チャイコフスキー/荘厳序曲「1812年」*",
            "同/バレエ「白鳥の湖」より",
            "ブラームス/交響曲第2番",
            "指揮　曽我 大介合唱　一音入魂合唱団*",
            "東京オペラシティコンサートホール",
            "全席指定：Ｓ席2,500円、Ａ席1,500円",
            "information",
            "●チラシを拡大する",
            "●チラシの裏面を読む",
            "●演奏会・チケットのお問合せ：コンサートイマジン　TEL03-3235-3777",
            "●託児のご案内：イベント託児・マザーズ　TEL0120-788-222",
            "・0歳児から小学生未満までのお子様が対象です。",
            "・託児料の一部として、お子様一人につき2,000円をご負担いただきます。",
            "・受付は公演の1週間前までですが、定員になり次第締切らせていただきます。",
            "●会場へのアクセス",
            "・新宿区西新宿3-20-2　東京オペラシティタワー3階",
            "・京王新線（都営地下鉄新宿線乗り入れ） 初台駅東口下車　徒歩5分以内（直結）",
            "・地下2階に有料駐車場：ホールへお車でご来場のお客様に割引券が発行されます。",
            "このページの先頭へ",
            "contents",
            "UnicodeEncodeError",
            "プロフィールprofile",
            "次回演奏会upcoming concert",
            "今までの活動recent activities",
            "団員募集join us",
            "音楽と医学information",
            "関係リンクlink",
            "バナースペース",
            "フェイスブックblog",
            "全日本医家管弦楽団",
            "連絡先",
            "Dr.muse@nifty.com",
            "UnicodeEncodeError"
        ]
        info = concertcrawler_file.scrape1Orchestra('全日本医家管弦楽団', lines2, self.master)
        self.assertEqual("第28回定期演奏会", info.info['title'])
        self.assertEqual("2018/04/01", info.info['date'])
        self.assertEqual("14:00", info.info['kaien'])
        self.assertEqual("東京オペラシティ", info.info['hall'])
        self.assertEqual("全席指定：Ｓ席2,500円、Ａ席1,500円", info.info['ryoukin'])

    def test_mitaphil201905(self):
        lines = [
            "三田フィルハーモニーオーケストラ",
            "演奏会情報私たちのことこれまでの演奏会団員募集お問い合わせ練習日程",
            "演奏会情報",
            "三田フィルハーモニーオーケストラ第28回定期演奏会2019年5月26日（日）14時開演於：大田区民ホール・アプリコ　大ホール JR京浜東北線 東急多摩川線・池上線「蒲田駅」東口から徒歩約3分京浜急行線 京急「蒲田駅」西口から徒歩約7分指揮：後藤　悠仁【曲目】メンデルスゾーン／交響曲第５番　『宗教改革』　ニ長調　作品107ブラームス／交響曲第２番 ニ長調　作品73入場無料（未就学のお子様の入場はご遠慮頂いております）三田フィルハーモニーオーケストラ第27回定期演奏会＊こちらの演奏会は終了致しました＊たくさんの皆様にご来場いただき誠に有り難うございました。2018年5月4日（金・祝）14時開演於：めぐろパーシモンホール　大ホール（東急東横線【都立大学駅】より徒歩7分）指揮：後藤　悠仁【曲目】シベリウス／交響詩「春の歌」シベリウス／交響曲第７番ベートーヴェン／交響曲第７番入場無料（未就学のお子様の入場はご遠慮頂いております）三田フィルハーモニーオーケストラ",
            "団員と仲間たちによる室内楽ミニ クラシック コンサート",
            "＊こちらの演奏会は終了致しました＊たくさんの皆様にご来場いただき誠に有り難うございました。",
            "2016年9月19日（月祝）",
            "開場：13:30　開演：14:00於：高輪区民センター　区民ホール",
            "(都営三田線・東京メトロ南北線白金高輪駅(1番出口)から直結）",
            "入場無料（未就学のお子様の入場はご遠慮頂いております）",
            "【演奏予定曲目】",
            "ジョヴァンニ・ガブリエーリ / カンツォーナ･ペル･ソナーレ 第２番",
            "ジャック・イベール / 木管五重奏のための３つの小品",
            "ブラームス / ピアノ四重奏曲 第１番より 第１楽章",
            "ブラームス / セレナーデ 第１番 ニ長調 作品１１（九重奏版）より",
            "ドヴォルザーク / 弦楽セレナーデ ホ長調作品２２ より",
            "リヒャルト・シュトラウス / １３管楽器のためのセレナーデ",
            "エルガー / 弦楽セレナーデ　ホ短調 作品２０",
            "Sign in|Report Abuse|Print Page|Powered By Google Sites"
        ]
        info = concertcrawler_file.scrape1Orchestra('三田フィルハーモニーオーケストラ', lines, self.master)
        self.assertEqual("第28回定期演奏会", info.info['title'])
        self.assertEqual("めぐろパーシモン", info.info['hall'])
        self.assertEqual("入場無料", info.info['ryoukin'])

    def test_mozart201805(self):
        lines = [
            "モーツァルト・アンサンブル・オーケストラ",
            "MOZART ENSEMBLE ORCHESTRA Home Page",
            "MEOのページへようこそ !",
            "団員募集中　  弦楽器全パート： (特にCb1名）",
            "モーツァルト・アンサンブル・オーケストラ（MEO）は、ハイドン、モーツァルトのシンフォニーを",
            "レパートリーの中心に据え、指揮者藤原義章氏のリズム論 を実践するために創立された",
            "小編成のオーケストラです。  このサイトではMEOの活動を紹介いたします。",
            "終了した演奏会　たくさんの方のご来場ありがとうございました。",
            "第34回定期演奏会　2018年5月27日(日)　午後２時開演",
            "日時：2018年5月27日（日）午後2時開演（午後1時30分開場）",
            "場所：第一生命ホール",
            "指揮：藤原義章",
            "曲目：J.C.バッハ  　　　シンフォニア 作品18-2",
            "モーツァルト　  　交響曲第31番　ニ長調「パリ」K.297",
            "シベリウス　　　　組曲「ペレアスとメリザンド」作品46",
            "ハイドン　　　　　交響曲第103番　「太鼓連打」 Hob.I:103",
            "甲府演奏会　2017年12月23日(土)　午後4時開演 山梨県立図書館ホール",
            "日時：2017年12月23日（土）午後4時開演 （午後3時30分開場）",
            "場所：山梨県立図書館ホール",
            "指揮：藤原義章",
            "独奏フルート：渡辺 玲子",
            "曲目：J.C.バッハ　　　　シンフォニア 作品18-2　変ロ長調",
            "モーツァルト　  　フルート協奏曲第1番　ト長調　K.313 全曲",
            "ハイドン　　　　　交響曲第103番「太鼓連打」変ホ長調　Hob.I:103より第1・4楽章",
            "モーツァルト　　　交響曲第31番　ニ長調「パリ」 K.297 全曲",
            "これまでの演奏会一覧はこちら",
            "最終更新日2018年11月5日"
        ]
        info = concertcrawler_file.scrape1Orchestra('モーツァルト・アンサンブル・オーケストラ', lines, self.master)
        self.assertEqual("第34回定期演奏会", info.info['title'])
        self.assertEqual("14:00", info.info['kaien'])
        self.assertEqual("13:30", info.info['kaijou'])
        self.assertEqual("第一生命ホール", info.info['hall'])

    def test_funabashijunior201903(self):
        lines = [
            "船橋ジュニアオーケストラ事務局",
            "〒273-0005　千葉県船橋市本町2-2-5",
            "船橋市民文化ホール事務局内",
            "UnicodeEncodeError",
            "＊＊＊19'スプリングコンサートのご案内＊＊＊",
            "平成３１年３月３０日（土）　14：00開演",
            "指揮：江上孝則　　会場：船橋市民文化ホール",
            "曲目　＊序曲「謝肉祭」　　　　　　ドヴォルザーク",
            "＊序曲「１８１２年」　　　　　チャイコフスキー",
            "＊序曲「天国と地獄」　　　オッフェンバック",
            "その他"
            ]
        info = concertcrawler_file.scrape1Orchestra('船橋ジュニアオーケストラ事務局', lines, self.master)
        self.assertEqual("14:00", info.info['kaien'])
        self.assertEqual("2019/03/30", info.info['date'])
        self.assertEqual("船橋市民文化ホール", info.info['hall'])

    def test_tokyogaikokugo201804(self):
        lines = [
            "東京外国語大学管弦楽団",
            "トップ",
            "演奏会情報",
            "次回演奏会情報",
            "過去演奏会情報",
            "演奏会PR掲示板",
            "楽団紹介",
            "当楽団について",
            "年間活動予定",
            "常任指揮者紹介",
            "団員募集",
            "お問い合わせ",
            "リンク",
            "演奏会のご案内",
            "第95回定期演奏会",
            "2018年4月14日(土)",
            "R.ワーグナー/「ニュルンベルクのマイスタージンガー」序曲",
            "P.ヒンデミット/画家マティス",
            "F.メンデルスゾーン/交響曲第五番「宗教改革」",
            "指揮: 清水醍輝",
            "時間：開場　17:15 開演　18:00",
            "場所: 練馬文化センターにて",
            "団員募集中！",
            "急募！Vn. Va. Cb. Ob. Fg. Tp.",
            "練習見学随時歓迎！詳しくは団員募集ページにて。",
            "言語選択",
            "更新履歴 (ログ)",
            "SNS",
            "twitter",
            "facebook",
            "Tweet",
            "twitter",
            "Tweets by tufsorc",
            "サイトマップ",
            "演奏会情報",
            "定期演奏会情報",
            "外語祭公演情報",
            "過去演奏会情報",
            "演奏会PR掲示板",
            "楽団紹介",
            "当楽団について",
            "年間活動予定",
            "常任指揮者紹介",
            "団員募集",
            "お問い合わせ",
            "FAQ",
            "リンク",
            "団員専用",
            "OBOG掲示板",
            "推奨環境",
            "Google Chrome(最新版) 確認済み",
            "スマートフォン & パソコン両対応",
            "HTML5+CSS3+JavaScript",
            "アクセスカウンター",
            "UnicodeEncodeError"
        ]
        info = concertcrawler.scrape1Orchestra('東京外国語大学管弦楽団', lines, self.master)
        self.assertEqual("2018/4/14", info['date'])
        self.assertEqual("17:15", info['kaijou'])
        self.assertEqual("18:00", info['kaien'])
        self.assertEqual("練馬文化センター", info['hall'])

    def test_tokyogaikokugo201804(self):
        lines = [
            "Ensemble ARDORE Home Page",
            "燃えるアンサンブル団体 ～Ensemble ARDORE/アンサンブル・アルドーレ～",
            "Ensemble ARDOREのホームページへようこそ！！",
            "このページは、アマチュアのアンサンブル団体「Ensemble ARDORE」のホームページです。",
            "What's New",
            "・2018/01/07　第13回コンサート情報を掲載しました。",
            "演奏会案内",
            "☆★Ensemble",
            "ARDORE 13th Concert★☆",
            "2018年 10月 27日（土）　13:30開場　14：00開演",
            "かつしかシンフォニーヒルズ　アイリスホール　→アクセス",
            "入場無料　全席自由　（チケットはございません）",
            "＜曲目＞",
            "W.A. モーツァルト　：　フルート四重奏曲第1番 D-Dur K. 285",
            "UnicodeEncodeError",
            "J. シベリウス　：　ヴァイオリンとヴィオラのための二重奏曲 C-Dur",
            "D.ショスタコーヴィチ　：　弦楽四重奏第6番 G-Dur Op.101",
            "A. ピアソラ　：　デカリシモ、オブリヴィオン（忘却）、ロ・ケ・ヴェンドラ（来るべきもの）",
            "HOME",
            "ABOUT US",
            "CONCERT",
            "HISTORY",
            "LINKS",
            "Copyright(C)2009 Ensemble ARDORE All Rights Reserved.",
            "Template design by",
            "Nikukyu-Pundh"
        ]
        info = concertcrawler_file.scrape1Orchestra('Ensemble ARDORE Home Page', lines, self.master)
        self.assertEqual("13:30", info.info['kaijou'])
        self.assertEqual("14:00", info.info['kaien'])
        self.assertEqual("かつしかシンフォニーヒルズ", info.info['hall'])
        self.assertEqual("入場無料", info.info['ryoukin'])

    def test_chuuouku201906(self):
        lines = [
			"第25回定期演奏会",
			" 日時　：　 2019年6月2日（日) 開場・開演時間：未定",
			" 会場　：　 第一生命ホール",
			"　http://www.harumi-triton.jp/access/",
			" 入場料：寄付制（予定）",
			" 指揮　：　 佐藤 雄一（プロフィール紹介）",
			" グリンカ ／歌劇「ルスランとリュドミラ」序曲",
			" チャイコフスキー／幻想序曲「ロミオとジュリエット」",
			" カリンニコフ ／交響曲第1番 ト短調",
        ]
        info = concertcrawler_file.scrape1Orchestra('中央区交響楽団', lines, self.master)
        self.assertEqual("シンフォニーヒルズ", info.info['hall'])
        self.assertEqual("グリンカ ", info.info['kyokumoku'][0][]'composer')
        self.assertEqual("歌劇「ルスランとリュドミラ」序曲", info.info['kyokumoku'][0][]'title')
        self.assertEqual("チャイコフスキー", info.info['kyokumoku'][1][]'composer')
        self.assertEqual("幻想序曲「ロミオとジュリエット」", info.info['kyokumoku'][1][]'title')
        self.assertEqual("カリンニコフ ", info.info['kyokumoku'][2][]'composer')
        self.assertEqual("交響曲第1番 ト短調", info.info['kyokumoku'][2][]'title')

unittest.main()
