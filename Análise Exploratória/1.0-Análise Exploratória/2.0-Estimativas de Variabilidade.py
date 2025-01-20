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
sorted_brazil_population = sorted(brazil_data['Population'] / 1_000_000)



# A variabilidade ou também dispersão, é uma segunda dimensão na sumarização dos dados. Ela mede se os valores de dados estão compactados ou espalhados. 
# Da mesma forma que é maneiras diferentes de medir a localização (media, mediana etc) também há formas diferentes de medir a variabilidade. 

# Desvio padrão e Estimativas relacionadas
# As estimativas de dispersão mais utilizadas são baseados na diferença (ou desvio) da localização e os dados observados. 
# Dados os seguintes valores [1, 4, 4] a média é 3 e a mediana 4. Os desvios da média são 
# [1 - 3 = -2, 4 - 3 = 1, 4 - 3 = 1]. Eles no dizem o quanto os valores observados estão disperso em relação ao valor central (localização)

# Desvio padrão da população de state_data 
print("Desvio padrao da state_data: ", state_data['Population'].dropna().std() / 1_000_000)

# Desvio padrão da população do Brasil ao longo dos anos
print("Desvio padrao da populacao do Brasil ao longo dos anos: ", brazil_data['Population'].std() / 1_000_000)

# Desvio absoluto médio
# Porem a soma dos desvios da média é exatamente 0. Uma abordagem simples é tirar a média dos valores absoluto.
# Pegando os valores absolutos do exemplo anterior [1, 1, 2]. Somo-os 2 tiro sua média 1 + 1 + 2 / 3 = 1,33. 
# Isso é chaamado de desvio absoluto médio

# Variância
# A soma dos quadrados do desvio médio dividido pelo numero de valores dados (Observação existe a variancia populacional em que a soma dos quadrados do desvio médio é dividido por N sendo N a quantidade de valores e existe a variancia populacional que é dividido por n - 1). Peguemos os dados anteriores
# Desvio médio: [1 - 3 = -2, 4 - 3 = 1, 4 - 3 = 1] = [-2, 1, 1]
# Variância populacional = [-2**2 + 1**2 + 1**2] = 6 / 3 = 2
# Variância amostral = [-2**2 + 1**2 + 1**2] = 6 / 2 = 3

# Desvio padrão é a raiz quadrada da variância
# [-2**2 + 1**2 + 1**2] = 6 / 3 = raiz_quadrada(2) = 1,41

# Porem a variância e o desvio padrão não são robustos em relação a outliers. 
# Uma estimativa robusta a outliers é o desvio absoluto mediano da mediana
# Pegando os valores anteriores como exemplo
# [1, 4, 4] = [1 - 4, 4 - 4, 4 - 4] = MAD é igual a 0
# Outro exemplo
# [2, 4, 6, 8, 10] = mediana 6
# desvio absoluto mediano da mediana = [2 - 6 = 4, 4 - 6 = 2, 6 - 6 = 0, 8 - 6 = 2, 100 - 6 = 94] = [0, 2, 2, 4, 94] = 2

# Desvio absoluto mediano da mediana de state_data
print("Desvio absoluto mediano da mediana de state_data['Population']: ", robust.scale.mad(state_data['Population']/ 1_000_000))

# Desvio absoluto mediano da mediana de brazil_data['Population']
sorted_brazil_population_median = np.median(sorted_brazil_population);
absolute_deviation_brazil = np.abs(sorted_brazil_population - sorted_brazil_population_median)
mad_brazil_population = np.median(absolute_deviation_brazil)
print("Desvio absoluto mediano da mediana de sorted_brazil_population: ", mad_brazil_population)
# Estimativas baseadas em percentis
# Uma abordagem para calcular a dispersão é com base na distribuição de dados classificados e a medida mais básica é a amplitude que é a diferença entre o maior e o menor valor. Porém essa media é sensível a outliers

# Uma forma robusta é a amplitude interquartil (ou IQR), fazer a diferença entre o terceiro quartil (Q3) e o primeiro quartil (Q1)
# Exemplo: Dado os valores ordenados [1,2,3,3,5,6,7,9] 
# Calculamos o Q2 que é a mediana desse valor 3 + 5 / 2= 4
# Calculo Q1 a mediana da metade inferior: 2 + 3 / 2 = 2,5
# Calculo A3 a mediana da metade superior: 6 + 7 / 2 = 6,5
# Agora fazemos a diferença de Q3 - Q1: 6,5 - 2,5 = 4
# A amplitude interquartil do nosso dado é: 4


# Diferença interquartil de state_data['Population']
print("Diferenca interquartil de state_data['Population']: ", (state_data['Population'].quantile(0.75) - state_data['Population'].quantile(0.25)) / 1_000_000)

# Diferença interquartil de sorted_brazil_population
q3, q1 = np.percentile(sorted_brazil_population, [75, 25])
print("Diferenca interquartil de sorted_brazil_population: ", q3 - q1)