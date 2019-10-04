# Process the raw 2015 electoral district data into a simpler form.

from os import walk, path

import pandas as pd

# Read in each district and aggregate it.
(path, _, district_files) = next(walk('data/2015/'))
headers = ['id', 'name', 'party', 'votes']
keep_columns = [0, 1, 13, 17]
for f in district_files:
    df = pd.read_csv(
        path.join(path, f),
        header=0,
        names=headers,
        usecols=keep_columns,
    )
    parties = df.groupby('party', sort=False)
    parties_by_vote = parties.agg({
        'id': 'first',
        'name': 'first',
        'votes': 'sum',
    })
