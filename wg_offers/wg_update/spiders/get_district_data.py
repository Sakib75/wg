import scrapy
import json
import csv
from scraper_api import ScraperAPIClient
from scraperapikey import key

client = ScraperAPIClient(key)

class GetDistrictDataSpider(scrapy.Spider):
    name = 'get_district_data'
    city_code =''
    api = ''
    def start_requests(self):
        url = f'https://www.wg-gesucht.de/en/wg-zimmer-in-cityname.{self.city_code}.0.1.0.html'
        if(self.api == '1'):
            yield scrapy.Request(client.scrapyGet(url=url),callback=self.parse)
        else:
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response):
        options = response.xpath(".//*[@id='offer_filter_form']/div[2]/div[2]/div[2]/div/div/select/option")
        dict_data = {}
        for option in options:
            val = (option.xpath(".//@value").get())
            name = (option.xpath(".//text()").get().strip())
            dict_data[name] = val
        code_file = open(f'./district_codes/district_codes {self.city_code}.json','w',encoding='utf-8')
        json.dump(dict_data,code_file,ensure_ascii=False)
        code_file.close()

        

