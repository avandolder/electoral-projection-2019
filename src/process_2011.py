# Process 2011 electoral data transposed to 2015 ridings.
# Should be used with the data from
# https://www.elections.ca/res/cir/trans2013/includes/downloadCSV.asp?zip=10&lang=e&choice=form2&mysubmit=Download%A0Grouped+Polling+Divisions

import pandas as pd

column_names = ['prov', 'id', 'name', 'votes', 'cpc', 'ndp', 'lpc', 'bq', 'gpc', 'other']
keep_columns = [0, 1, 2, 14, 15, 16, 17, 18, 19, 20]
initial_data = pd.read_csv(
    'data/TRANSPOSITION_338FED.csv',
    header=0,
    names=column_names,
    usecols=keep_columns,
)
grouped_districts = initial_data.groupby('id', sort=False)
districts = grouped_districts.agg({
    'prov': 'first',
    'name': 'first',
    'votes': sum,
    'cpc': sum,
    'ndp': sum,
    'lpc': sum,
    'bq': sum,
    'gpc': sum,
    'other': sum,
})
districts.to_csv('data/results_2011.csv')
