# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import json
from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline

class PradoCrawlerPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('tour_data.json', 'ab')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item



class CustomImageNamePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        yield scrapy.Request(item['image_url'], meta={'id' : item['id']})

    def file_path(self, request, response=None, info=None):
        return '%s.jpg' % request.meta['id']