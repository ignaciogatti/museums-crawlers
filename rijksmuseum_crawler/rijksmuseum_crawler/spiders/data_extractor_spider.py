import scrapy
import re
from scrapy.spiders import CrawlSpider
from rijksmuseum_crawler.items import RijksmuseumCrawlerItem
import unicodedata


class DataExtractorSpider(CrawlSpider):
    name = "dataExtractorSpider"

#    start_urls = ['https://www.rijksmuseum.nl/en/tour/9c051b0a-4dba-4c7d-9bd6-960cdfc749d1']


    def normalize_title(self, title):
        return unicodedata.normalize('NFKD', title.lower()).encode('ASCII', 'ignore').decode('utf8')


    def clean_data(self, data):
        return re.sub(r'\n\s+', '', data)


    def get_metadata(self, data):
        data_clean = self.clean_data(data)
        data_clean = self.normalize_title(data_clean)
        artwork_data = data_clean.split(', ')

        #id
        id = artwork_data[0].split('.')[0]
        #Clean id
        artwork_data[0] = artwork_data[0].split('. ')[-1]

        #No artist
        if len(artwork_data) == 2:
            artwork_data.insert(0, 'None')

        #artist
        artist = self.clean_data(artwork_data[0])
        del(artwork_data[0])

        #data
        data = self.clean_data(artwork_data[-1])
        del(artwork_data[-1])

        #title
        title = ''
        #title with 'comas'
        if len(artwork_data) > 1 :
            title = ' '.join(artwork_data)
        else:
            title = artwork_data[0]
        title = self.clean_data(title)

        return {
            'id': id,
            'artist': artist, 
            'data' : data,
            'title': title
            }



    def parse(self, response):
        
        #Get images_urls
        images_urls = response.css('li.column img').xpath('@data-srcset').getall()
        images_urls_clean = []

        for url in images_urls:
            #Get the url with the greatest image
            url_clean = url.split(',')[-1]
            url_clean = url_clean.split(' ')[0]
            images_urls_clean.append(url_clean)

        #Get image metadata
        #Get the url with the greatest image
        metadata = response.css('li.column h4.header-small::text').getall()

        index = 0
        for data in metadata:
            data_clean = self.get_metadata(data)

            image_url = images_urls_clean[index]
            index +=1
            #check url start with https:
            if not image_url.startswith('https:'):
                image_url = 'https:' + image_url
            yield RijksmuseumCrawlerItem(
                id=data_clean['id'], 
                author=data_clean['artist'], 
                title=data_clean['title'], 
                data=data_clean['data'], 
                image_url=image_url)




class DataVisitorExtractorSpider(DataExtractorSpider):
    name = "dataVisitorExtractorSpider"

#    start_urls = ['https://www.rijksmuseum.nl/en/rijksstudio/213416--patty-struik/route/fashion-details']

    artwork_id = 1

    def get_metadata(self, data):
        data_clean = self.clean_data(data)
        data_clean = self.normalize_title(data_clean)
        artwork_data = data_clean.split(', ')

        #id
        id = str(self.artwork_id)
        self.artwork_id += 1 

        #data
        data = self.clean_data(artwork_data[-1])
        del(artwork_data[-1])
        
        #No artist
        artist = ''
        if len(artwork_data) < 2:
            artist = 'None'
        else:
            artist = self.clean_data(artwork_data[-1])
            del(artwork_data[-1])

        #title
        title = ''
        #title with 'comas'
        if len(artwork_data) > 1 :
            title = ' '.join(artwork_data)
        else:
            title = artwork_data[0]
        title = self.clean_data(title)

        return {
            'id': id,
            'artist': artist, 
            'data' : data,
            'title': title
            }

