import scrapy
import time
from scraper_api import ScraperAPIClient
from scraperapikey import key
from set_parameters import start_date_value,end_date_value,scrape_all,use_scraper_api
import datetime
client = ScraperAPIClient(key)

class WgSpider(scrapy.Spider):
    name = 'requests'

    scrape_all = scrape_all

    try:
        start_date = list(map(int,start_date_value.split('.')))
        start_date = int(datetime.datetime(start_date[2],start_date[1],start_date[0]).timestamp())
    except:
        start_date = ''

    try:
        end_date = list(map(int,end_date_value.split('.')))
        end_date = int(datetime.datetime(end_date[2],end_date[1],end_date[0]).timestamp())
    except:
        end_date = ''
    
    def start_requests(self):


        #Specify the range
        start = 11
        end = 30

        

        for i in range(start,end):
            if(self.scrape_all == True):
                link = f"https://www.wg-gesucht.de/en/wg-zimmer-in-cityname-gesucht.{i}.0.1.0.html"
            else:
                link = f"https://www.wg-gesucht.de/en/wg-zimmer-in-cityname-gesucht.{i}.0.1.0.html?request_filter=1&city_id={i}&noDeact=1&dFr={self.start_date}&dTo={self.end_date}&categories%5B%5D=0&rent_types%5B%5D=0"
            if(use_scraper_api == True):
                yield scrapy.Request(client.scrapyGet(url=link),callback=self.parse,meta={'id':i})
            else:
                yield scrapy.Request(url=link,callback=self.parse,meta={'id':i})

            

    def parse(self, response):
     
        requests = response.xpath("//*[@id='top_column_wrapper']/div/div[1]/div/h1/text()").get()
        if(requests):
            requests = requests.replace('Requests','').replace('Request','').strip()
            district_name = requests.split(':')[0].replace('Flatshares in','').strip()
            num_of_offers = requests.split(':')[1]
            if(scrape_all == True):
                yield {'start_date': 'All', 'end_date': 'All','city id':response.meta['id'],'district name':district_name,'type':'requests','amount':num_of_offers}
            else:
                yield {'start_date': start_date_value, 'end_date': end_date_value,'city id':response.meta['id'],'district name':district_name,'type':'requests','amount':num_of_offers}


