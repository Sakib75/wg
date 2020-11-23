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
        if(use_scraper_api == True):
            os.system(f'scrapy crawl get_district_data -a city_code={code} -a api=1')
        else:
            os.system(f'scrapy crawl get_district_data -a city_code={code} -a api=2')



# Setting up the output file

def write_header():
    out_file = open('Requests.csv','w')
    head = "city,district,start_date,end_date,facilities,size,price,name,online_for,url,price_per_qm" + "\n"
    out_file.write(head)
    out_file.close()

try:
    with open('Requests.csv', newline='') as f:
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
    if(start_date_value != 'any' and end_date_value != 'any'):
        start_date = list(map(int,start_date_value.split('.')))
        start_date = int(datetime.datetime(start_date[2],start_date[1],start_date[0]).timestamp())
        end_date = list(map(int,end_date_value.split('.')))
        end_date = int(datetime.datetime(end_date[2],end_date[1],end_date[0]).timestamp())
    else:
        start_date = ''
        end_date = ''

    city_id = row['City_code']



    district_name = row['District_name']
    district_code_file = open(f'./district_codes/district_codes {city_id}.json',encoding='utf-8')
    data = json.load(district_code_file)
    all_districts = []

    for key in data.keys():
        if(not key[0].isdigit() and key != 'Any'):
            all_districts.append(key)

    all_districts = ','.join(all_districts)

    if(scrape_all == True):
        if(use_scraper_api == True):
            os.system(f"scrapy crawl wg_all -a city_id={city_id} -a api=1")
        else:
            os.system(f"scrapy crawl wg_all -a city_id={city_id} -a api=2")
    else:

     
        if(district_name == 'any'):
            if(use_scraper_api == True):                    
                command = f"scrapy crawl wg -a ot=0 -a district_name={district_name} -a date_to={end_date} -a date_from={start_date} -a city_id={city_id} -a start_date_value={start_date_value} -a end_date_value={end_date_value} -a api=1"
            else:
                command = f"scrapy crawl wg -a ot=0 -a district_name={district_name} -a date_to={end_date} -a date_from={start_date} -a city_id={city_id} -a start_date_value={start_date_value} -a end_date_value={end_date_value} -a api=2"
            os.system(command)
            time.sleep(10)
        else:
            district_code =  data[district_name.strip()]
            if(use_scraper_api == True):
                command = f"scrapy crawl wg -a ot={district_code} -a district_name={district_name} -a date_to={end_date} -a date_from={start_date} -a city_id={city_id} -a start_date_value={start_date_value} -a end_date_value={end_date_value} -a api=1"
            else:
                command = f"scrapy crawl wg -a ot={district_code} -a district_name={district_name} -a date_to={end_date} -a date_from={start_date} -a city_id={city_id} -a start_date_value={start_date_value} -a end_date_value={end_date_value} -a api=2"
            os.system(command)
            time.sleep(10)

    

# os.system("python pre_calculation.py")
    

    


    
 
    



