# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv

class WgRequestsPipeline:
    def open_spider(self, spider):

        pass

    def close_spider(self, spider):

        pass

    def process_item(self, item, spider):
        item.setdefault('start_date','')
        item.setdefault('end_date','')
        self.file_1 = open('Requests.csv','a',encoding='utf-8',newline='')
        writer = csv.writer(self.file_1,delimiter=',')
        writer.writerow(ItemAdapter(item).values())
        self.file_1.close()


        
        return item

