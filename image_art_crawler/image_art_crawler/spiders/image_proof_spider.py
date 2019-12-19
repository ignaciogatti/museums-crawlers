import scrapy
import json
import re
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class LinkProofArtSpider(CrawlSpider):
    name = "imageProofArt"

    def start_requests(self):
        browser = webdriver.Chrome()
        browser.get('http://www.bellasartes.gob.ar/coleccion/escuela/argentina-s.xix')
        SCROLL_PAUSE_TIME = 2

        # Get scroll height
        last_height = browser.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            # Calculate new scroll height and compare with last scroll height
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        elems = browser.find_elements_by_xpath('//div[@class="obras"]//a')
        urls = [e.get_attribute("href") for e in elems]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):

        print(response.css('#data h1::text').extract_first())
        