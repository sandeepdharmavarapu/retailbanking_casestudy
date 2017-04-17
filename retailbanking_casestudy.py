import pandas as pd
import numpy as np
import sys
from datetime import datetime
import csv
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

import plotly as plotly
import plotly.plotly as py
import plotly.tools as plotly_tools
from plotly.graph_objs import *

plotly.tools.set_credentials_file(username='sandeepdharmavarapu', api_key='DFi5qZEh4QVhu0KX4bzO')
py.sign_in("sandeepdharmavarapu", "DFi5qZEh4QVhu0KX4bzO")
plotly.tools.set_config_file(world_readable=True, sharing='public')


f = pd.read_csv('daily_trans.csv')

#convert the Dormancy.csv file into a dictionary
with open('dormancy.csv', mode='r') as infile:
    reader = csv.reader(infile)
    with open('dormancy_new.csv', mode='w') as outfile:
        writer = csv.writer(outfile)
        mydict = {rows[0]:int(rows[1]) for rows in reader}

#Groupby Business unit, Merchant id and Card number and place all the transaction dates in a list for the corresponding key
r2  = f.groupby(['Business_unit','Merch_id', 'Card_num'])['Trans_date'].apply(list)

#reset the index
r4 = r2.reset_index()



# set a report generation date
report_gendt = '2015-04-01'
d1 = datetime.strptime(report_gendt, "%Y-%m-%d")

#create a variable in the r4 dataframe
state = []
print(sys.argv)
print('hi')

#loop thru r4 rows
for index, row in r4.iterrows():

	# finding the difference between the report generation date and recent transaction date
	#need to find the date which is maximum of all dates and smaller than the report generation date
	d2=pd.DataFrame(columns = ['A'])

	#d2 = datetime.strptime(max(row['Trans_date']), "%Y-%m-%d")
	for date1 in row['Trans_date']:
		t=pd.DataFrame([datetime.strptime(date1, "%Y-%m-%d")], columns = ['A'])
		d2 = d2.append(t, ignore_index=True)	
	d3 = d2.loc[d2['A'] < report_gendt]
	if d3.empty:
		pass
	else:	
		d4 = max(d3['A'])
		diff = abs((d4-d1).days)
	

	if (diff >= mydict[str(row['Merch_id'])]) & (diff < 90):
		state.append('dormant')
	elif (diff >= 90) | (d3.empty):
		state.append('new')
	elif diff < mydict[str(row['Merch_id'])]:
		state.append('active')
	else:
		print(row['Merch_id'], diff, mydict['99993'])	


#print(r4)
r4['state'] = state	

#print(r4)	


# Plotly
#merchlist = [99999, 99998, 99997, 99996, 99995, 99994, 99993, 99992, 99991, 100000]
merchlist = set(r4['Merch_id'])
print(merchlist)
r5=[]
for i in merchlist:
	r5.append(len(r4.loc[(r4['state']=='dormant') & (r4['Merch_id'] == i) & (r4['Business_unit'] == int(sys.argv[1]))]))


pichart = {
    'data': [{'labels': ['99991', '99992', '99993', '99994','99995','99996','99997','99998','99999', '100000'],
              'values': r5,
              'type': 'pie'}],
    'layout': {'title': 'Dormant customer count for Business Unit - %s' % sys.argv[1] }
     }

py.iplot(pichart)


