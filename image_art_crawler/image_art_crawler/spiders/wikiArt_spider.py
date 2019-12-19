import scrapy
import re
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from image_art_crawler.items import ImageArtCrawlerItem
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
import time

keys_map_wiki={u'G\xe9nero': 'genre',  u'Dimensi\xf3nes': 'dimmensions', u'Estilo': 'style', u'Fecha': 'date' }

class WikiArtSpider(CrawlSpider):
    name = "WikiArt"
    id_incrementer = 0

    def start_requests(self):

        browser = webdriver.Chrome()
        #impressionism
        #browser.get('https://www.wikiart.org/es/paintings-by-style/impresionismo?select=featured#!#filterName:featured,viewType:masonry')
        #cubism
        #browser.get('https://www.wikiart.org/es/paintings-by-style/cubismo?select=featured#!#filterName:featured,viewType:masonry')
        #barroc
        #browser.get('https://www.wikiart.org/es/paintings-by-style/barroco?select=featured#!#filterName:featured,viewType:masonry')
        #abstract
        browser.get('https://www.wikiart.org/es/paintings-by-style/arte-abstracto?select=featured#!#filterName:featured,viewType:masonry')

        PAUSE_TIME = 3
        time.sleep(PAUSE_TIME)
        
        while True:
            try:
                button_next = browser.find_element_by_xpath("//a[@class='masonry-load-more-button']")
                button_next.click()
                # Wait to load page
                time.sleep(PAUSE_TIME)
            except ElementNotVisibleException:
                # Wait to load page
                time.sleep(PAUSE_TIME)
            except NoSuchElementException:
                break    


        urls = browser.find_elements_by_xpath("//div[@class='title-block']/a")
        urls_clear = urls[::2]
        urls_clear = [ url.get_attribute('href') for url in urls_clear]
        for url in urls_clear:
            yield scrapy.Request(url=url, callback=self.parse_image)
      

    def parse_image(self, response):
        data_image = {}

        #id generator
        data_image['id'] = str(WikiArtSpider.id_incrementer)
        WikiArtSpider.id_incrementer = WikiArtSpider.id_incrementer + 1 
        
        data_image['name'] = response.css('article h3 ::text').extract_first()
        data_image['author'] = response.css('article h5 span a ::text').extract_first()

        values = response.css('article li ::text').extract()

        values = [re.sub(r'[\n\t: ]+', '', w) for w in values]

        values = [w for w in values if w !='']

        for key in keys_map_wiki.keys():
            if key in values:
                data_image[ keys_map_wiki[key] ] = values[values.index(key) + 1 ]
        
        image_url = response.css('img').xpath('@src').extract_first()
        print(image_url)
        yield ImageArtCrawlerItem(id= data_image['id'], name=data_image['name'], data=data_image, image_urls=[image_url])