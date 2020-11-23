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
    name = 'wg_all'
    cookies1={}
    ot,date_from,date_to,fur,city_id,district_name,start_date_value,end_date_value,api = '','','','','','','','',''
    header = {}

    def start_requests(self):

        url = f"https://www.wg-gesucht.de/en/wg-zimmer-in-Berlin-gesucht.{self.city_id}.0.1.0.html" 
        if(self.api == '1'):
            yield scrapy.Request(client.scrapyGet(url=url),callback=self.parse,meta={"handle_httpstatus_list": [302,500,502]})
        else:
            yield scrapy.Request(url, callback=self.parse,meta={"handle_httpstatus_list": [302,500,502]})
    

    def parse(self, response):
            last_page = response.xpath('//nav/ul/li/a/text()').getall()
            try:
                last_page_no =int(last_page[-3].strip()) 
            except:
                last_page_no = 1
            print('LAST PAGE NO')
            print(last_page_no)
            for i in range(0,last_page_no):
                if(i == 0):             
                    yield scrapy.Request(url=response.request.url,callback=self.parse_2,dont_filter=True,meta={'dont_redirect': True,"handle_httpstatus_list": [302,500,502]})
                else:       
    
                    url = f"https://www.wg-gesucht.de/en/wg-zimmer-in-Berlin-gesucht.{self.city_id}.0.1.{i}.html"
                    if(self.api == '1'):
                        yield scrapy.Request(client.scrapyGet(url=url),callback=self.parse_2,meta={"handle_httpstatus_list": [302,500,502]})
                    else:
                        yield scrapy.Request(url,callback=self.parse_2,meta={"handle_httpstatus_list": [302,500,502]})
        
    def parse_2(self,response):
        items = response.xpath("//div[@class='col-sm-8 card_body']")

        try:
            city_name = response.xpath("//*[@id='top_column_wrapper']/div/div[1]/div/h1/text()").get().split(':')[0].replace('Flatshares in','').strip()
        except:
            city_name = 'n.a'
        
        
        for item in items:
            price = item.xpath(".//div[2]/div/b/text()").get()
            if(not price):
                price = 'n.a'
            if(price != 'from'):
                
                # Size
                size = item.xpath(".//div[2]/div[3]/b/text()").get()
                if(size == None):
                    size = 'n.a'

                
            
                


                online_for = item.xpath("..//div[3]/div[2]/div[2]/div/span[2]/text()").get()
                if(online_for):
                    online_for = online_for.replace("Online:",'').strip()
                else:
                    online_for = 'n.a'
                


                

                start_end_date = item.xpath('./div[2]/div[2]/text()').get()

                try:
    
                    start_date =   start_end_date.split('-')[0].strip() 
                    if(start_date == ''):
                        start_date = 'n.a'
                    
                except:
                    start_date = 'n.a' 
                try:
                    end_date =   start_end_date.split('-')[1].strip() 
                except:
                    end_date = 'n.a' 

                
                
                # district_name = district_name.replace('ü','u').replace('Ü','U').replace('ä','a').replace('Ä','A').replace('ö','Ö').replace('ß','ss')            
                try:
                    district_name = " ".join(item.xpath("./div[1]/div[2]/span/text()").get().split()).split('|')[1]
                    district_name = district_name.replace(city_name,'',1).strip()
                    district_name = district_name.replace('(','').replace(')','')
                except:
                    pass                    
                if(district_name == ''):
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
                if(not district_name):
                    district_name = 'n.a'


                #Price Per QM
                try:
                    price_per_qm = int(price.replace(' €',''))/int(size.replace(' m²',''))
                except:
                    price_per_qm = 'n.a'

                #URL
                try:
                    next_page_url = 'https://www.wg-gesucht.de/en/' + item.xpath(".//h3/a/@href").get()
                except:
                    next_page_url = 'n.a'
                
                #Title
                # title = item.xpath(".//div/div/h3/a/text()").get()
                # if(not title):
                #     title = 'n.a'

                # Name
                name = item.xpath("./div[3]/div[2]/div[2]/div/span[1]/text()").get() 
                if(not name):
                    name = 'n.a'
                    loader = ItemLoader(item=WgRequestsItem(),selector=item,response=response)
                    try:
                        facilities = 'n.a'
                    except:
                        facilities ='n.a'
                    loader.add_value('city',city_name)
                    loader.add_value('district',district_name)
                    loader.add_value('start_date',start_date)
                    loader.add_value('end_date',end_date)
                    loader.add_value("facilities",facilities)
                    loader.add_value('size',size)
                    loader.add_value('price',price)
                    loader.add_value('name',name)  
                    loader.add_value('online_for',online_for)
                    loader.add_value('url',next_page_url)
                    loader.add_value('price_per_qm',price_per_qm)                    
                    yield loader.load_item()   
                else:
                    try:            

                        if(self.api == '1'):
                            yield scrapy.Request(client.scrapyGet(url=next_page_url),callback=self.parse_3,meta={'url':response.request.url,'next_page_url':next_page_url,'name':name,'city':city_name,'district':district_name,'price':price,'size':size,'price_per_qm':price_per_qm,'online_for':online_for,'start_date':start_date,'end_date':end_date})
                        else:
                            yield scrapy.Request(url=next_page_url,callback=self.parse_3,meta={"handle_httpstatus_list": [302],'next_page_url':next_page_url,'name':name,'city':city_name,'district':district_name,'price':price,'size':size,'price_per_qm':price_per_qm,'online_for':online_for,'start_date':start_date,'end_date':end_date})
                    except:
                        print('No URL Found')
    def parse_3(self,response):
        loader = ItemLoader(item=WgRequestsItem(),selector=response,response=response)

        # Facilities
        try:
            facilities = response.css("tr:nth-child(6) td+ td").get().replace('<td>','').replace('</td>','').strip()
        except:
            facilities ='n.a'
        loader.add_value('city',response.meta['city'])
        loader.add_value('district',response.meta['district'])
        loader.add_value('start_date',response.meta['start_date'])
        loader.add_value('end_date',response.meta['end_date'])
        loader.add_value("facilities",facilities)
        loader.add_value('size',response.meta['size'])
        loader.add_value('price',response.meta['price'])
        loader.add_value('name',response.meta['name'])  
        loader.add_value('online_for',response.meta['online_for'])
        loader.add_value('url',response.meta['next_page_url'])
        loader.add_value('price_per_qm',response.meta['price_per_qm'])


        yield loader.load_item()


    
