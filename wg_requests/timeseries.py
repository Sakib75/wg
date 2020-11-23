import pandas
from pandas import read_csv
from matplotlib import pyplot
from matplotlib.backends.backend_pdf import PdfPages
import datetime

# Specify KPI Type
foreground_indicator = 5
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



series = read_csv('pre_calculation.csv')

with PdfPages('Report_Requests(district_based).pdf') as pdf:
    cities = series.City.unique()
    for city in cities:
        districts = series.District.unique()
        for district in districts:
            postal_data = series.loc[series['District']==district]
            timestamps = postal_data['Timestamp'].unique()

            furnished = postal_data.loc[postal_data['KPI Name'] == 'Count furnished'].Result.tolist()
            unfurnished = postal_data.loc[postal_data['KPI Name'] == 'Count unfurnished'].Result.tolist()

            count = [x + y for x, y in zip(furnished, unfurnished)]
            index = get_month(timestamps)
            for kpi in KPI_names:
                fig, axs = pyplot.subplots()
                data = {
                    kpi: postal_data.loc[postal_data['KPI Name'] == kpi].Result.tolist(),
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