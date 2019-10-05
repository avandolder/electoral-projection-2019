# Generate provinicial results for the 2011 and 2015 elections.

import pandas as pd

def provincial_results(data: pd.DataFrame) -> pd.DataFrame:
    return data.groupby('prov').agg({
        'votes': 'sum',
        'cpc': 'sum',
        'lpc': 'sum',
        'ndp': 'sum',
        'gpc': 'sum',
        'bq': 'sum',
        'other': 'sum',
    })

if __name__ == '__main__':
    provincial_results(pd.read_csv('data/results_2011.csv')).to_csv('data/provincial_results_2011.csv')
    provincial_results(pd.read_csv('data/results_2015.csv')).to_csv('data/provincial_results_2015.csv')
