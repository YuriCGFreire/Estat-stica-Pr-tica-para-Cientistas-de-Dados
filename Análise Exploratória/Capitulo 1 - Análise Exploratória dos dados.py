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
# print("Media populacao: ", state_data['Population'].mean())

# Média aparada
# Exclui uma quantidade fixa de valores das pontas e então tira a média dos valores restantes
# Fazer isso elimina a influência de valores extremos
# print("Media aparada da populacao: ", trim_mean(state_data['Population'], 0.1))

# Mediana e estimativas robustas 
# Mediana é chamada de estimativa robusta pois não é influenciável por outliers (casos extremos)
# Mediana é o numero central dos dados classificados. Se a quantidade de numeros for par, 
# é pego os dois valores centrais e feito a média deles. 
# print("Mediana: ", state_data['Population'].median())

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

print("Desvio padrao da populacao: ", state_data['Population'].std())

# Desvio absoluto mediano da mediana
# As estimativas de variabilidade acima são sensíveis a outliers. 
# Um estimativa robusta é o Desvio absoluto mediano da mediana
# A mediana das diferenças dos valores observados menos a mediana
# [1 - 4 = 3, 4 - 4 = 0, 4 - 4 = 0] = [0,0,3] = 3
# Obs: O valor certo de 1 - 4 é -3, porem como é o desvio absoluto, aqui é ignorado o simbolo negativo

print("Desvio absoluto mediano da mediana da populacao: ", robust.scale.mad(state_data['Population']))