import csv
import pandas
from set_parameters import start_date_value,end_date_value,scrape_all
from datetime import datetime


cleansing_data = True

def intersection(lst1, lst2):
        lst3 = [value for value in lst1 if value in lst2]
        return lst3
        
def get_districts(all_district_name):
  districts = []
  for d in all_district_name:
    for district in (d.split(',')):
      if(district.lower() not in [x.lower() for x in districts]):
        districts.append(district.strip())
  return list(dict.fromkeys(districts))

now = datetime.now()
timestamp = f'{now.day}.{now.month}.{now.year} {now.hour}:{now.minute}'

def write_header():
    out_file = open('pre_calculation(district).csv','w')
    head = "Timestamp,Filetype,City,District,KPIType,KPI Name,Result" + "\n"
    out_file.write(head)
    out_file.close()

try:
  with open('pre_calculation(district).csv','r') as f:
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

df = pandas.read_csv('Requests.csv')




if(scrape_all == True):
  date_filter = df
else:
  date_filter_primary = df.loc[df['start_date'] == start_date_value]
  date_filter = date_filter_primary[date_filter_primary['end_date'] == end_date_value]

all_city_name = date_filter.city.unique()

for city in all_city_name:
  print(f'City : {city}')
  city_data = date_filter.loc[date_filter['city'] == city]
    

  valid_district_data = pandas.read_csv(r'valid_district_postal\Mapping_Stadtteil_PLZ.csv')
  valid_district_data_per_city = valid_district_data.loc[valid_district_data['Stadt'] == city]
  valid_district_list = list(map(str, valid_district_data_per_city['Stadtteil'].tolist()))

  all_district_name = get_districts(city_data.district.unique())

  print(f'Number of total district existing in Offers.csv : {len(all_district_name)}')


    

  if(cleansing_data == True and len(valid_district_list) > 0):
    all_district_name = set(intersection(valid_district_list, all_district_name))

  print(f'Number of total district existing in Offers.csv (After cleansing) : {len(all_district_name)}')


  for district in all_district_name:

    district_data = city_data.loc[city_data['district'].str.lower().str.contains(district.lower().replace('?',''))]

    prices = district_data['price'].str.replace('€','').apply(pandas.to_numeric, args=('coerce',))

    average_price = prices.mean(axis= 0)
    

    sizes = district_data['size'].str.replace(' m²','').apply(pandas.to_numeric, args=('coerce',))
    
    average_size = sizes.mean(axis= 0)

    prices_per_qm = district_data['price_per_qm'].apply(pandas.to_numeric, args=('coerce',))
    

    average_price_per_qm = prices_per_qm.mean(axis=0)
    
    number_of_fur_yes = len(district_data[district_data['facilities'].str.contains('Furnished')])
    number_of_fur_no = len(district_data) - number_of_fur_yes
    



    with open('pre_calculation(district).csv', mode='a',encoding='utf-8',newline='') as csv_file:
      csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

      csv_writer.writerow([timestamp,'requests',city, district, 'KPI 1','Average price',average_price])
      csv_writer.writerow([timestamp,'requests',city ,district, 'KPI 2','Average size',average_size])
      csv_writer.writerow([timestamp,'requests',city, district, 'KPI 3','Average €/qm',average_price_per_qm])
      csv_writer.writerow([timestamp,'requests',city, district, 'KPI 4','Count furnished',number_of_fur_yes])
      csv_writer.writerow([timestamp,'requests',city, district, 'KPI 5','Count unfurnished',number_of_fur_no])




