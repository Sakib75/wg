import csv
import pandas
from set_parameters import start_date_value,end_date_value,scrape_all
from datetime import datetime

scrape_all = True

now = datetime.now()
timestamp = f'{now.day}.{now.month}.{now.year} {now.hour}:{now.minute}'

def get_districts(all_district_name):
  districts = []
  for d in all_district_name:
    for district in (d.split(',')):
      if(district.lower() not in [x.lower() for x in districts]):
        districts.append(district.strip())
  return list(dict.fromkeys(districts))
def write_header(field_name,file_name):
    out_file = open(file_name,'w')
    head = f"Timestamp,Filetype,City,{field_name},KPIType,KPI Name,Result" + "\n"
    out_file.write(head)
    out_file.close()

try:
  with open('pre_calculation.csv','r') as f:
    reader = csv.reader(f)
    try:
      row1 = next(reader)
      if(row1 != []):
        pass
      else:
        write_header('District','pre_calculation.csv')
    except:
        write_header('District','pre_calculation.csv')
except:
  write_header('District','pre_calculation.csv')

df = pandas.read_csv('Offers.csv')


if(scrape_all == True):
  date_filter = df
else:
  date_filter_primary = df.loc[df['start_date'] == start_date_value]
  date_filter = date_filter_primary[date_filter_primary['end_date'] == end_date_value]



all_city_name = date_filter.city.unique()
for city in all_city_name:
  city_data = date_filter.loc[date_filter['city'] == city]
  all_district_name = get_districts(city_data.district.unique())

  for district in all_district_name:
    print(f'{city} : {district}' )
    district_data = city_data.loc[city_data['district'].str.lower().str.contains(district.lower())]
    print(district_data[['city','district','price','size','furnished']])
    prices = district_data['price'].str.replace('€','').apply(pandas.to_numeric, args=('coerce',))

    average_price = prices.mean(axis= 0)
    

    sizes = district_data['size'].str.replace(' m²','').apply(pandas.to_numeric, args=('coerce',))
    
    average_size = sizes.mean(axis= 0)

    prices_per_qm = district_data['price_per_qm'].apply(pandas.to_numeric, args=('coerce',))
    

    average_price_per_qm = prices_per_qm.mean(axis=0)
    
    number_of_fur_yes = len(district_data[district_data['furnished'].str.contains('Yes')])
    number_of_fur_no = len(district_data) - number_of_fur_yes
    
    print('*************')
    print(city)
    print(district)
    print(start_date_value)
    print(end_date_value)
    print(f'Average price: {average_price}')
    print(f'Average size: {average_size}')
    print(f'Average price/qm: {average_price_per_qm}')
    print(f'No of fur:Yes: {number_of_fur_yes}')
    print(f'No of fur: No: {number_of_fur_no}')



    with open('pre_calculation.csv', mode='a',encoding='utf-8',newline='') as csv_file:
      csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

      csv_writer.writerow([timestamp,'offers',city, district, 'KPI 1','Average price',average_price])
      csv_writer.writerow([timestamp,'offers',city ,district, 'KPI 2','Average size',average_size])
      csv_writer.writerow([timestamp,'offers',city, district, 'KPI 3','Average €/qm',average_price_per_qm])
      csv_writer.writerow([timestamp,'offers',city, district, 'KPI 4','Count furnished',number_of_fur_yes])
      csv_writer.writerow([timestamp,'offers',city, district, 'KPI 5','Count unfurnished',number_of_fur_no])



try:
  with open('pre_calculation(postal_code).csv','r') as f:
    reader = csv.reader(f)
    try:
      row1 = next(reader)
      if(row1 != []):
        pass
      else:
        write_header('Postal_Code','pre_calculation(postal_code).csv')
    except:
        write_header('Postal_Code','pre_calculation(postal_code).csv')
except:
  write_header('Postal_Code','pre_calculation(postal_code).csv')

all_post = date_filter.postal_code.unique()

for post in all_post:
  print(post)
  data = date_filter.loc[date_filter['postal_code'] == post]
  print(data)
  prices = data['price'].str.replace('€','').apply(pandas.to_numeric, args=('coerce',))

  average_price = prices.mean(axis= 0)

  sizes = data['size'].str.replace(' m²','').apply(pandas.to_numeric, args=('coerce',))
    
  average_size = sizes.mean(axis= 0)
  prices_per_qm = data['price_per_qm'].apply(pandas.to_numeric, args=('coerce',))
  average_price_per_qm = prices_per_qm.mean(axis=0)
  number_of_fur_yes = len(data[data['furnished'] == 'Yes'])
  number_of_fur_no = len(data[data['furnished'] == 'No'])
  print('*************')
  print(district)
  print(start_date_value)
  print(end_date_value)
  print(f'Average price: {average_price}')
  if(not average_price):
    average_price = 'n.a'
  print(f'Average size: {average_size}')
  if(not average_size):
    average_size = 'n.a'

  print(f'Average price/qm: {average_price_per_qm}')
  print(f'No of fur:Yes: {number_of_fur_yes}')
  print(f'No of fun: No: {number_of_fur_no}')
  postal_code = post
  with open('pre_calculation(postal_code).csv', mode='a',encoding='utf-8',newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    csv_writer.writerow([timestamp,'offers',city,postal_code, 'KPI 1','Average price',average_price])
    csv_writer.writerow([timestamp,'offers',city,postal_code, 'KPI 2','Average size',average_size])
    csv_writer.writerow([timestamp,'offers',city,postal_code, 'KPI 3','Average €/qm',average_price_per_qm])
    csv_writer.writerow([timestamp,'offers',city,postal_code, 'KPI 4','Count furnished',number_of_fur_yes])
    csv_writer.writerow([timestamp,'offers',city,postal_code, 'KPI 5','Count unfurnished',number_of_fur_no])