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

# Estimativa de localização
# Um passo fundamental é definir um valor típico para cada carcterística (variável)
# Uma estimativa de onde a maioria dos dados está localizada
# Ou seja, sua tendencia central 

# Média
# Estimativa de localização mais básica 
# Soma de todos os valores, divida pela quantidade de valores
# print("Media populacao: ", state_data['Population'].mean())
# brazil_data.loc[:, 'GDP (USD)'] = brazil_data['GDP (USD)'].apply(
#     lambda x: f"{x / 1_000_000_000_000:.2f} T"
# )
# print(brazil_data[['Year', 'Unemployment Rate (%)']].sort_values(by='Unemployment Rate (%)'))
# print("Media de desemprego do Brazil: ")
# print()
# print(brazil_data['GDP (USD)'].mean())

# print("Pib Brazil")
# locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
# print(brazil_data[['Year', 'GDP (USD)']].sort_values(by='GDP (USD)').sort_values(by= 'GDP (USD)'))
# print("Media do pib Brazil: ")
# print(brazil_data['GDP (USD)'].mean() / 1_000_000_000_000)




# Média aparada
# Exclui uma quantidade fixa de valores das pontas e então tira a média dos valores restantes
# Fazer isso elimina a influência de valores extremos
# print("Media aparada da populacao: ", trim_mean(state_data['Population'], 0.1))
# print("Media aparada do PIB do Brasil: ")
# print(trim_mean(brazil_data['GDP (USD)'], 0.1))

# Mediana e estimativas robustas 
# Mediana é chamada de estimativa robusta pois não é influenciável por outliers (casos extremos)
# Mediana é o numero central dos dados classificados. Se a quantidade de numeros for par, 
# é pego os dois valores centrais e feito a média deles. 
# print("Mediana: ", state_data['Population'].median())
# print("Mediana PIB Brasil: ", brazil_data['GDP (USD)'].median() / 1_000_000_000_000)

# Média ponderada
# A soma da multiplicação de um dado por um peso dividido pela soma dos pesos.
# x*w / soma(todos os pesos)
# print("Media ponderada da populacao: ", np.average(state_data['Murder.Rate'], weights=state_data['Population']))

# Mediana ponderada
# print("Mediana ponderada: ", wquantiles.median(state_data['Murder.Rate'], weights=state_data['Population']))


# Estimativas de variabilidade
# Variabilidade ou dispersão mede se os valores de dados estão compactados ou espalhados

# Desvio-padrão e Estimativas relacionadas 
# As estimativas de variação mais utilizadas são baseadas na estimativas de localização e dados classificados. 
# Dado os valores > [1, 4, 4] a média é 3
# Os desvios da média são as diferenças entre a média e os dados > [1 - 3 = -2, 4 - 3 = 1, 4 - 3 = 1]
# Eles nos mostram como os dados estão disperso em torno do valor central 

# Desvio absoluto médio
# Tirar a média dos valores absolutos dos desvios da média. Pegando o exemplo acima 
# (1 + 1 + 2) / 3 = 1.33

# Variância e desvio padrão
# Variância é calculada fazendo a soma dos quadrados do desvio da média dividido por n - 1 ou dividido por n
# ((-2**2) + (1**2) + (1**2)) / 2 obs: 2 aqui é a quantidade de valores - 1. Então 3 - 1

# Desvio padrão
# Raiz quadrada da variância 
# Pode parecer estranho que o desvio padrão seja o preferido na estatística ao invés do desvio absoluto médio, dado a sua formula
# print("Desvio padrao da populacao: ", state_data['Population'].std())

# Desvio absoluto mediano da mediana
# As estimativas de variabilidade acima são sensíveis a outliers. 
# Um estimativa robusta é o Desvio absoluto mediano da mediana
# A mediana das diferenças dos valores observados menos a mediana
# [1 - 4 = 3, 4 - 4 = 0, 4 - 4 = 0] = [0,0,3] = 3
# Obs: O valor certo de 1 - 4 é -3, porem como é o desvio absoluto, aqui é ignorado o simbolo negativo
# print("Desvio absoluto mediano da mediana da populacao: ", robust.scale.mad(state_data['Population']))
# print("Desvio absoludo mediano da mediana do PIB do Brasil: ", robust.scale.mad(brazil_data['GDP (USD)'])/1_000_000_000_000)

# Estimativa baseada em percentis
# Uma abordagem diferente para analisar a dispersão é com base na observação na distribuição em dados classificados. 
# E a medida mais basica é a amplitude que é a diferença entre o maior e o menor numero. Porém a amplitude é sensível a outliers e não é muito util na medida geral da dispersão dos dados. 
# print("Q1 da populacao: ", state_data['Population'].quantile(0.25))
# print("Q3 da populacao: ", state_data['Population'].quantile(0.75))
# print("Amplitude interquartil da populacao: ", state_data['Population'].quantile(0.75) - state_data['Population'].quantile(0.25))
# brazil_life_expectancy = brazil_data['Life Expectancy'].sort_values()
# print("Q1 Expectativa de vida Brasil: ", brazil_life_expectancy.quantile(0.25))
# print("Q3 Expectativa de vida Brasil: ", brazil_life_expectancy.quantile(0.75))
# print("Amplitude interquartil: ", brazil_life_expectancy.quantile(0.75) - brazil_life_expectancy.quantile(0.25))

# Explorando a Distribuição de Dados 
# As estimativas que vimos resume em um unico numero para descrever sua localização e variabilidade dos dados.

# Percentis e Boxplots
# Percentis podem ser usado para medir a dispersão, valiosos para resumir toda distribuição e para resumir as caudas (amplitude externa) da distribuição

# Percentis da taxa de homicidio por estado 
# print("Percentis da taxa de homicidio por estado: ")
# print(state_data['Murder.Rate'].quantile([0.05, 0.25, 0.5, 0.75, 0.95]))

# Percentis Emissão de CO2 Brasil
# print(brazil_data['CO2 Emissions (metric tons per capita)'])
# print((world_bank_data['Country','GDP (USD)']))

# Boxplot da população por estado
# ax = (state_data['Population']/1_000_000).plot.box(figsize=(3, 4))
# ax.set_ylabel('Population (millions)')

# plt.tight_layout()
# plt.show()
ax = (world_bank_data['Unemployment Rate (%)']).plot.box(figsize=(3,4))
ax.set_ylabel('GDP (Trillions)')
plt.tight_layout()
plt.show()

