# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv

class WgTestPipeline:
    def open_spider(self,spider):
        def write_header():
            out_file = open('Number_of_Offers_Reuqests.csv','w')
            head = "start_date,end_date,city_id,city_name,type,amount" + "\n"
            out_file.write(head)
            out_file.close()
        try:
            with open('Number_of_Offers_Reuqests.csv', newline='') as f:
                reader = csv.reader(f)
                try:
                    row1 = next(reader)
                    if(row1 != []):
                        pass
                    else:
                        write_header()
                except:
                    write_header()
        except:
            write_header()

    def process_item(self, item, spider):

        self.file1 = open('Number_of_Offers_Reuqests.csv','a',encoding='utf-8',newline='')
        writer = csv.writer(self.file1,delimiter=',')
        writer.writerow(ItemAdapter(item).values())
        self.file1.close()

        return item
