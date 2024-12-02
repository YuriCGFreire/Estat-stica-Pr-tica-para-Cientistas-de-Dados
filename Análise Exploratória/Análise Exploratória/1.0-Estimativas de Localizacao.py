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
# Um passo fundamental na exploração de dados é definir um valor típico para cada carcterística (variável)
# Uma estimativa de onde a maioria dos dados está localizada
# Ou seja, sua tendencia central
# Apesar de ser simples de computar e ser conveniente, nem sempre é a melhor medida para um valor central

# Média
# Estimativa de localização mais básica 
# Soma de todos os valores, divida pela quantidade de valores

# Exemplo de código de Média
print("Media da populacao (State data): ", state_data["Population"].mean() / 1_000_000)

# No exemplo abaixo há dados que são outliers
print("Media populacao Brazil ", brazil_data['Population'].mean() / 1_000_000)

# Média aparada
# Exclui uma quantidade fixa de valores das pontas (Do começo e do final) e então tira a média dos valores restantes
# Fazer isso elimina a influência de valores extremos (ouliers)
# Os dados precisam estar classificados

# Media aparada state_data
print("Media aparada da populacao (state data): ", trim_mean(sorted(state_data['Population'] / 1_000_000), proportiontocut=0.1))

# Media aparada brazil_data 
print("Media aparada da populacao (brazil_data): ", trim_mean(sorted(brazil_data['Population'] / 1_000_000), proportiontocut=0.2))

# Média ponderada
# A somatoria da multiplicação de um dado por um peso, dividido pela soma dos pesos.
# x*w / soma(todos os pesos)
# Razões principais para o uso da média ponderada: 
# Observações altamente variáveis recebem um peso menor
# Os dados coletados não representam igualmente os diferentes grupos que estamos interessados em medir.

# Media ponderada state_data Murder.Rate 
print("Media ponderada da taxa de assassinato em relacao a populacao: ", np.average(state_data['Murder.Rate'], weights=state_data['Population']))

# Media pondera brazil_data life expectancy em population
print("Media ponderada da taxa de vida em relacao a populacao: ", np.average(brazil_data['Life Expectancy'], weights=brazil_data['Population'])) 

# Mediana e estimativas robustas 

# Mediana é o número central em um lista de dados classificadas. Se houver um numero para de valores de dados 
# é feito a média dos dois valores centrais dos dados classificados
# Também há a mediana ponderada que é a metade da somas dos pesos dos valores classificados e então encontrado
# o menor valor que atinge a metade das somas dos pesos
# Mediana é chamada de estimativa robusta pois não é influenciável por outliers (casos extremos)

# Mediana da população em state_data
# print(sorted(state_data['Population'] / 1_000_000))
print("Mediana da populacao em state_data: ", state_data['Population'].median() / 1_000_000)

# Mediana da populcação em brazil_data
# print(sorted(brazil_data['Population'] / 1_000_000 ))
print("Mediana da populacao em brazil_data: ", brazil_data['Population'].median() / 1_000_000)

# Mediana ponderada da população em state_data
print("Mediana ponderada da populacao em state_data: ", wquantiles.median(state_data['Murder.Rate'], weights=state_data['Population']))

# Mediana ponderada da populcação em brazil_data
print("Mediana ponderada da populacao em brazil_data: ", wquantiles.median(brazil_data['Life Expectancy'], weights=brazil_data['Population']))

