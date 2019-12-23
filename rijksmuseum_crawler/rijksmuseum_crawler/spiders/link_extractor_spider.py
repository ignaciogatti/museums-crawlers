import scrapy
import re
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from rijksmuseum_crawler.items import UrlsTourItem


class LinkExtractorSpider(CrawlSpider):

    name = "linkExtractorSpider"

    start_urls = ['https://www.rijksmuseum.nl/en/tours']

    def parse(self, response):
        urls_highlights_tours = []
        #Look for all highlights tours urls
        for link in LxmlLinkExtractor(allow=['/en/tour/'], restrict_css=['div.mini-page.slideshow-em-wrapper', 'div#rijksmuseum-app'] ).extract_links(response):
            urls_highlights_tours.append(link.url)
        
        urls_visitor_tours = []
        #Look for all visitor tour urls
        for link in LxmlLinkExtractor(allow=['/en/rijksstudio/'], restrict_css=['div#rijksmuseum-app'] ).extract_links(response):
            urls_visitor_tours.append(link.url)

        urls_visitor_tours = list(filter(lambda x : x.find('/route') != -1, urls_visitor_tours ))

        yield UrlsTourItem(highlight_tours=urls_highlights_tours, visitor_tours=urls_visitor_tours)