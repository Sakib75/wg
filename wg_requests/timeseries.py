import pandas
from pandas import read_csv
from matplotlib import pyplot
from matplotlib.backends.backend_pdf import PdfPages
import datetime
import matplotlib.dates as mdates
pandas.options.mode.chained_assignment = None 
# Specify KPI Type
cleansing_data = True
KPI_names = ['Average price','Average size','Average €/qm','Count furnished','Count unfurnished']
def get_month(time):

	date = time.split()[0].split('.')
	date = datetime.datetime(int(date[2]),int(date[1]),int(date[0]))
	month = date.strftime("%b")
	year = date.strftime("%Y")

	date_string = f"{month} {year}"

	return date_string

def get_timing(date):
    now = datetime.datetime.now()
    try:
        if(date.endswith('day') or date.endswith('days')):
            timing = now - datetime.timedelta(days = int(date.split()[0]))
        elif(date.endswith('hour') or date.endswith('hours')):
            timing = now - datetime.timedelta(hours = int(date.split()[0]))
        elif(date.endswith('minute') or date.endswith('minutes')):
            timing = now - datetime.timedelta(minutes = int(date.split()[0]))
        else:
            timing = datetime.datetime.strptime(date, "%d.%m.%Y")
        date_string = timing.strftime("%d.%m.%Y")
    except:
        date_string = 'n.a'

    date_string = get_month(date_string)
    return date_string


def get_districts(all_district_name):
  districts = []
  for d in all_district_name:
    for district in (d.split(',')):
      if(district.lower() not in [x.lower() for x in districts]):
        districts.append(district.strip())
  return list(dict.fromkeys(districts))

def intersection(lst1, lst2):
        lst3 = [value for value in lst1 if value in lst2]
        return lst3

# Analyze data 
def Analyze_data(k_data):

                    prices = k_data['price'].str.replace(
                        '€', '').apply(pandas.to_numeric, args=('coerce',))

                    average_price = prices.mean(axis=0)





                    sizes = k_data['size'].str.replace(
                        ' m²', '').apply(pandas.to_numeric, args=('coerce',))

                    average_size = sizes.mean(axis=0)

                    prices_per_qm = k_data['price_per_qm'].apply(
                        pandas.to_numeric, args=('coerce',))

                    average_price_per_qm = prices_per_qm.mean(axis=0)
                    
                    


                    number_of_fur_yes = len(
                        k_data[k_data['facilities'].str.contains('Furnished')])
                    number_of_fur_no = len(k_data) - number_of_fur_yes

                    return {'Average Price': average_price,'Average Size':average_size,'Average €/qm':average_price_per_qm,'Count Furnished':number_of_fur_yes,'Count Unfurnished':number_of_fur_no}


series = read_csv('Requests.csv')



with PdfPages('Report_for_Requests(district_based).pdf') as pdf:

    cities = series.city.unique()
    
    cc = 1
    for city in cities:
        
        city_data = series.loc[series['city'] == city]
        districts = get_districts(city_data.district.unique())
        cd = 1

        valid_district_data = pandas.read_csv(r'valid_district_postal\Mapping_Stadtteil_PLZ.csv')
        valid_district_data_per_city = valid_district_data.loc[valid_district_data['Stadt'] == city]
        valid_district_list = list(map(str, valid_district_data_per_city['Stadtteil'].tolist()))

        all_district_name = get_districts(city_data.district.unique())

        print(f'Number of total district existing in Offers.csv : {len(all_district_name)}')


  

        if(cleansing_data == True and len(valid_district_list) > 0):
            districts = set(intersection(valid_district_list, all_district_name))

        print(f'Number of total district existing in Offers.csv (After cleansing) : {len(districts)}')

        for district in districts:

            print(f'City {cc} out of {len(cities)}  | District {cd} out of {len(districts)}')
            district_data = city_data.loc[city_data['district'].str.lower().str.contains(district.lower().replace('?',''))]

            district_data['online_for'] = district_data['online_for'].apply(get_timing)
            months = district_data['online_for'].unique().tolist()
            months.sort(key = lambda date: datetime.datetime.strptime(date, '%b %Y'))


            final_data = {'Average Price': {},'Average Size': {}, 'Average €/qm': {},'Count Furnished': {}, 'Count Unfurnished': {}}
            
            for month in months:

                month_data = district_data.loc[district_data['online_for'] == month]

                    

                kpis = Analyze_data(month_data)
                index = months
                for kpi in kpis:
                    final_data[kpi][month] = kpis[kpi]
     
            count = [x + y for x, y in zip(list(final_data['Count Furnished'].values()), list(final_data['Count Unfurnished'].values()))]
            for k in final_data:

                    data = list(final_data[k].values())
                    index = list(final_data[k].keys())


                    width = len(index) * 0.3
                    if(width < 15):
                        width = 15
                    fig, axs = pyplot.subplots(figsize=(width, 5))

                    dataFrame = pandas.DataFrame(data={k:data}, index=index)
                    color = 'tab:blue'
                    axs.set_xlabel('Month', fontsize='large', fontweight='bold')
       
                    axs.set_ylabel('Measure\'s value',color=color, fontsize='large', fontweight='bold')
                    axs.tick_params(axis='y', colors=color)
                    axs.tick_params(axis='x')
                    
                    dataFrame.plot.bar(ax=axs,rot=15, title=f"Timeseries analysis for {city}: {district}")

                     

                    x1 = []
                    
                    ax2 = axs.twinx()

                        
                    color = 'tab:red'
                    ax2.tick_params(axis='y', colors=color)
                    ax2.set_ylabel('Count',color=color, fontsize='large', fontweight='bold')
                    for i in range(0,len(count)):
                        x1.append(i)               
                    y1 = count
                    axs.format_xdata = mdates.DateFormatter('%b %Y')
                    fig.autofmt_xdate()

                        #Foreground

                    ax2.plot(x1, y1,color=color)
                    ax2.set_ylim(ymin=0)
                    # Tell matplotlib to interpret the x-axis values as dates
                    # myLocator = mticker.MultipleLocator(4)
                    # axs.xaxis.set_major_locator(myLocator)
                    pyplot.xticks(rotation=90)
                    pyplot.grid()
                    fig.tight_layout()
                    pdf.savefig()
                    pyplot.close()

            
            
            
            # timestamps = district_data['Timestamp'].unique()

            # furnished = district_data.loc[district_data['KPI Name'] == 'Count furnished'].Result.tolist()
            # unfurnished = district_data.loc[district_data['KPI Name'] == 'Count unfurnished'].Result.tolist()

            # count = [x + y for x, y in zip(furnished, unfurnished)]

            # index = get_month(timestamps)

            # index.sort(key=lambda date: datetime.datetime.strptime(date, "%b %Y"))

            # for kpi in KPI_names:
            #     fig, axs = pyplot.subplots()
            #     data = {
            #         kpi: district_data.loc[district_data['KPI Name'] == kpi].Result.tolist(),
            #     }


            #     dataFrame = pandas.DataFrame(data=data, index=index)

            #     #Background 
            #     color = 'tab:blue'
            #     axs.set_xlabel('Month', fontsize='large', fontweight='bold')
                
            #     axs.set_ylabel('Measure\'s value',color=color, fontsize='large', fontweight='bold')
            #     axs.tick_params(axis='y', colors=color)

            #     dataFrame.plot.bar(ax=axs,rot=15, title=f"Timeseries analysis for {city}: {district}")

            #     x1 = []

            #     ax2 = axs.twinx()
                
            #     color = 'tab:red'
            #     ax2.tick_params(axis='y', colors=color)
            #     ax2.set_ylabel('Count',color=color, fontsize='large', fontweight='bold')
            #     for i in range(0,len(count)):
            #         x1.append(i)               
            #     y1 = count


            #     #Foreground

            #     ax2.plot(x1, y1,color=color)
            #     ax2.set_ylim(ymin=0)
            #     fig.tight_layout()
            #     pdf.savefig()
            #     pyplot.close()
            cd = cd + 1
        cc = cc + 1