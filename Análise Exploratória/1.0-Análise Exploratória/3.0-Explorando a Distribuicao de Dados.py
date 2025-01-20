import locale
from pathlib import Path

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

STATE_CSV = DATA / 'state.csv'
WORLD_BANK_DATASET = DATA / 'world_bank_dataset.csv'
state_data = pd.read_csv(STATE_CSV)
world_bank_data = pd.read_csv(WORLD_BANK_DATASET)
brazil_data = world_bank_data[world_bank_data['Country'] == 'Brazil']
usa_data = world_bank_data[world_bank_data['Country'] == 'United States']
sorted_brazil_population = sorted(brazil_data['Population'] / 1_000_000)
sorted_brazil_unemployment_rate = sorted(brazil_data['Unemployment Rate (%)'])
sorted_usa_unemployment_rate = sorted(usa_data['Unemployment Rate (%)'])
sorted_world_bank_data_population = sorted(world_bank_data['Population'] / 1_000_000)

# Percentis e Boxplots 
print(sorted_usa_unemployment_rate)
# Percentiles Murder.Rat
print("Percentiles Murder.Rate state_data:\n", state_data['Murder.Rate'].quantile([0.05, 0.25, 0.5, 0.75, 0.95]))
ax = (state_data['Population']/1_000_000).plot.box(figsize=(3,4))
ax.set_ylabel('Population (millions)')

plt.tight_layout()
plt.show()

# Percentiles Unployment Rate Brazil
print("Percentiles sorted_brazil_unemployment_rate:", np.quantile(sorted_brazil_unemployment_rate, [0.05, 0.25, 0.5, 0.75, 0.95]))
ax = pd.Series(sorted_world_bank_data_population).plot.box(figsize=(3,4))
ax.set_ylabel('Population (Millions)')

plt.tight_layout()
plt.show()

# Boxplot comparando taxa de desemprego do Brasil e EUA
# Primeiro preparar os dados para o boxplot 
# A parte whiskers superior mostra o percentil maximo dos dados
# A parte whiskers inferior mostra o percentil minimo dos dados
# A caixa em si, mostra a mediana que é a linha do meio, a parte abaixo da mediana é o Q1 e a parte 
# superior é o Q3
# Se houverem pontos depois ou antes dos whiskers, eles serão os outliers


data = {
    'Country': ['Brazil'] * len(sorted_brazil_unemployment_rate) + ['USA'] * len(sorted_usa_unemployment_rate),
    'Unemployment Rate (%)': sorted_brazil_unemployment_rate + sorted_usa_unemployment_rate
}

# Criar o data frame com o pandas 
df = pd.DataFrame(data)

# Criar boxplot
plt.figure(figsize=(6, 4))
ax = df.boxplot(by='Country', column='Unemployment Rate (%)', grid=False)
plt.title('Unemployment Rate (%) by Country')
plt.ylabel('Unemployment Rate (%)')
plt.tight_layout()
plt.show()


# Boxplot escolas
# Dados fictícios de exemplo
data = {
    'Escola': ['A'] * 100 + ['B'] * 100,
    'Nota': [50, 60, 70, 80, 90] * 20 + [30, 40, 50, 60, 70] * 20
}

dfescola = pd.DataFrame(data)

# Criar o boxplot
plt.figure(figsize=(8, 5))
sns.boxplot(x='Escola', y='Nota', data=dfescola, palette="Pastel1")
plt.title('Distribuição de Notas por Escola')
plt.xlabel('Escola')
plt.ylabel('Notas')
plt.show()

# Tabela de frequência e Histogramas
# Tabela de frequência irá mostrar quantos dados atingem aquele valor mostrado na tabela
# Na tabela 1.5 mostra quais estados atingem o valor mostrado
binnedPopulation = pd.cut(state_data['Population'], 10)
print(binnedPopulation.value_counts())

# Table 1.5
binnedPopulation.name = 'binnedPopulation'
df = pd.concat([state_data, binnedPopulation], axis=1)
df = df.sort_values(by='Population')
groups = []
for group, subset in df.groupby(by='binnedPopulation', observed=False):
    groups.append({
        'BinRange': group,
        'Count': len(subset),
        'States': ','.join(subset.Abbreviation)
    })
print(pd.DataFrame(groups))

# _Pandas_ also supports histograms for exploratory data analysis.
# Histograma é um gráfico que segue o raciocinio da tabela de frequência
# Nele não são excluidos os espaços em branco 

ax = (state_data['Population'] / 1_000_000).plot.hist(figsize=(4, 4))
ax.set_xlabel('Population (millions)')

plt.tight_layout()
plt.show()

ax2 = (world_bank_data['Population'] / 1_000_000).plot.hist(figsize=(6,6))
ax.set_label('Population (millions)')
plt.tight_layout()
plt.show()

ax3 = (dfescola[dfescola['Escola']=='A']['Nota']).plot.hist(figsize=(4,4))
ax3.set_label('Notas (Escola A)')
plt.tight_layout()
plt.show()

# Estimativas de densidade

ax = state_data['Murder.Rate'].plot.hist(density=True, xlim=[0, 12], 
                                    bins=range(1,12), figsize=(4, 4))
state_data['Murder.Rate'].plot.density(ax=ax)
ax.set_xlabel('Murder Rate (per 100,000)')

plt.tight_layout()
plt.show()