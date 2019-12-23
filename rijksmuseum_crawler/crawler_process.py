import sys
import scrapy
from scrapy.crawler import CrawlerProcess
from rijksmuseum_crawler.spiders.data_extractor_spider import DataExtractorSpider, DataVisitorExtractorSpider
import re
import os

BASE_PATH = '/home/ignacio/Devel/crawler/rijksmuseum_crawler/image_sequence'

#Get args
cmdargs = str(sys.argv)
#Clean args
args = cmdargs.split(',')
index = int(re.sub(r'[\s \']+', '', args[1]))
spider_selector = int(re.sub(r'[\s \']+', '', args[2]))
url = re.sub(r'[\s \'\]]+', '', args[3])


#Create folder to save tour
tour_path = os.path.join(BASE_PATH, 'tour_' + str(index))
os.makedirs(tour_path)
image_path = os.path.join(tour_path, 'images')
os.makedirs(image_path)

process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': os.path.join(tour_path, 'items.json'),
        'IMAGES_STORE': image_path,
        'ITEM_PIPELINES' : {
            'rijksmuseum_crawler.pipelines.CustomImageNamePipeline': 1
            }
    })

if spider_selector == 0: 
    process.crawl(DataExtractorSpider, start_urls=[url])
else:
    process.crawl(DataVisitorExtractorSpider, start_urls=[url])

process.start()
