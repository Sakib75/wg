import pandas
from pandas import read_csv
from matplotlib import pyplot
from matplotlib.backends.backend_pdf import PdfPages
import datetime
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
pandas.options.mode.chained_assignment = None  # default='warn'
from pylab import MaxNLocator
# Specify KPI Type
cleansing_data = True
foreground_opacity = 0.8

KPI_names = ['Average Price','Average Size','Average €/qm','Count furnished','Count unfurnished']

def Include_Empty_months(data):
    month_range = pandas.date_range(start=list(data.keys())[0], end=list(data.keys())[-1], freq='MS').strftime('%b %Y').tolist()
    final_data = pandas.Series(data, index=month_range).fillna(0).to_dict()
    return final_data

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

# Analyze data 
def Analyze_data(k_data):

                    prices = k_data['price'].str.replace(
                        '€', '').apply(pandas.to_numeric, args=('coerce',))

                    average_price = prices.mean(axis=0)

                    miscellaneous_costs = k_data['miscellaneous_cost'].str.replace(
                        '€', '').apply(pandas.to_numeric, args=('coerce',))

                    average_miscellaneous_cost = miscellaneous_costs.mean(axis=0)


                    


                    utilities_costs = k_data['utilities_cost'].str.replace(
                        '€', '').apply(pandas.to_numeric, args=('coerce',))

                    average_utilities_cost = utilities_costs.mean(axis=0)


                    rents = k_data['rent'].str.replace(
                        '€', '').apply(pandas.to_numeric, args=('coerce',))

                    average_rent = rents.mean(axis=0)


                    base_rent = k_data['base_rent'].str.replace(
                        '€', '').apply(pandas.to_numeric, args=('coerce',))

                    average_base_rent = base_rent.mean(axis=0)

                    sizes = k_data['size'].str.replace(
                        ' m²', '').apply(pandas.to_numeric, args=('coerce',))

                    average_size = sizes.mean(axis=0)

                    prices_per_qm = k_data['price_per_qm'].apply(
                        pandas.to_numeric, args=('coerce',))

                    average_price_per_qm = prices_per_qm.mean(axis=0)
                    
                    


                    number_of_fur_yes = len(
                        k_data[k_data['furnished'].str.contains('Yes')])
                    number_of_fur_no = len(k_data) - number_of_fur_yes

                    return {'Average Miscellaneous Cost':average_miscellaneous_cost,'Rent':average_rent,'Average Utilities Cost':average_utilities_cost,'Average Base Rent':average_base_rent,'Average Price': average_price,'Average Size':average_size,'Average €/qm':average_price_per_qm,'Count Furnished':number_of_fur_yes,'Count Unfurnished':number_of_fur_no}

def Graph_for_ind(pd,type):
                series['postal_code'] = series['postal_code'].apply(str)
                pd_data = series.loc[series[type]==pd]         
                pd_data['online_for'] = pd_data['online_for'].apply(get_timing)
                months = pd_data['online_for'].unique().tolist()
                months.sort(key = lambda date: datetime.datetime.strptime(date, '%b %Y'))
                final_data = {'Average Price': {},'Average Size': {}, 'Average €/qm': {},'Count Furnished': {}, 'Count Unfurnished': {},'Average Miscellaneous Cost': {},'Rent':{},'Average Utilities Cost':{},'Average Base Rent':{}}
                for month in months:
                    month_data = pd_data.loc[pd_data['online_for'] == month]
                    kpis = Analyze_data(month_data)
                    index = months
                    for kpi in kpis:
                        final_data[kpi][month] = kpis[kpi]
                count = [x + y for x, y in zip(list(final_data['Count Furnished'].values()), list(final_data['Count Unfurnished'].values()))]
                count_map = Include_Empty_months(dict(zip(months,count)))         
                for k in final_data:
                    final_data[k] = Include_Empty_months(final_data[k])
                    data = list(final_data[k].values())
                    index = list(final_data[k].keys())
                    width = len(index) * 0.3
                    if(width < 15):
                        width = 15
                    fig, axs = pyplot.subplots(figsize=(width, 5))
                    dataFrame = pandas.DataFrame(data={k:data}, index=index)
                    color = 'tab:red'
                    axs.set_xlabel('Month', fontsize='large', fontweight='bold')
                    axs.set_ylabel('Count',color=color, fontsize='large', fontweight='bold')
                    ya = axs.get_yaxis()
                    ya.set_major_locator(MaxNLocator(integer=True))
                    axs.plot(list(count_map.keys()), list(count_map.values()),color=color)
                    axs.set_ylim(ymin=0)                        
                    axs.format_xdata = mdates.DateFormatter('%b %Y')
                    fig.autofmt_xdate() 
                    color = 'tab:blue'
                    ax2 = axs.twinx()
                    dataFrame.plot.bar(ax=ax2,rot=15, title=f"Timeseries analysis for {city}: {pd} ({k})",alpha=foreground_opacity)
                    ax2.tick_params(axis='y', colors=color)
                    ax2.set_ylabel('Measure\'s value',color=color, fontsize='large', fontweight='bold')
                    ax2.grid(True)
                    fig.tight_layout()
                    pdf.savefig()
                    pyplot.close()



def intersection(lst1, lst2):

        lst3 = [value for value in lst1 if value in lst2]
        return lst3



series = read_csv('Offers.csv')

with PdfPages('Report_for_Offers(postal_code_based).pdf') as pdf:
    cities = series.city.unique()
    valid_postal_data = pandas.read_csv(r'valid_district_postal\Mapping_Stadtteil_PLZ.csv')
    cc = 1
    for city in cities:
        Graph_for_ind(city,'city')       
        city_data = series.loc[series['city'] == city]
        postals = list(map(str,city_data.postal_code.unique().tolist()))

        valid_postal_data_per_city = valid_postal_data.loc[valid_postal_data['Stadt'] == city]
        valid_postal_list = list(map(str, valid_postal_data_per_city['PLZ'].tolist()))    
        
        print(f'Number of total postals existing in Offers.csv : {len(postals)}')

        if(cleansing_data == True and len(valid_postal_list) > 0):
            postals = set(intersection(valid_postal_list, postals))
        
        print(f'Number of total postals existing in Offers.csv (After cleansing) : {len(postals)}')

        print(f'Plotting graph for city {city}')
        Graph_for_ind(city,'city')

        cd = 1
        for postal in postals:
            print(postal)
            print(f'City {cc} out of {len(cities)} | Postal Code {cd} out of {len(postals)}')
            

            Graph_for_ind(postal,'postal_code')


            cd = cd + 1
        cc = cc + 1
    


with PdfPages('Report_for_Offers(district_based).pdf') as pdf:

    cities = series.city.unique()
    
    cc = 1
    valid_district_data = pandas.read_csv(r'valid_district_postal\Mapping_Stadtteil_PLZ.csv')
    

    for city in cities:
        
        city_data = series.loc[series['city'] == city]
        districts = city_data.district.unique()
        

        valid_district_data_per_city = valid_district_data.loc[valid_district_data['Stadt'] == city]
        valid_district_list = list(map(str, valid_district_data_per_city['Stadtteil'].tolist()))    
        
        print(f'Number of total district existing in Offers.csv : {len(districts)}')

        if(cleansing_data == True and len(valid_district_list) > 0):
            districts = set(intersection(valid_district_list, districts))
        
        print(f'Number of total district existing in Offers.csv (After cleansing) : {len(districts)}')

        print(f'Plotting graph for city {city}')
        Graph_for_ind(city,'city')
        cd = 1
        for district in districts:

            print(f'City {cc} out of {len(cities)}  | District {cd} out of {len(districts)}')
            Graph_for_ind(district,'district')
            
            cd = cd + 1
        cc = cc + 1