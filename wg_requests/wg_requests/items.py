# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst,MapCompose
from datetime import datetime,timedelta
import re

def parse_name(name):
    return name.split(',')[0]


class WgRequestsItem(scrapy.Item):

    # url = scrapy.Field(output_processor = TakeFirst())
    city = scrapy.Field(output_processor = TakeFirst())
    district = scrapy.Field(output_processor = TakeFirst())
    start_date = scrapy.Field(output_processor = TakeFirst())
    end_date = scrapy.Field(output_processor = TakeFirst())
    facilities = scrapy.Field(output_processor = TakeFirst())
    size = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor = TakeFirst())
    name = scrapy.Field(output_processor = TakeFirst(),input_processor=MapCompose(parse_name))
    online_for = scrapy.Field(output_processor= TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    price_per_qm = scrapy.Field(output_processor=TakeFirst())
    
