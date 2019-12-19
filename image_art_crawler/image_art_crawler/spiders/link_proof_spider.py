import scrapy
import re
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor


class LinkProofArtSpider(CrawlSpider):
    name = "linkProofArt"

    def start_requests(self):
        queries =['antonio+berni','pridiliano+pueyrredon']
        urls = [
            'https://www.bellasartes.gob.ar/coleccion/buscar?q='
        ]
        for url in urls:
            for q in queries:
                yield scrapy.Request(url=url+q, callback=self.parse)


    def parse(self, response):
        for link in LxmlLinkExtractor(allow=r'https://www.bellasartes.gob.ar/coleccion/obra/.+', restrict_xpaths='//div[@class="obra card"]').extract_links(response):
            print(link)
        