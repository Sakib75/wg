import scrapy
from http.cookies import SimpleCookie
from ..items import WgUpdateItem
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
  

    def start_requests(self):

        url = f"https://www.wg-gesucht.de/en/wg-zimmer-in-Berlin.{self.city_id}.0.1.0.html" 
        if(self.api == '1'):
            yield scrapy.Request(client.scrapyGet(url=url),callback=self.parse)
        else:
            yield scrapy.Request(url, callback=self.parse,meta={"handle_httpstatus_list": [302]})
    

    def parse(self, response):
            last_page = response.xpath('//nav/ul/li/a/text()').getall()
            try:
                last_page_no =int(last_page[-3].strip()) 
            except:
                last_page_no = 1
            print(f'Last Page No: {last_page_no}')

            for i in range(0,last_page_no):
                if(i == 0):             
                    yield scrapy.Request(url=response.request.url,callback=self.parse_2,dont_filter=True,meta={"handle_httpstatus_list": [302]})
                else:       
                    url = response.request.url       
                    url = f"https://www.wg-gesucht.de/en/wg-zimmer-in-Berlin.{self.city_id}.0.1.{i}.html"
                    if(self.api == '1'):
                        yield scrapy.Request(client.scrapyGet(url=url),callback=self.parse_2)
                    else:
                        yield scrapy.Request(url,callback=self.parse_2,meta={"handle_httpstatus_list": [302]})
        
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
                
                #Size
                size = item.xpath(".//div[2]/div[3]/b/text()").get()
                if(size == None):
                    size = 'n.a'

                #Owner
                owner = item.xpath("./div[3]/div[2]/div[2]/div/span[1]/text()").get() 
                if(not owner):
                    owner = 'n.a'  

                #Online For
                online_for = item.xpath("..//div[3]/div[2]/div[2]/div/span[2]/text()").get()
                if(online_for):
                    online_for = online_for.replace("Online:",'').strip()
                else:
                    online_for = 'n.a'

                #District Name
                try:
                    district_name = " ".join(item.xpath("./div[1]/div[2]/span/text()").get().split()).split('|')[1] 
                    district_name = district_name.replace(city_name,'',1).strip()
                    district_name = district_name.replace('(','').replace(')','')
                except:
                    pass
                if(district_name == ''):
                    district_name = city_name

                #Start date
                start_end_date = item.xpath('./div[2]/div[2]/text()').get()
                try:
    
                    start_date =   start_end_date.split('-')[0].replace('from\n','').strip() 
                    if(start_date == ''):
                        start_date = 'n.a'
                except:
                    start_date = 'n.a' 
                
                #End date
                try:
                    end_date =   start_end_date.split('-')[1].strip() 
                except:
                    end_date = 'n.a' 

                # Title
                title = item.xpath(".//div/div/h3/a/text()").get()
                if(not title):
                    title = 'n.a'
                
                # URL
                next_page_url = "https://www.wg-gesucht.de" + item.xpath(".//h3/a/@href").get()
                if(not next_page_url):
                    next_page_url = 'n.a'

                if(self.api == '1'):
                    yield scrapy.Request(client.scrapyGet(url=next_page_url),callback=self.parse_3,meta={'owner':owner,'city':city_name,'district':district_name,'size':size,'online_for':online_for,'start_date':start_date,'end_date':end_date,'title':title,'url':next_page_url})
                else:
                    yield scrapy.Request(url=next_page_url,callback=self.parse_3,meta={"handle_httpstatus_list": [302],'owner':owner,'city':city_name,'district':district_name,'size':size,'online_for':online_for,'start_date':start_date,'end_date':end_date,'title':title,'url':next_page_url})

    def parse_3(self,response):
        loader = ItemLoader(item=WgUpdateItem(),selector=response,response=response)

        #Base Rent
        base_rent = response.xpath("//table/tr/td/b/text()").get()
        if(not base_rent):
            base_rent = 'n.a'

        #Address
        address = ' '.join(response.css('.col-sm-4 a::text').getall()).replace('\n','').replace('   ','').strip()
        if(not address):
            address = 'n.a'
        
        #Postal Code
        words = address.split()

        if(response.meta['city'] in words[1:]):
            try:
                code = int(words[words.index(response.meta['city'])-1])
            except:
                code = 'n.a'
        else:
            code = 'n.a'

        #Furnished Status
        try:
            furnished_data = " ".join(response.css(".text-center.print_text_left::text").getall()).replace("\n",'').split()
            if('furnished' in furnished_data or 'Furnished' in furnished_data):
                fur = 'Yes'
            else:
                fur = 'No'

        except:
            fur = 'No'

        # Misc Cost
        try:
            misc_cost = response.xpath("//*[@id='misc_costs']/label/text()").get().strip()
        except:
            misc_cost = 'n.a'
        
        #Utilities Cost
        try:
            utilities_cost = response.xpath("//*[@id='utilities_costs']/label/text()").get().strip()
        except:
            utilities_cost = 'n.a'

        #Rent
        try:
            rent = response.xpath("//*[@id='rent']/label/text()").get().strip()
        except:
            rent = 'n.a'

        #Price
        try:
            price = response.xpath("//*[@id='graph_wrapper']/div[2]/label[1]/text()").get().strip()
        except:
            price = 'n.a'

        #Price Per QM
        try:
            price_per_qm = int(price.replace('€',''))/int(response.meta['size'].replace('m²',''))
        except:
            price_per_qm = 'n.a'

        loader.add_value('city',response.meta['city'])
        loader.add_value('district',response.meta['district'])
        loader.add_value('address',address)
        loader.add_value('postal_code',code)
        loader.add_value('start_date',response.meta['start_date'])
        loader.add_value('end_date',response.meta['end_date'])
        loader.add_value('furnished',fur)
        loader.add_value('size',response.meta['size'])
        loader.add_value('miscellaneous_cost',misc_cost)
        loader.add_value('utilities_cost',utilities_cost)
        loader.add_value('rent',rent)
        loader.add_value('price',price)
        loader.add_value('base_rent',base_rent)
        loader.add_value('owner',response.meta['owner'])
        loader.add_value('online_for',response.meta['online_for'])
        loader.add_value('url',response.meta['url'])
        loader.add_value('title',response.meta['title'])
        loader.add_value('price_per_qm',price_per_qm)

        yield loader.load_item()