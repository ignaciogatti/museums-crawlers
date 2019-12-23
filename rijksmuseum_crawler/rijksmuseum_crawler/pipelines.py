# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline

class RijksmuseumCrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class CustomImageNamePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        yield scrapy.Request(item['image_url'], meta={'id' : item['id']})

    def file_path(self, request, response=None, info=None):
        return '%s.jpg' % request.meta['id']