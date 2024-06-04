#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 14:51:58 2024

@author: adelino
"""

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import sys
import os
from utils import extractValueColumn
import dill                   
from qqplot import plot_qqplot
import statsmodels.formula.api as smf

from scipy import stats



boxprops = dict(linestyle='-', linewidth=2.5, color='black')
medianprops = dict(linestyle='-', linewidth=2.5, color='gray')

plt.rcParams['image.cmap'] = 'gist_gray'

# =============================================================================
PPF = os.path.basename(__file__).split("_")[0] + '_'
DATA_PLACA_CSV_FILE = 'PUB_Ticket_Log_PCMG_PLACA_UNICA_19_22.csv'
DATA_PECA_CSV_FILE = 'PUB_Ticket_Log_PCMG_NOREP_BASE_19_22.csv'


df_Placa = pd.read_csv(DATA_PLACA_CSV_FILE,sep="\t")
df_Peca  = pd.read_csv(DATA_PECA_CSV_FILE,sep="\t")

# df_Placa = df_Placa[df_Placa["PORTE"] == 'UTILITÁRIO']
# df_Peca = df_Peca[df_Peca["PORTE"] == 'UTILITÁRIO']

lstTypeComb = df_Placa["COMBUSTÍVEL"].unique()
lstTypePeca = df_Peca["Grupo Peça"].unique()
lstTypeManu = df_Placa["Manutencoes"].unique()
tagManutençoes = [" 1 "," 2 - 3"," < 3"]
tagManutençoes = [" uma "," duas ou três"," acima de três"]
lstTypePecaSel = ['MOTOR', 'ELETRICA', 'FREIO', 'SUSPENSAO', 'TRANSMISSAO']

lstTagMarcas = df_Peca['MARCA'].unique()
lstTagSelMarcas = []
lstValoresMarca = []
lstValoresOutrasMarcas = []
lstOutrasMarcas = []
numOutras = 0
for k, marca in enumerate(lstTagMarcas):
    dfTemp = df_Peca[df_Peca['MARCA'] == marca]
    if (dfTemp.shape[0] > 30):
        lstTagSelMarcas.append(marca)
        lstValoresMarca.append(extractValueColumn(dfTemp))
    else:
        arrayTemp = extractValueColumn(dfTemp)
        lstValoresOutrasMarcas = list(np.hstack((lstValoresOutrasMarcas,extractValueColumn(dfTemp))))
        lstOutrasMarcas.append(marca)
        numOutras +=dfTemp.shape[0]
        
lstTagSelMarcas.append('OUTRAS')
lstValoresMarca.append(lstValoresOutrasMarcas)


dictJoin = {}
lstManuJoin = []
lstIntvJoin = []
lstNumManuJoin = []
lstPrecoJoin = []
lstGrupoPecaJoin = []
lstMontadoraJoin = []
for i in range(0,df_Peca.shape[0]):
    plate = df_Peca["Placa"].iloc[i]
    dfTemp = df_Placa[df_Placa["Placa"] == plate]
    lstNumManuJoin.append(dfTemp['Num Manutencoes'].values[0])
    lstManuJoin.append(dfTemp['Manutencoes'].values[0])
    lstIntvJoin.append(dfTemp['Intervalo'].values[0])
    lstPrecoJoin.append(extractValueColumn(dfTemp)[0])
    if (dfTemp['Grupo Peça'].values[0] in lstTypePecaSel):
        lstGrupoPecaJoin.append(dfTemp['Grupo Peça'].values[0])
    else:
        lstGrupoPecaJoin.append('Outra')
    if (dfTemp['MARCA'].values[0] in lstTagSelMarcas):
        lstMontadoraJoin.append(dfTemp['MARCA'].values[0])
    else:
        lstMontadoraJoin.append('Outra')
        
        
dictJoin['Num_Manutencoes'] = lstNumManuJoin
dictJoin['Manutencoes'] = lstManuJoin
dictJoin['Intervalo'] = lstIntvJoin
dictJoin['Preco'] = lstPrecoJoin
dictJoin['Peca'] = lstGrupoPecaJoin
dictJoin['Montadora'] = lstMontadoraJoin
other = pd.DataFrame(dictJoin)
df_Peca = df_Peca.join(other)
    
df_Peca = df_Peca.rename({'Idade na Manut': 'Idade', 'Dias na Oficina': 'Dias_Oficina'}, axis=1)
'''
df_Peca.columns
Index(['Placa', 'Família Segmento', 'Data Entrada Veículo', 'Veículo Modelo',
       'Tipo Manutenção Oficina', 'Grupo Peça', 'Ano Fab/Mod',
       'Dias na Oficina', 'Valor Total', 'MARCA', 'MODELO', 'PORTE',
       'COMBUSTÍVEL', 'Idade na Manut', 'Classificação idade na Manut',
       'Num _anutencoes', 'Manutencoes', 'Intervalo', 'Preco', 'Peca',
       'Montadora'],
      '''
colPeca = df_Placa.columns

FILE_GENERAL_MODEL = PPF + 'LM_General_model_for_Quanty.pty'
GENERAL_MODEL = True
if (GENERAL_MODEL):
    if (os.path.exists(FILE_GENERAL_MODEL) and False):
        print("Nao carrega modelo...")
    else:
        print("Inicio da modelagem por modelo geral...")
        # gmd = smf.glm("Quantidade ~ Exame",data=newDF2) #family=sm.families.Gamma()
        # npResid = np.array(newDF2["Quantidade"] - gmdf.predict())
        # strFormula = "Preco ~ Idade + Num_Manutencoes + " + \
        strFormula = "Preco ~ Idade + Num_Manutencoes + " + \
                     " C(COMBUSTÍVEL) + C(Peca) + C(Montadora) + 0"
        gmd = smf.glm(strFormula,data=df_Peca) #family=sm.families.Gamma()
        gmdf = gmd.fit()
        dictGenModel = {"Modelo": gmdf,
                                 "Residuo": []} 
        with open(FILE_GENERAL_MODEL, "wb") as dill_file:
            dill.dump(dictGenModel, dill_file)   

    yParam = np.array(gmdf.params.index)
    xValues = np.array(gmdf.params)
    pValues = np.array(gmdf.pvalues)
    
    idxOrd = np.argsort(xValues)
    pValues = pValues[idxOrd]
    yParam = yParam[idxOrd]
    xValues = xValues[idxOrd]
    xQuant = np.zeros((len(idxOrd),))
    nInt = 0
    labely = [sParam.split('T.')[-1].replace("]",'') for sParam in yParam]
    labely =  yParam
    for i, label in enumerate(labely):
        parts = label.split(")[")
        if (len(parts) > 1):
            part0 = parts[0].replace("C(","")
            part1 = parts[1].replace("T.","").replace("]","")
            labely[i] = "{:}: {:}".format(part0,part1)
        else:
            labely[i] = label.replace("_"," ")
    ref = range(0,len(yParam))
    
    maxbar = np.max(xValues)
    order = 10**int(np.log10(abs(maxbar)))
    k_max = order*np.ceil(maxbar/(order))
    minbar = np.min(xValues)
    order = 10**int(np.log10(abs(minbar)))
    k_min = order*np.ceil(minbar/(order))
    
    
    # fig, ax = plt.subplots(1, 3, figsize =(16, 12),gridspec_kw={'width_ratios': [3, 1.5, 0.75]})
    fig, ax = plt.subplots(1, 2, figsize =(16, 6),gridspec_kw={'width_ratios': [3, 2]})
    ax[0].set_title("Valores dos coeficiente do modelo e respectivo valor-p")
    ax[0].barh(ref,xValues, color='0.75',alpha=0.5)
    ax[0].set_xlabel("Valor do coeficiente")
    ax[0].set_yticks(ref,labely)
    ax[0].grid(color='gray', linestyle='-.', linewidth=0.5)
    ax[0].set_ylim([-0.5,len(yParam)])
    
     
    ax[1].barh(ref,pValues, color='0.35',alpha=0.5)
    ax[1].plot([0.05,0.05],[-0.5,len(yParam)], "k-.", linewidth=2)
    ax[1].set_xlabel("Valor-p")
    ax[1].grid(color='gray', linestyle='-.', linewidth=0.5)
    ax[1].set_yticks(ref,[])
    ax[1].set_ylim([-0.5,len(yParam)])
    
    plt.subplots_adjust(wspace=0, hspace=0)
    
    fig.savefig(PPF+ 'Resultado_Modelo.png',dpi=200,bbox_inches='tight')


    

    fig, ax1 = plt.subplots(nrows=1, ncols=2,figsize =(16, 6))
    ax1[0].hist(gmdf.resid_response, 50, density=False, histtype='stepfilled', color='0.35',alpha=0.5, label = "Quantidade")
    ax1[0].set_title('Histograma da distribuição resíduos')
    ax1[0].set_ylabel('Número de de ocorrências')
    ax1[0].set_xlabel("Valores de resíduos")
    ax1[0].grid(color='gray', linestyle='-.', linewidth=0.5)
    
    ax1[1] =  plot_qqplot(gmdf.resid_response, ax1[1])
    ax1[1].set_title('Quantil-quantil com intervalo de confiança de 95%')
    ax1[1].set_xlabel('Quantis Teóricos')
    ax1[1].set_ylabel('Quantis Amostrais')
    ax1[1].legend()
    ax1[1].grid(color='gray', linestyle='-.', linewidth=0.5)
    
    fig.savefig(PPF+ 'Analise_residuos.png',dpi=200,bbox_inches='tight')
    
    res = stats.shapiro(gmdf.resid_response)


