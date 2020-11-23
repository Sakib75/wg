import os
import csv
import datetime
import time
import json
from set_parameters import start_date_value,end_date_value,scrape_all,use_scraper_api



try:
    input_file = open('input_file.csv','r',encoding="utf-8")
except:
    print('Not input file')

reader = csv.DictReader(input_file)
codes = []
for row in reader:

    code = (row['City_code'])
    if code not in codes:
        codes.append(code)
        if(use_scraper_api):
            os.system(f'scrapy crawl get_district_data -a city_code={code} -a api=1')
        else:
            os.system(f'scrapy crawl get_district_data -a city_code={code} -a api=2')



# Setting up the output file

def write_header():
    out_file = open('Offers.csv','w')
    head = "city,district,address,postal_code,start_date,end_date,furnished,size,miscellaneous_cost,utilities_cost,rent,price,base_rent,owner,online_for,url,title,price_per_qm" + "\n"
    out_file.write(head)
    out_file.close()
try:
    with open('Offers.csv', newline='') as f:
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

# Reading the inputs and sending crawl request to Scrapy spider for each input 
try:
    input_file = open('input_file.csv','r',encoding="utf-8")
except:
    print('Not input file')

reader = csv.DictReader(input_file)
for row in reader:

    # Parsing the inputs 

    # Convert start and end date to timestamp 
    try:
        start_date = list(map(int,start_date_value.split('.')))
        start_date = int(datetime.datetime(start_date[2],start_date[1],start_date[0]).timestamp())
        end_date = list(map(int,end_date_value.split('.')))
        end_date = int(datetime.datetime(end_date[2],end_date[1],end_date[0]).timestamp())
    except:
        start_date = ''
        end_date = ''

    # City ID
    city_id = row['City_code']

    # District Code
    district_code = ''
    try:
        district_name = row['District_name']
        if(district_name != 'any'):
          
            district_code_file = open(f'./district_codes/district_codes {city_id}.json',encoding='utf-8')
   
            data = json.load(district_code_file)

            district_code =  data.get(district_name.strip())

            
            print(district_code)
            
    except:
        print('error')
        

    
    # Sending crawl requests for each input
    if(scrape_all == True):
        if(use_scraper_api):
            os.system(f"scrapy crawl wg_all -a city_id={city_id} -a api=1")
        else:
            os.system(f"scrapy crawl wg_all -a city_id={city_id} -a api=2")
    else:
        if(district_name == 'any'):
            
            if(use_scraper_api):
                command = f"scrapy crawl wg -a ot= -a date_to={end_date} -a date_from={start_date} -a city_id={city_id} -a start_date_value={start_date_value} -a end_date_value={end_date_value} -a api=1"
            else:
                command = f"scrapy crawl wg -a ot= -a date_to={end_date} -a date_from={start_date} -a city_id={city_id} -a start_date_value={start_date_value} -a end_date_value={end_date_value} -a api=2"
            os.system(command)

        elif(district_code != 'any' and district_code != ''):
            
            if(use_scraper_api):
                command = f"scrapy crawl wg -a ot={district_code} -a date_to={end_date} -a date_from={start_date} -a city_id={city_id} -a start_date_value={start_date_value} -a end_date_value={end_date_value} -a api=1"
            else:
                command = f"scrapy crawl wg -a ot={district_code} -a date_to={end_date} -a date_from={start_date} -a city_id={city_id} -a start_date_value={start_date_value} -a end_date_value={end_date_value} -a api=2"
            os.system(command)



# os.system("python pre_calculation.py")


    
 
    



