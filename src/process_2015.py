# Process the raw 2015 electoral district data into a simpler form.
# Should be used with the data from
# https://www.elections.ca/res/rep/off/ovr2015app/41/data_donnees/pollbypoll_bureauparbureauCanada.zip

from os import walk, path

import pandas as pd

# Read in each district and aggregate it.
district_headers = ['prov', 'name', 'votes', 'cpc', 'ndp', 'lpc', 'bq', 'gpc', 'other']
districts = pd.DataFrame(columns=district_headers)

(dirpath, _, district_files) = next(walk('data/2015/'))
headers = ['id', 'name', 'party', 'votes']
parties = {
    'Conservative': 'cpc',
    'NDP-New Democratic Party': 'ndp',
    'Liberal': 'lpc',
    'Green Party': 'gpc',
    'Bloc Québécois': 'bq',
}
keep_columns = [0, 1, 13, 17]
for f in district_files:
    df = pd.read_csv(
        path.join(dirpath, f),
        header=0,
        names=headers,
        usecols=keep_columns,
    )
    group_by_party = df.groupby('party', sort=False)
    parties_by_vote = group_by_party.agg({
        'id': 'first',
        'name': 'first',
        'votes': 'sum',
    })

    district = {
        'id': [parties_by_vote['id'].iloc[0]],
        'name': [parties_by_vote['name'].iloc[0]],
        'other': [0],
        'cpc': [0],
        'lpc': [0],
        'ndp': [0],
        'gpc': [0],
        'bq': [0],
    }
    votes = 0
    for (party, series) in parties_by_vote.iterrows():
        votes += series['votes']
        if party in parties:
            district[parties[party]][0] = series['votes']
        else:
            district['other'][0] += series['votes']
    district['votes'] = [votes]
    district['prov'] = [int(str(district['id'][0])[:2])]

    districts = districts.append(pd.DataFrame.from_records(district, index='id'))

districts.to_csv('data/results_2015.csv', index_label='id', columns=district_headers)
