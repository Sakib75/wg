import pandas
from pandas import read_csv
from matplotlib import pyplot
from matplotlib.backends.backend_pdf import PdfPages
import datetime
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
pandas.options.mode.chained_assignment = None  # default='warn'
# Specify KPI Type
cleansing_data = True
KPI_names = ['Average Price','Average Size','Average €/qm','Count furnished','Count unfurnished']
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

                    # average_size[month] = kpis['Average Size']
                    # average_price_per_qm[month] = kpis['Average €/qm']
                    # fur_yes[month] = kpis['Count Furnished']
                    # fur_no[month] = kpis['Count Unfurnished']

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
                    
                    dataFrame.plot.bar(ax=axs,rot=15, title=f"Timeseries analysis for {city}: {pd}")

                     

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

def intersection(lst1, lst2):

        lst3 = [value for value in lst1 if value in lst2]
        return lst3


series = read_csv('Offers.csv')

with PdfPages('Report_for_Offers(postal_code_based).pdf') as pdf:
    cities = series.city.unique()
    valid_postal_data = pandas.read_csv(r'valid_district_postal\Mapping_Stadtteil_PLZ.csv')
    cc = 1
    for city in cities:       
        city_data = series.loc[series['city'] == city]
        postals = list(map(str,city_data.postal_code.unique().tolist()))

        valid_postal_data_per_city = valid_postal_data.loc[valid_postal_data['Stadt'] == city]
        valid_postal_list = list(map(str, valid_postal_data_per_city['PLZ'].tolist()))    
        
        print(f'Number of total postals existing in Offers.csv : {len(postals)}')

        if(cleansing_data == True and len(valid_postal_list) > 0):
            postals = set(intersection(valid_postal_list, postals))
        
        print(f'Number of total postals existing in Offers.csv (After cleansing) : {len(postals)}')
 

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
        
        cd = 1
        for district in districts:

            print(f'City {cc} out of {len(cities)}  | District {cd} out of {len(districts)}')
            Graph_for_ind(district,'district')
            
            cd = cd + 1
        cc = cc + 1