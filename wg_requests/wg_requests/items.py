# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst,MapCompose
import datetime
import re

def parse_name(name):
    return name.split(',')[0]

def get_timing(date):
    now = datetime.datetime.now()
    try:
        if(date.endswith('day') or date.endswith('days')):
            timing = now - datetime.timedelta(days = int(date.split()[0]))
        elif(date.endswith('hour') or date.endswith('hours')):
            timing = now - datetime.timedelta(hours = int(date.split()[0]))
        elif(date.endswith('minute') or date.endswith('minutes')):
            timing = now - datetime.timedelta(minutes = int(date.split()[0]))
        else:
            timing = datetime.datetime.strptime(date, "%d.%m.%Y")
        date_string = timing.strftime("%d.%m.%Y")
    except:
        date_string = 'n.a'

    date_string = timing.strftime("%d.%m.%Y")
    return date_string

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
    online_for = scrapy.Field(output_processor= TakeFirst(),input_processor=MapCompose(get_timing))
    url = scrapy.Field(output_processor=TakeFirst())
    price_per_qm = scrapy.Field(output_processor=TakeFirst())
    
