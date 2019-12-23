# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class RijksmuseumCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    id = Field()
    title = Field()
    author = Field()
    data = Field()
    image_url = Field()
    

class UrlsTourItem(scrapy.Item):
    highlight_tours = Field()
    visitor_tours = Field()