import scrapy
import re
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from prado_crawler.items import PradoCrawlerItem
import unicodedata

class TourDataSpider(CrawlSpider):
    name = "tourDataSpider"

    def normalize_title(self, title):
        return unicodedata.normalize('NFKD', title.lower()).encode('ASCII', 'ignore').decode('utf8')

    def clean_data(self, data):
        return re.sub(r'\n\s+', '', data)
    
    
    def parse(self, response):
        urls = []
        #Look for all artworks urls
        for link in LxmlLinkExtractor(allow='https://www.museodelprado.es/en/the-collection/art-work/' , restrict_css='div.vista-muro.mostrable' ).extract_links(response):
            urls.append(link.url)

        index =0 
        for url in urls:
            index +=1
            yield scrapy.Request(url=url, callback=self.parse_data, cb_kwargs=dict(id=index))
                

    def parse_data(self, response, id):

        #author
        author = self.normalize_title( response.css('div.metadata div.author::text').get() )

        #title
        title = self.normalize_title( response.css('div.metadata div.artwork-name::text').get() )

        #data
        data = self.normalize_title( response.css('div.obra strong::text').get() )
        #clean extra whitespace
        data = self.clean_data(data)

        #image url
        image_url = response.css('div.imagenes a img').xpath('@src').extract_first()

        #save artwork data
        yield PradoCrawlerItem(id=id, author=author, title=title, data=data, image_url=image_url)


