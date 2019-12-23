import sys
import scrapy
from scrapy.crawler import CrawlerProcess
from rijksmuseum_crawler.spiders.link_extractor_spider import LinkExtractorSpider 
import re
import os
import json
import subprocess


BASE_PATH = '/home/ignacio/Devel/crawler/rijksmuseum_crawler/'

url = 'https://www.rijksmuseum.nl/en/tours'


process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': os.path.join(BASE_PATH, 'urls.json'),
    })

process.crawl(LinkExtractorSpider, start_urls=[url])
process.start()

with open(os.path.join(BASE_PATH, 'urls.json')) as json_file:
    urls = json.load(json_file)
    urls = urls[0]


process_path = os.path.join(os.getcwd(), 'crawler_process.py')
print(process_path)

index = 0
for url in urls['highlight_tours']:

    subprocess.run("python " + process_path + " " + str(index) + " " + "0" + " " +url, shell=True  )
    index += 1

for url in urls['visitor_tours']:

    subprocess.run("python " + process_path + " " + str(index) + " " + "1" + " " +url, shell=True  )
    index += 1