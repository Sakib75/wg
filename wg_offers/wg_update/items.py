# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst,MapCompose
from datetime import datetime,timedelta
import re



class WgUpdateItem(scrapy.Item):
    city = scrapy.Field(output_processor = TakeFirst())
    district = scrapy.Field(output_processor = TakeFirst())
    address = scrapy.Field(output_processor = TakeFirst())
    postal_code = scrapy.Field(output_processor= TakeFirst())
    # location = scrapy.Field(output_processor = TakeFirst(),input_processor=MapCompose(location_parser))
    start_date = scrapy.Field(output_processor = TakeFirst())
    end_date = scrapy.Field(output_processor = TakeFirst())
    title = scrapy.Field(output_processor = TakeFirst(),input_processor=MapCompose(str.strip))
    furnished = scrapy.Field(output_processor = TakeFirst())
    size = scrapy.Field(output_processor = TakeFirst())
    url = scrapy.Field(output_processor = TakeFirst())
    miscellaneous_cost = scrapy.Field(output_processor = TakeFirst())
    utilities_cost = scrapy.Field(output_processor = TakeFirst())
    rent = scrapy.Field(output_processor = TakeFirst())
    price = scrapy.Field(output_processor = TakeFirst())
    owner = scrapy.Field(output_processor = TakeFirst())
    online_for = scrapy.Field(output_processor = TakeFirst())
    price_per_qm = scrapy.Field(output_processor = TakeFirst())
    base_rent = scrapy.Field(output_processor = TakeFirst())
    address = scrapy.Field(output_processor = TakeFirst())
