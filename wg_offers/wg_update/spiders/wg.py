import scrapy
from http.cookies import SimpleCookie
from ..items import WgUpdateItem
from scrapy.loader import ItemLoader
import re
from scraper_api import ScraperAPIClient
from scraperapikey import key

client = ScraperAPIClient(key)

class WgSpider(scrapy.Spider):
    name = 'wg'
    cookies1={}
    ot,date_from,date_to,fur,city_id,start_date_value,end_date_value,api = '','','','','','','',''
    

    def start_requests(self):
        
        rawdata = f" last_city={self.city_id}; last_cat=0; last_type=0"
        cookie = SimpleCookie()
        cookie.load(rawdata)        
        for key,morsel in cookie.items():
            self.cookies1[key] = morsel.value
        
        url = f"https://www.wg-gesucht.de/en/wg-zimmer-in-cityname.{self.city_id}.0.1.0.html?offer_filter=1&city_id={self.city_id}&noDeact=1&dFr={self.date_from}&dTo={self.date_to}&categories%5B%5D=0&rent_types%5B%5D=0&ot%5B%5D={self.ot}" 
        if(self.api == '1'):
            yield scrapy.Request(client.scrapyGet(url=url),cookies=self.cookies1,callback=self.parse)
        else:
            yield scrapy.Request(url=url,cookies=self.cookies1,callback=self.parse,dont_filter=True,meta={"handle_httpstatus_list": [302]})
    

    def parse(self, response):
            last_page = response.xpath('//nav/ul/li/a/text()').getall()
            try:
                last_page_no =int(last_page[-3].strip()) 
            except:
                last_page_no = 1
            rawdata = f" last_city={self.city_id}; last_cat=0; last_type=0"
            cookie = SimpleCookie()
            cookie.load(rawdata)
            cookies1={}
            for key,morsel in cookie.items():
                cookies1[key] = morsel.value
            print(f'Last Page Number: {last_page_no}')

            for i in range(0,last_page_no):
                if(i == 0):             
                    yield scrapy.Request(url=response.request.url,cookies=self.cookies1,callback=self.parse_2,dont_filter=True,meta={'dont_redirect': True,"handle_httpstatus_list": [302]})
                else:            
                    url = response.request.url       
                    url = f"https://www.wg-gesucht.de/en/wg-zimmer-in-cityname.{self.city_id}.0.1.{i}.html?category=0&city_id={self.city_id}&rent_type=0&noDeact=1&dFr={self.date_from}&dTo={self.date_to}&ot={self.ot}&img=1&rent_types%5B0%5D=0"
                    if(self.api == '1'):
                        yield scrapy.Request(client.scrapyGet(url=url),cookies=self.cookies1,callback=self.parse_2)
                    else:
                        yield scrapy.Request(url=url,cookies=self.cookies1,callback=self.parse_2,dont_filter=True,meta={"handle_httpstatus_list": [302]})

        
    def parse_2(self,response):
        #City Name
        try:
            city_name = response.xpath("//*[@id='top_column_wrapper']/div/div[1]/div/h1/text()").get().split(':')[0].replace('Flatshares in','').strip()
        except:
            city_name = 'n.a'
        
        
        items = response.xpath("//div[@class='col-sm-8 card_body']")
        for item in items:
            price = item.xpath(".//div[2]/div/b/text()").get()
            if(not price):
                price = 'n.a'
            if(price != 'from'):

                #District Name
               
                try:
                    district_name = " ".join(item.xpath("./div[1]/div[2]/span/text()").get().split()).split('|')[1] 
                    district_name = district_name.replace(city_name,'',1).strip()
                    district_name = district_name.replace('(','').replace(')','')
                except:
                    pass
                if(district_name == ''):
                    district_name = city_name

                
                #Size
                size = item.xpath(".//div[2]/div[3]/b/text()").get()
                if(not size):
                    size = 'n.a'

                #Owner
                owner = item.xpath(".//div[3]/div[2]/div[2]/div/span/text()").get()
                if(not owner):
                    owner = 'n.a'
                #Online For
                online_for = item.xpath(".//div[3]/div[2]/div[2]/div/span[2]/text()").get().replace("Online: ","")
                if(not online_for):
                    online_for = 'n.a'

                #Title
                title = item.xpath(".//div/div/h3/a/text()").get()
                if(not title):
                    title = 'n.a'
                
                #URL
                next_page_url = 'https://www.wg-gesucht.de' + item.xpath(".//h3/a/@href").get()
                if(not next_page_url):
                    next_page_url = 'n.a'

                if(self.api == '1'):
                    yield scrapy.Request(client.scrapyGet(url=next_page_url),callback=self.parse_3,meta={"handle_httpstatus_list": [302],'size':size,'owner':owner,'online_for':online_for,'title':title,'city':city_name,'district':district_name,'url':next_page_url})
                else:
                    yield scrapy.Request(url=next_page_url,cookies=self.cookies1,callback=self.parse_3,dont_filter=True,meta={"handle_httpstatus_list": [302],'size':size,'owner':owner,'online_for':online_for,'title':title,'city':city_name,'district':district_name,'url':next_page_url})

    
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
        loader.add_value('start_date',self.start_date_value)
        loader.add_value('end_date',self.end_date_value)
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



    
