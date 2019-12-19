import scrapy
import re
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from image_art_crawler.items import ImageArtCrawlerItem
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

keys_map={u'G\xe9nero': 'genre', u'Autor': 'author', u'Origen': 'origin', u'Medidas': 'dimmensions', u'Objeto': 'object', 
    u'Estilo': 'style', u'T\xe9cnica': 'technique', u'Soporte': 'support', u'Escuela': 'school', u'Fecha':'date'}

class LinkArtSpider(CrawlSpider):
    name = "linkArt"

    def start_requests(self):
        browser = webdriver.Chrome()
        browser.get('http://www.bellasartes.gob.ar/coleccion/obras')
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
            yield scrapy.Request(url=url, callback=self.parse_image)
      

    def parse_image(self, response):
        data_image = {}
        data_image['name'] = response.css('#data h1::text').extract_first()
        data_image['id'] = response.css('div.numinv span::text').extract_first()

        for data in response.css('#data li '):
            values = data.css('::text').re(r'[^\n\t]+')
            if (len(values) != 0) and (re.sub(r'[: ]+', '', values[0]) in keys_map.keys()):
                key = keys_map[re.sub(r'[: ]+', '', values[0])]
                data_image[key] = ' '.join(values[1:])
        #print(data_image)
        relative_image_url = response.css('#image a.hd.non-printable::attr(href)').extract_first()
        image_url = response.urljoin(relative_image_url)
        yield ImageArtCrawlerItem(id= data_image['id'], name=data_image['name'], data=data_image, image_urls=[image_url])  
#        print(response.css('div.buttons.non-printable a.btn.next ::attr(href)').extract())
        


