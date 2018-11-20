#!/usr/local/bin/python3

import concertcrawler

urls = concertcrawler.getPastOrchestra()
for url in urls:
	print(url)
