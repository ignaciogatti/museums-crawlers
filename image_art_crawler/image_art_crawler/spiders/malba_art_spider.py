import scrapy
import re
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from image_art_crawler.items import ImageArtCrawlerItem
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class MalbaArtSpider(CrawlSpider):
    name = "MalbaArt"

    def selenimum_href_extractor(self, url, xpath):
        browser = webdriver.Chrome()
        browser.get(url)
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
        elems = browser.find_elements_by_xpath(xpath)
        urls = [e.get_attribute("href") for e in elems]
        print(urls)
        print(len(urls))
        return urls


    def start_requests(self):

        urls = self.selenimum_href_extractor('http://www.malba.org.ar/coleccion-online/alfabetico/A/', '//a[@class="titulo"]')
        urls_paintings = self.selenimum_href_extractor(urls[0], '//div[@class="container"] a')
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_image)
      

    def parse_image(self, response):
        data_image = {}
        data_image['name'] = response.css('title::text').extract_first()
        #data_image['id'] = response.css('div.numinv span::text').extract_first()
        print(data_image)

