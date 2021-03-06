import pandas
from pandas import read_csv
from matplotlib import pyplot
from matplotlib.backends.backend_pdf import PdfPages
import datetime
import matplotlib.dates as mdates
from pylab import MaxNLocator
pandas.options.mode.chained_assignment = None 

# Set parameters

yearly_sampling = True
cleansing_data = True
foreground_opacity = 1.0


KPI_names = ['Average price','Average size','Average €/qm','Count furnished','Count unfurnished']
def get_month(time):
    date = time.split()[0].split('.')
    date = datetime.datetime(int(date[2]),int(date[1]),int(date[0]))
    month = date.strftime("%b")
    year = date.strftime("%Y")
    date_string = f"{month} {year}"
    return date_string

def get_year(time):
    date = time.split()[0].split('.')
    date = datetime.datetime(int(date[2]),int(date[1]),int(date[0]))
    year = date.strftime("%Y")
    date_string = f"{year}"
    return date_string

def get_timing_month(date):
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

def get_timing_year(date):
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
    date_string = get_year(date_string)
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


def Include_Empty_months(data,ys):
    if(ys == True):
        month_range = pandas.date_range(start=list(data.keys())[0], end=list(data.keys())[-1], freq='MS').strftime('%Y').tolist()
    else:
        month_range = pandas.date_range(start=list(data.keys())[0], end=list(data.keys())[-1], freq='MS').strftime('%b %Y').tolist()
    final_data = pandas.Series(data, index=month_range).fillna(0).to_dict()
    return final_data

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

def Graph_for_ind(d,type,ys):
    
    if(type == 'district'):
        district_data = city_data.loc[city_data[type].str.lower().str.contains(district.lower().replace('?',''))]
    elif(type == 'city'):
        district_data = city_data.loc[city_data['city'] == city]

    district_data['online_for'] = district_data['online_for'].apply(get_timing_year) if ys else district_data['online_for'].apply(get_timing_month)

    months = district_data['online_for'].unique().tolist()
    if(ys == True):
        months.sort(key = lambda date: datetime.datetime.strptime(date, '%Y'))
    else:
        months.sort(key = lambda date: datetime.datetime.strptime(date, '%b %Y'))
    final_data = {'Average Price': {},'Average Size': {}, 'Average €/qm': {},'Count Furnished': {}, 'Count Unfurnished': {}}            
    for month in months:
        month_data = district_data.loc[district_data['online_for'] == month]
        kpis = Analyze_data(month_data)
        index = months
        for kpi in kpis:
            final_data[kpi][month] = kpis[kpi]
    count = [x + y for x, y in zip(list(final_data['Count Furnished'].values()), list(final_data['Count Unfurnished'].values()))]
    count_map = Include_Empty_months(dict(zip(months,count)),ys) 
    for k in final_data:
        final_data[k] = Include_Empty_months(final_data[k],ys)
        data = list(final_data[k].values())
        index = list(final_data[k].keys())
        width = len(index) * 0.3
        if(width < 15):
            width = 15
        fig, axs = pyplot.subplots(figsize=(width, 5))
        dataFrame = pandas.DataFrame(data={k:data}, index=index)
        color = 'tab:blue'
        dataFrame.plot.bar(ax=axs, width=0.9, title=f"{'Yearly' if ys else 'Monthly'} analysis for {city}: {d} ({k})",alpha=foreground_opacity)
        axs.tick_params(axis='y', colors=color)

        axs.set_ylabel('Measure\'s value',color=color, fontsize='large', fontweight='bold')
        axs.set_ylim(ymin=0)     
        yb = axs.get_yaxis()
        yb.set_major_locator(MaxNLocator(integer=True))
        ax2 = axs.twinx()
        color = 'tab:red'
        ax2.set_xlabel('Month', fontsize='large', fontweight='bold')
        ax2.set_ylabel('Count',color=color, fontsize='large', fontweight='bold')
        ya = ax2.get_yaxis()
        ya.set_major_locator(MaxNLocator(integer=True))
        axs.grid(axis='y')
        ax2.plot(list(count_map.keys()), list(count_map.values()),color=color)
        ax2.set_ylim(ymin=0)                        
        ax2.format_xdata = mdates.DateFormatter('%b %Y')

        fig.autofmt_xdate() 
        fig.tight_layout()
        pdf.savefig()
        pyplot.close()

series = read_csv('Requests.csv')

with PdfPages('Report_for_Requests(district_based).pdf') as pdf:

    cities = series.city.unique()
    valid_district_data = pandas.read_csv(r'valid_district_postal\Mapping_Stadtteil_PLZ.csv')
    cc = 1
    for city in cities:
        city_data = series.loc[series['city'] == city]
        districts = get_districts(city_data.district.unique())
        print(f'\nPlotting graph for city: {city}')
        if(yearly_sampling == True):
            for ys in [True,False]:
                Graph_for_ind(city,'city',ys)
        else:
            Graph_for_ind(city,'city',False)
        valid_district_data_per_city = valid_district_data.loc[valid_district_data['Stadt'] == city]
        valid_district_list = list(map(str, valid_district_data_per_city['Stadtteil'].tolist()))
        all_district_name = get_districts(city_data.district.unique())
        
        print(f'Number of total district existing in Offers.csv : {len(all_district_name)}')
        if(cleansing_data == True and len(valid_district_list) > 0):
            districts = set(intersection(valid_district_list, all_district_name))
        
        print(f'Number of total district existing in Offers.csv (After cleansing) : {len(districts)}')
        
        
        cd = 1
        for district in districts:
            print(f'City {cc} out of {len(cities)}  | District {cd} out of {len(districts)}')       
            
            if(yearly_sampling == True):
                for ys in [True,False]:
                    Graph_for_ind(district,'district',ys)
            else:
                Graph_for_ind(district,'district',False)
            
            cd = cd + 1
        cc = cc + 1