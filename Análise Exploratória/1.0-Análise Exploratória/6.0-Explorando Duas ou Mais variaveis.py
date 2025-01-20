import locale
from pathlib import Path
from matplotlib.collections import EllipseCollection
from matplotlib.colors import Normalize

import pandas as pd
import numpy as np
from scipy.stats import trim_mean
from statsmodels import robust
import wquantiles

import seaborn as sns
import matplotlib.pylab as plt

try:
    import common 
    DATA = common.dataDirectory()
except ImportError:
    DATA = Path().resolve() / 'data' 

KC_TAX_CSV = DATA / 'kc_tax.csv.gz'
kc_tax = pd.read_csv(KC_TAX_CSV)

# Media e variância analisam uma variavel por vez (analise univariada)
# Correlação compara duas variaveis (analise bivariada)
# Nesta seção veremos analise multivariada

# Compartimentação hexagonal e contornos 
# Para um numero grande de registros um grafico de dispersão não é bom
# O codigo abaixo pega as casas que tenham um imposto menor que 750000 e as casas que sao maiores que 100 pés e menores que 3500
kc_tax0 = kc_tax.loc[(kc_tax.TaxAssessedValue < 750000) & 
                     (kc_tax.SqFtTotLiving > 100) &
                     (kc_tax.SqFtTotLiving < 3500), :]

ax = kc_tax0.plot.hexbin(x='SqFtTotLiving', y='TaxAssessedValue',
                         gridsize=30, sharex=False, figsize=(5, 4))
ax.set_xlabel('Finished Square Feet')
ax.set_ylabel('Tax Assessed Value')

plt.tight_layout()
plt.show()

# The _seaborn_ kdeplot is a two-dimensional extension of the density plot. The calculation of the 2D-density for the full dataset takes several minutes. It is sufficient to create the visualization with a smaller sample of the dataset. With 10,000 data points, creating the graph takes only seconds. While some details may be lost, the overall shape is preserved.

fig, ax2 = plt.subplots(figsize=(4, 4))
sns.kdeplot(data=kc_tax0.sample(10000), x='SqFtTotLiving', y='TaxAssessedValue', ax=ax2)
ax2.set_xlabel('Finished Square Feet')
ax2.set_ylabel('Tax Assessed Value')

plt.tight_layout()
plt.show()

# Visualizando variáveis multiplas 
# No exemplo acima foi feito o relacionamento entre metros quadrados e valor dos impostos
# Porem se levarmos em consideração a localização de cada casa, teremos mais detalhamento
# O imposto é mais caro em alguns codigos postais do que outros 

zip_codes = [98188, 98105, 98108, 98126]
kc_tax_zip = kc_tax0.loc[kc_tax0.ZipCode.isin(zip_codes),:]
kc_tax_zip

def hexbin(x, y, color, **kwargs):
    cmap = sns.light_palette(color, as_cmap=True)
    plt.hexbin(x, y, gridsize=25, cmap=cmap, **kwargs)

g = sns.FacetGrid(kc_tax_zip, col='ZipCode', col_wrap=2)
g.map(hexbin, 'SqFtTotLiving', 'TaxAssessedValue', 
      extent=[0, 3500, 0, 700000])
g.set_axis_labels('Finished Square Feet', 'Tax Assessed Value')
g.set_titles('Zip code {col_name:.0f}')

plt.tight_layout()
plt.show()