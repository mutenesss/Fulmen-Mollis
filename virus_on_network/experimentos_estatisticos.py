# Experimentos estatísticos
import numpy as np


# planejamento do experimento
# hipótese 1 - 

controles_e_seus_niveis = {
    "num_nodes": 50,
    "avg_node_degree": 3,
    "initial_outbreak_size": 5,
    "virus_spread_chance": 0.4,
    "virus_check_frequency": 0.4,
    "recovery_chance": 0.3,
    "gain_resistance_chance": 0.3
    # "mortality_chance": 0.2
}

# usando o framework mesa e as facilidades da computação experimental, 
# combinado com as orientações em https://www.voxco.com/blog/factorial-experimental-design/
# vamos realizar o "desenho fatorial de experimentos", onde estudaremos os efeitos de múltiplos fatores.
# vamos usar a técnica de "desenho totalmente cruzado", onde cada um dos fatores possui múltiplos níveis de tratamento
# "Using this design, all the possible combinations of factor levels can be investigated in each replication"

variaveis_independentes_e_seus_niveis = {
    # "num_nodes": 50,
    # "avg_node_degree": 3,
    # "initial_outbreak_size": 5,
    # "virus_spread_chance": 0.4,
    # "virus_check_frequency": 0.4,
    # "recovery_chance": 0.3,
    # "gain_resistance_chance": 0.3,
    "mortality_chance": np.arange(0.1, 1.1, 0.1),
    
}
lista_de_fatores = variaveis_independentes_e_seus_niveis.keys()
lista_de_niveis_por_fator = variaveis_independentes_e_seus_niveis.values()
qtd_de_tratamentos_por_fator = [f.size for f in lista_de_niveis_por_fator]
qtd_total_tratamentos = np.prod([f.size for f in variaveis_independentes_e_seus_niveis.values()])

print("Lista de Fatores: " + str(lista_de_fatores))
print("Lista de tratamentos ou níveis por fator: " + str(lista_de_niveis_por_fator))
print("Quantidade de tratamentos ou níveis por fator: " + str(qtd_de_tratamentos_por_fator))
print("Quantidade total de tratamentos a serem aplicados: " + str(qtd_total_tratamentos))

# soma os dois dicionários 
experimental_design_of_independent_plus_control_variables = controles_e_seus_niveis.copy()
experimental_design_of_independent_plus_control_variables.update(variaveis_independentes_e_seus_niveis)

replicacoes = 500 # no desenho experimental, esse parâmetro é chamado de replicação, 
                # e indica a quantidade de replicações de cada tratamento 
print("Quantidade de replicações para cada tratamento:"+str(replicacoes))

print("Quantidade total de simulações independentes a serem realizadas:"+str(replicacoes*qtd_total_tratamentos))

print("Uma vez que cada simulação é um sujeito novo, completamente definido por variáveis aleatórias,\
        estaremos fazendo um 'Between Subject Factorial Design'")


import mesa
from model import VirusOnNetwork
qtd_maxima_passos_para_estabilizar = 100 # qtd de interações necessárias para o fenômeno é estabilizar

from datetime import datetime
inicio_experimento = datetime.now()

qtd_processadores = 8
print("No âmbito da algoritmica experimental, estamos interessados em saber se a computação multithead reduz o tempo... ")
print("Qtd de processadores: "+str(qtd_processadores))


results = mesa.batch_run(
    VirusOnNetwork,
    parameters=experimental_design_of_independent_plus_control_variables,
    iterations=replicacoes,
    max_steps=qtd_maxima_passos_para_estabilizar,
    number_processes=qtd_processadores, # usar todos os processadores disponíveis em um arranjo multithread
    data_collection_period=-1,
    display_progress=True,
)

# gera uma string com data e hora
fim_experimento = datetime.now()
duracao_experimento = fim_experimento - inicio_experimento
fim_experimento_str = str(fim_experimento)


file_name_suffix = (
    "_fatores[" + str(lista_de_fatores).replace("[","").replace("]","").replace("(","").replace(")","").replace("-","").replace("dict_keys","")+"]"
    "_tratam[" + str(qtd_total_tratamentos) +"]" +
    "_replic[" + str (replicacoes) +"]"+
    "_passos[" + str (qtd_maxima_passos_para_estabilizar)+"]"+
    "_process[" + str (qtd_processadores)+ "]"+
    "_segs[" + str(duracao_experimento.seconds) + "]"+
    "_final[" + fim_experimento_str +"]"
). replace ( ":" , "-" ). replace ( " " , "-" )
# define um prefixo para o nome para o arquivo de dados
model_name_preffix = "Exp.Tot.Cruzados_BetweenSubject_VirusOnNetwork"
# define o nome do arquivo
file_name = model_name_preffix + file_name_suffix + ".csv"
print(file_name)

import pandas as pd
results_df = pd.DataFrame(results)
results_df.to_csv(file_name)
