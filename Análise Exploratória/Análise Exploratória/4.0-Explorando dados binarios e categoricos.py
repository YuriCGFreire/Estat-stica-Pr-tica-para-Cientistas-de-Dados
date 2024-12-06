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

AIRPORT_DELAYS_CSV = DATA / 'dfw_airline.csv'
HOUSING = DATA / 'Housing.csv'
dfw = pd.read_csv(AIRPORT_DELAYS_CSV)
df_housing = pd.read_csv(HOUSING)

# Explorando dados binários e categóricos
# Para dados categóricos, proporções simples ou porcentagens, conte o histórico dos dados
# Para encontrar um resumo de dados binários ou categóricos basta contar a proporção de 1s ou das categorias importantes
# Na tabela abaixo os dados de atraso de voos do aeroporto sao divididos e categorizados em "Companhia Aerea", atraso no sistema de controle de trafego aereo, clima, segurança ou entrada

print(100 * dfw / dfw.values.sum())
# Uma boa forma de visualizar essa informação é usando graficos de barra 
# Onde no eixo X mostra a categoria e no eixo Y mostra o historico dos dados, a quantidade de vezes que ele ocorreu
ax = dfw.transpose().plot.bar(figsize=(4, 4), legend=False)
ax.set_xlabel('Cause of delay')
ax.set_ylabel('Count')

plt.tight_layout()
plt.show()
