import locale
from pathlib import Path
from matplotlib.collections import EllipseCollection
from matplotlib.colors import Normalize

import pandas as pd
import numpy as np
from scipy.stats import trim_mean
from statsmodels import robust
import wquantiles
from sklearn.utils import resample

import seaborn as sns
import matplotlib.pylab as plt

try:
    import common 
    DATA = common.dataDirectory()
except ImportError:
    DATA = Path().resolve() / 'data' 

LOANS_INCOME_CSV = DATA / 'loans_income.csv'

loans_income = pd.read_csv(LOANS_INCOME_CSV).squeeze('columns')

# sample_data = pd.DataFrame({
#     'income': loans_income.sample(1000),
#     'type': 'Data',
# })

# sample_mean_05 = pd.DataFrame({
#     'income': [loans_income.sample(5).mean() for _ in range(1000)],
#     'type': 'Mean of 5',
# })

# sample_mean_20 = pd.DataFrame({
#     'income': [loans_income.sample(20).mean() for _ in range(1000)],
#     'type': 'Mean of 20',
# })

# results = pd.concat([sample_data, sample_mean_05, sample_mean_20])
# print(results.head())

# g = sns.FacetGrid(results, col='type', col_wrap=1, 
#                   height=2, aspect=2)
# g.map(plt.hist, 'income', range=[0, 200000], bins=40)
# g.set_axis_labels('Income', 'Count')
# g.set_titles('{col_name}')

# plt.tight_layout()
# plt.show()


## Bootstrap

results = [] 
for nrepeat in range(1000):
    sample = resample(loans_income)
    results.append(sample.median())
results = pd.Series(results)
print('Bootstrap Statistics:')
print(f'original: {loans_income.median()}')
print(f'bias: {results.mean() - loans_income.median()}')
print(f'std. error: {results.std()}')