import scrapy
from http.cookies import SimpleCookie
from ..items import WgRequestsItem
from scrapy.loader import ItemLoader
import re
from scraper_api import ScraperAPIClient
from scraperapikey import key
import json

client = ScraperAPIClient(key)

class WgSpider(scrapy.Spider):
    name = 'wg'
    cookies1={}
    ot,date_from,date_to,fur,city_id,district_name,start_date_value,end_date_value,api = '','','','','','','','',''
    header = {}

    def start_requests(self):
        rawdata = f" last_city={self.city_id}; last_cat=0; last_type=0"
        cookie = SimpleCookie()
        cookie.load(rawdata)        
        for key,morsel in cookie.items():
            self.cookies1[key] = morsel.value
        url = f"https://www.wg-gesucht.de/en/wg-zimmer-in-Berlin-gesucht.{self.city_id}.0.1.0.html?request_filter=1&city_id={self.city_id}&noDeact=1&dFr={self.date_from}&dTo={self.date_to}&categories%5B%5D=0&rent_types%5B%5D=0&ot%5B%5D={self.ot}" 
        if(self.api == '1'):
            yield scrapy.Request(client.scrapyGet(url=url), callback=self.parse,cookies=self.cookies1,dont_filter=True,meta={"handle_httpstatus_list": [302,500,502]})
        else:
            yield scrapy.Request(url, callback=self.parse,cookies=self.cookies1,dont_filter=True,meta={"handle_httpstatus_list": [302,500,502]})
    

    def parse(self, response):
            last_page = response.xpath('//nav/ul/li/a/text()').getall()
            try:
                last_page_no =int(last_page[-3].strip()) 
            except:
                last_page_no = 1
            print(f'Last Page No: {last_page_no}')

            for i in range(0,last_page_no):
                if(i == 0):             
                    yield scrapy.Request(url=response.request.url,callback=self.parse_2,dont_filter=True,meta={'dont_redirect': True,"handle_httpstatus_list": [302,500,502]})
                else:           
                    url = f"https://www.wg-gesucht.de/en/wg-zimmer-in-Berlin-gesucht.{self.city_id}.0.1.{i}.html?category=0&city_id={self.city_id}&rent_type=0&noDeact=1&dFr={self.date_from}&dTo={self.date_to}&ot={self.ot}&img=1&rent_types%5B0%5D=0"
                    if(self.api == '1'):
                        yield scrapy.Request(client.scrapyGet(url=url),cookies=self.cookies1,callback=self.parse_2,meta={"handle_httpstatus_list": [302,500,502]})
                    else:
                        yield scrapy.Request(url,cookies=self.cookies1,callback=self.parse_2,meta={"handle_httpstatus_list": [302,500,502]})
        
    def parse_2(self,response):

        items = response.xpath("//div[@class='col-sm-8 card_body']")
        
        #City Name
        try:
            city_name = response.xpath("//*[@id='top_column_wrapper']/div/div[1]/div/h1/text()").get().split(':')[0].replace('Flatshares in','').strip()
        except:
            city_name = 'n.a'
        
        
        for item in items:
            price = item.xpath(".//div[2]/div/b/text()").get()
            if(not price):
                price = 'n.a'
            if(price != 'from'):

                #Size
                size = item.xpath(".//div[2]/div[3]/b/text()").get()
                if(not size):
                    size = 'n.a'

                #Name
                name = item.xpath("./div[3]/div[2]/div[2]/div/span[1]/text()").get()
                if(not name):
                    name = 'n.a'   
                
                #Online For
                try:
                    online_for = item.xpath("..//div[3]/div[2]/div[2]/div/span[2]/text()").get().replace("Online:",'').strip()
                except:
                    online_for = 'n.a'

                #District Name
                if(self.district_name != 'any'):
                    district_name = self.district_name
                else:
                    try:
                        district_name = " ".join(item.xpath("./div[1]/div[2]/span/text()").get().split()).split('|')[1].strip()
                        district_name = district_name.replace(city_name,'',1).strip()
                        district_name = district_name.replace('(','').replace(')','')
                    except:
                        pass
                    if(not district_name):
                        district_code_file = open(f'./district_codes/district_codes {self.city_id}.json',encoding='utf-8')
                        data = json.load(district_code_file)
                        all_districts = []
                        for key in data.keys():
                            if(not key[0].isdigit() and key != 'Any'):
                                all_districts.append(key)
                        all_districts = ','.join(all_districts)
                        if(len(all_districts)):
                            district_name = all_districts
                        else:
                            district_name = city_name
                

                # Price
                price = item.xpath(".//div[2]/div/b/text()").get()
                if(not price):
                    price = 'n.a'

                #Price Per QM
                try:
                    price_per_qm = int(price.replace(' €',''))/int(size.replace(' m²',''))
                except:
                    price_per_qm = 'n.a'

                

                #URL
                next_page_url = "https://www.wg-gesucht.de/en/" + item.xpath(".//h3/a/@href").get()
                if(not next_page_url):
                    next_page_url = 'n.a'
                

                if(self.api == '1'):
                    yield scrapy.Request(client.scrapyGet(url=next_page_url),callback=self.parse_3,meta={"handle_httpstatus_list": [302],'next_page_url':next_page_url,'name':name,'city':city_name,'district':district_name,'price':price,'size':size,'price_per_qm':price_per_qm,'online_for':online_for})
                else:
                    yield scrapy.Request(url=next_page_url,callback=self.parse_3,meta={"handle_httpstatus_list": [302],'next_page_url':next_page_url,'name':name,'city':city_name,'district':district_name,'price':price,'size':size,'price_per_qm':price_per_qm,'online_for':online_for})

    def parse_3(self,response):
        loader = ItemLoader(item=WgRequestsItem(),selector=response,response=response)

        #Facilities
        try:
            facilities = response.css("tr:nth-child(6) td+ td").get().replace('<td>','').replace('</td>','').strip()
        except:
            facilities ='n.a'

        
        loader.add_value('city',response.meta['city'])
        loader.add_value('district',response.meta['district'])
        loader.add_value('start_date',self.start_date_value)
        loader.add_value('end_date',self.end_date_value)
        loader.add_value("facilities",facilities)
        loader.add_value('size',response.meta['size'])
        loader.add_value('price',response.meta['price'])
        loader.add_value('name',response.meta['name'])  
        loader.add_value('online_for',response.meta['online_for'])
        loader.add_value('url',response.meta['next_page_url'])
        loader.add_value('price_per_qm',response.meta['price_per_qm'])
        yield loader.load_item()


    
