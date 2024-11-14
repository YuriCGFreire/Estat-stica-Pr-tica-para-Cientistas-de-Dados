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
state_data = pd.read_csv(STATE_CSV)

# Estimativa de localização
# Um passo fundamental é definir um valor típico para cada carcterística
# Uma estimativa de onde a maioria dos dados está localizada
# Ou seja, sua tendencia central 

# Média
# Estimativa de localização mais básica 
# Soma de todos os valores, divida pela quantidade de valores

print("Media populacao: ", state_data['Population'].mean())

# Média aparada
# Exclui uma quantidade fixa de valores das pontas e então tira a média dos valores restantes
# Fazer isso elimina a influência de valores extremos

print("Media aparada da populacao: ", trim_mean(state_data['Population'], 0.1))

# Mediana e estimativas robustas 
# Mediana é chamada de estimativa robusta pois não é influenciável por outliers (casos extremos)
# Mediana é o numero central dos dados classificados. Se a quantidade de numeros for par, 
# é pego os dois valores centrais e feito a média deles. 

print("Mediana: ", state_data['Population'].median())

# Média ponderada
# A soma da multiplicação de um dado por um peso dividido pela soma dos pesos.
# x*w / soma(todos os pesos)
print("Media ponderada da populacao: ", np.average(state_data['Murder.Rate'], weights=state_data['Population']))

# Mediana ponderada
print("Mediana ponderada: ", wquantiles.median(state_data['Murder.Rate'], weights=state_data['Population']))