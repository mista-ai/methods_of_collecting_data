# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Compose
from twisted.web.html import output

def process_price(value):
    money = 0
    currency = ''
    if value:
        money = int(value[0].replace(' ', ''))
        currency = value[1]
    return {'money': money, 'currency': currency}

def process_name(value):
    return value[0].strip()

class CastoramaParserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field(input_processor=Compose(process_name), output_processor=TakeFirst())
    price = scrapy.Field(input_processor=Compose(process_price), output_processor=TakeFirst())
    photos = scrapy.Field()
    characteristics = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
