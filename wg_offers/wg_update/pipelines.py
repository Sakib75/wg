# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import csv

class WgUpdatePipeline:
    def open_spider(self, spider):

        pass

    def close_spider(self, spider):
        pass
        

    def process_item(self, item, spider):
        self.file_1 = open('Offers.csv','a',encoding='utf-8',newline='')
        item.setdefault('city','n.a')
        item.setdefault('district','n.a')
        item.setdefault('address','n.a')
        item.setdefault('postal_code','n.a')
        item.setdefault('start_date','n.a')
        item.setdefault('end_date','n.a')
        item.setdefault('furnished','n.a')
        item.setdefault('size','n.a')
        item.setdefault('price','n.a')
        item.setdefault('base_rent','n.a')
        item.setdefault('owner','n.a')
        item.setdefault('online_for','n.a')
        item.setdefault('url','n.a')
        item.setdefault('title','n.a')
        item.setdefault('price_per_qm','n.a')
        writer = csv.writer(self.file_1,delimiter=',')
        writer.writerow(ItemAdapter(item).values())

        self.file_1.close()

        
        return item
        
