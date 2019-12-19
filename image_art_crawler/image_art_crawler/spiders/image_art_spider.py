import scrapy
import re
from image_art_crawler.items import ImageArtCrawlerItem

keys_map={u'G\xe9nero': 'genre', u'Autor': 'author', u'Origen': 'origin', u'Medidas': 'dimmensions', u'Objeto': 'object', 
    u'Estilo': 'style', u'T\xe9cnica': 'technique', u'Soporte': 'support', u'Escuela': 'school'}

keys_map_wiki={u'G\xe9nero': 'genre',  u'Dimensi\xf3nes': 'dimmensions', u'Estilo': 'style', u'Fecha': 'date' }


class ImageArtSpider(scrapy.Spider):
    name = "imageArt"

    def start_requests(self):
        urls = [
            'https://www.wikiart.org/es/honore-daumier/wandering-saltimbanques-1850'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        data_image = {}
        data_image['name'] = response.css('article h3 ::text').extract_first()
        data_image['author'] = response.css('article h5 span a ::text').extract_first()
        data_image['id'] = str(1)

        values = response.css('article li ::text').extract()

        values = [re.sub(r'[\n\t: ]+', '', w) for w in values]

        values = [w for w in values if w !='']

        for key in keys_map_wiki.keys():
            if key in values:
                data_image[ keys_map_wiki[key] ] = values[values.index(key) + 1 ]
        
        image_url = response.css('img').xpath('@src').extract_first()
        print(image_url)
        #image_url = response.urljoin(relative_image_url)
        yield ImageArtCrawlerItem(id= str(1), name=data_image['name'], data=data_image, image_urls=[image_url])

        '''
        data_image['id'] = response.css('div.numinv span::text').extract_first()

        for data in response.css('#data li '):
            values = data.css('::text').re(r'[^\n\t]+')
            if len(values) != 0:
                key = keys_map[re.sub(r'[: ]+', '', values[0])]
                data_image[key] = ' '.join(values[1:])
        #print(data_image)
        relative_image_url = response.css('#image a.hd.non-printable::attr(href)').extract_first()
        image_url = response.urljoin(relative_image_url)
        yield ImageArtCrawlerItem(id= data_image['id'], name=data_image['name'], data=data_image, image_urls=[image_url])    
    '''


        '''
        data_keys = response.css('#data li ::text').re(r'[A-z\u00C0-\u024F0-9]+:')
        #get usefull keys
        data_keys = data_keys[:data_keys.index('Medidas:')+1]
        data_values = response.css('#data li span ::text').re(r'[^\n\t]+')

        for i in range(1, len(data_keys)):
            data_image[data_keys[(-1)*i]] = data_values[(-1)*i]

        data_image[data_keys[0]] = data_values[0]

        
        #author
        data_image['author'] = data[data.index('Autor:')+1]
        #date
        data_image['date'] = data[data.index('Fecha: ')+1]
        #origin
        data_image['origin'] = ''.join(data[data.index('Origen: ')+1:data.index('G')])
        #genre
        data_image['genre'] = ''.join(data[data.index('nero: ')+1:data.index('Escuela: ')])
        #school
        data_image['school'] = ''.join(data[data.index('Escuela: ')+1:data.index('T')])
        #technique
        data_image['technique'] = ''.join(data[data.index('cnica:')+1:data.index('Objeto: ')])
        #Object
        data_image['object'] = ''.join(data[data.index('Objeto: ')+1:data.index('Estilo:')])
        #style
        data_image['style'] = ''.join(data[data.index('Estilo:')+1:data.index('Soporte: ')])
        #support
        data_image['support'] = ''.join(data[data.index('Soporte: ')+1:data.index('Medidas: ')])
        #dimmension
        data_image['dimmension'] = ''.join(data[data.index('Medidas: ')+1:])
        
        print(data_keys)
        print(data_values)
        print(data_image)
        next_page = response.css('#data div.buttons.non-printable a.back').extract()
        print(next_page)
        '''
