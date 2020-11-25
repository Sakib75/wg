import pandas
from pandas import read_csv
from matplotlib import pyplot
from matplotlib.backends.backend_pdf import PdfPages
import datetime

# Specify KPI Type

KPI_names = ['Average price','Average size','Average €/qm','Count furnished','Count unfurnished']
def get_month(timestamps):
	months = []
	for time in timestamps:
		date = time.split()[0].split('.')
		date = datetime.datetime(int(date[2]),int(date[1]),int(date[0]))
		month = date.strftime("%b")
		year = date.strftime("%Y")

		date_string = f"{month} {year}"

		months.append(date_string)
	return months


series = read_csv('pre_calculation(district).csv')

with PdfPages('Report_for_Offers(district_based).pdf') as pdf:

    cities = series.City.unique()
    
    cc = 1
    for city in cities:
        
        city_data = series.loc[series['City'] == city]
        districts = city_data.District.unique()
        cd = 1
        for district in districts:

            print(f'City {cc} out of {len(cities)}  | District {cd} out of {len(districts)}')
            
            district_data = series.loc[series['District']==district]
            timestamps = district_data['Timestamp'].unique()

            furnished = district_data.loc[district_data['KPI Name'] == 'Count furnished'].Result.tolist()
            unfurnished = district_data.loc[district_data['KPI Name'] == 'Count unfurnished'].Result.tolist()

            count = [x + y for x, y in zip(furnished, unfurnished)]
            index = get_month(timestamps)
            for kpi in KPI_names:
                fig, axs = pyplot.subplots()
                data = {
                    kpi: district_data.loc[district_data['KPI Name'] == kpi].Result.tolist(),
                }


                dataFrame = pandas.DataFrame(data=data, index=index)

                #Background 
                color = 'tab:blue'
                axs.set_xlabel('Month', fontsize='large', fontweight='bold')
                
                axs.set_ylabel('Measure\'s value',color=color, fontsize='large', fontweight='bold')
                axs.tick_params(axis='y', colors=color)

                dataFrame.plot.bar(ax=axs,rot=15, title=f"Timeseries analysis for {city}: {district}")

                x1 = []

                ax2 = axs.twinx()
                
                color = 'tab:red'
                ax2.tick_params(axis='y', colors=color)
                ax2.set_ylabel('Count',color=color, fontsize='large', fontweight='bold')
                for i in range(0,len(count)):
                    x1.append(i)               
                y1 = count


                #Foreground

                ax2.plot(x1, y1,color=color)
                ax2.set_ylim(ymin=0)
                fig.tight_layout()
                pdf.savefig()
                pyplot.close()
            cd = cd + 1
        cc = cc + 1