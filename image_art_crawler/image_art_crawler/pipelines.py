# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import sqlite3
import re

class ImageArtCrawlerPipeline(object):

    def __init__(self):
        self.setup_db_con()
        self.create_table()
    
    def setup_db_con(self):
        self.con = sqlite3.connect('/home/ignacio/image_metadata.db')
        self.cur = self.con.cursor()
    
    def create_table(self):
        self.cur.execute('''create table if not exists image_data(
            id varchar(10) primary key not null,
            name text not null,
            author text,
            date char(30),
            origin text,
            genre varchar(100), 
            school char(30),
            technique varchar(100),
            object char(50),
            style text,
            support text,
            dimmensions text
        );
        ''')

    def closeDB(self):
        self.con.close()
    
    def __del__(self):
        self.closeDB()
    
    def store_data(self, item):
        data_image = item.get('data')
        if 'dimmensions' in data_image.keys():
            data_image['dimmensions'] = data_image['dimmensions'].replace(',','.')
        print('reading data...')
        columns = ', '.join(data_image.keys())
        values = data_image.values()
        incognites = [ '?' for x in values]
        values = [ re.sub(r'[,\-\(\)\?]', '', x) for x in values ]
        values = tuple(values)
        incognites = ', '.join(incognites)
        query = 'INSERT INTO  image_data('+columns +') VALUES('+incognites+')'

        self.cur.execute(query, values)
        print('storing data')
        self.con.commit()


    def process_item(self, item, spider):
        self.store_data(item)
        return item


class ImpressionismCrawlerPipeline(ImageArtCrawlerPipeline):


    def setup_db_con(self):
        self.con = sqlite3.connect('/home/ignacio/abstract.db')
        self.cur = self.con.cursor()
    
    def create_table(self):
        self.cur.execute('''create table if not exists image_data(
            id varchar(10) primary key not null,
            name text not null,
            author text,
            date char(30),
            genre varchar(100),
            style text,
            dimmensions text
        );
        ''')


class CustomImageNamePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url, meta={'id' : item['id']})

    def file_path(self, request, response=None, info=None):
        return '%s.jpg' % request.meta['id']