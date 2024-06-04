#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 14:25:59 2023

@author: adelino

Run over python 3.11 enviroment (p11_env)
"""
import pandas as pd
import sys
import numpy as np
from utils import extractValueColumn, anovaResult, genDecPercEstUnique
import os
import matplotlib.pyplot as plt
import datetime
from pirateplot import pirateplot
from scipy.stats import t

plt.rcParams['image.cmap'] = 'gist_heat'

cm = 1/2.54
DEBUG = False
RAW_DATA_CSV_FILE = 'PUB_Ticket_Log_PCMG_NOREP_BASE_19_22.csv'
SEL_DATA_CSV_FILE = 'PUB_Ticket_Log_PCMG_PLACA_UNICA_19_22.csv'
SEL_DATA_TXT_FILE = 'PUB_Ticket_Log_PCMG_PLACA_UNICA_19_22.txt'

SEL_DATA_CSV_FILE_PECA = 'PUB_Ticket_Log_PCMG_PECA_UNICA_19_22.csv'
SEL_DATA_TXT_FILE_PECA = 'SEL_Ticket_Log_PCMG_PECA_UNICA_19_22.txt'

PPF = os.path.basename(__file__).split("_")[0] + '_'


dfRawData = pd.read_csv(RAW_DATA_CSV_FILE,sep="\t")
tagManutençoes = [" uma "," duas ou três"," acima de três"]


'''
dfRawData.columns

['Placa', 'Família Segmento', 'Veículo Modelo',
       'Tipo Manutenção Oficina', 'Informacao Adicional2', 'Grupo Peça',
       'Cidade', 'Data Entrada Veículo', 'Data Retirada Veículo',
       'Dias na Oficina', 'Valor Total', 'MARCA', 'MODELO', 'PORTE',
       'Ano Fab/Mod', 'COMBUSTÍVEL', 'Ano Manut', 'Idade na Manut',
       'Classificação idade na Manut']

selected
        ['Placa','Tipo Manutenção Oficina','Data Entrada Veículo', 
         'Data Retirada Veículo', 'Dias na Oficina','Valor Total',
         'MARCA','PORTE','Ano Fab/Mod','COMBUSTÍVEL',
         'Idade na Manut','Classificação idade na Manut']
'''

dfSelData= dfRawData[['Placa','Data Entrada Veículo','Tipo Manutenção Oficina',#'Data Retirada Veículo',
                      'Dias na Oficina','Valor Total', 'Grupo Peça',
                      'MARCA', 'PORTE','Ano Fab/Mod', 'COMBUSTÍVEL',
                      'Idade na Manut','Classificação idade na Manut']]
if (DEBUG):
    sys.exit("DEPURA tabela")







# --- Unificaçao por placa ----------------------------------------------------
dfOriSelData = dfSelData;

# dfSelData = dfOriSelData[dfOriSelData["PORTE"] == 'UTILITÁRIO']

uniquePlates = np.unique(dfSelData['Placa'])
rows_list = []
numRep = np.zeros((9,))
lstValoresMedios = [np.array([]) for i in range(0,9)]
deltaDays = []
deltaHodometro = []
for i, plate in enumerate(uniquePlates):
    sub_df = dfSelData[dfSelData["Placa"] == plate]
    plateDates = sub_df['Data Entrada Veículo'].unique()
    # if (sub_df.shape[0] > 1):
    #     print("")
    base = sub_df.iloc[-1,:].copy()
    valoresManut = extractValueColumn(sub_df)
    base['Valor Total'] = np.sum(valoresManut)
    
    numPlates = len(plateDates)
    if (numPlates == 1):
        numRep[0] = numRep[0] + 1
        lstValoresMedios[0] = np.hstack((lstValoresMedios[0],valoresManut))
    if (numPlates == 2):
        numRep[1] = numRep[1] + 1
        lstValoresMedios[1] = np.hstack((lstValoresMedios[1],valoresManut))
    if (numPlates == 3):
        numRep[2] = numRep[2] + 1
        lstValoresMedios[2] = np.hstack((lstValoresMedios[2],valoresManut))
    if (numPlates == 4):
        numRep[3] = numRep[3] + 1
        lstValoresMedios[3] = np.hstack((lstValoresMedios[3],valoresManut))
    if (numPlates == 5):
        numRep[4] = numRep[4] + 1
        lstValoresMedios[4] = np.hstack((lstValoresMedios[4],valoresManut))
    if (numPlates == 6):
        numRep[5] = numRep[5] + 1
        lstValoresMedios[5] = np.hstack((lstValoresMedios[5],valoresManut))
    if (numPlates == 7):
        numRep[6] = numRep[6] + 1
        lstValoresMedios[6] = np.hstack((lstValoresMedios[6],valoresManut))
    if (numPlates == 8):
        numRep[7] = numRep[7] + 1
        lstValoresMedios[7] = np.hstack((lstValoresMedios[7],valoresManut))
    if (numPlates > 8):
        numRep[8] = numRep[8] + 1
        lstValoresMedios[8] = np.hstack((lstValoresMedios[8],valoresManut))
   
    
    if (numPlates == 1):
        numManutencoes = 0
        medTempo = 0
    elif ((numPlates > 1) and (numPlates < 4)):
        numManutencoes = 1
        medTempo = 0
        nPlates = numPlates
        for i in range(0,nPlates-1):
            A = datetime.datetime.strptime(plateDates[i], "%d/%m/%Y").date()
            B = datetime.datetime.strptime(plateDates[i+1], "%d/%m/%Y").date()
            medTempo += np.abs((B-A).days)
        medTempo = medTempo/nPlates
    else:
        numManutencoes = 2
        medTempo = 0
        for i in range(0,numPlates-1):
            A = datetime.datetime.strptime(plateDates[i], "%d/%m/%Y").date()
            B = datetime.datetime.strptime(plateDates[i+1], "%d/%m/%Y").date()
            medTempo += np.abs((B-A).days)
        medTempo = medTempo/numPlates
    base['Num Manutencoes'] = numPlates
    base['Manutencoes'] = numManutencoes
    base['Intervalo'] = medTempo
    dict1 = dict(base)
    rows_list.append(dict1)





numRepLabel = ['1','2','3','4','5','6','7','8','>8']
fig = plt.figure(figsize =(8, 4))
plt.bar(numRepLabel, numRep, edgecolor='0.25', color='0.25')
plt.title("Quantidade de placas com diferentes datas de chegada pata manutençao")
plt.ylabel('Quantidade de placas')
plt.xlabel('Numero de diferentes datas de chegada para manutenção')
plt.grid(color='gray', linestyle='-.', linewidth=0.5)
plt.savefig(PPF+'Numero_Ocorrencias.png',dpi=200,bbox_inches='tight')

percRep = 100*numRep/np.sum(numRep)
csumRep = np.cumsum(percRep)

fig = plt.figure(figsize =(8,4))
plt = pirateplot(lstValoresMedios,numRepLabel)
plt.title("Valores, medidas descritivas e inferenciais de manutenção",fontsize=16)
plt.ylabel('Valor de manutenção (R$)',fontsize=14)
plt.xlabel('Número de manutenções',fontsize=14)
plt.savefig(PPF+'Valor_Manutencoes_RDI_por_Quatidade_00.png',dpi=200,bbox_inches='tight')    

vecMean = [np.mean(i) for i in lstValoresMedios]
vecStd = [np.std(i) for i in lstValoresMedios]
vecErp = [t.ppf(0.975,len(i)-1)*np.std(i)/np.sqrt(len(i)) for i in lstValoresMedios]

fig = plt.figure(figsize =(8,4))
plt.bar(numRepLabel, vecMean, edgecolor='0.25', color='0.25', label='Valor médio')
plt.errorbar(numRepLabel, vecMean,yerr=vecStd, 
             linestyle=' ',marker='.', capsize=2, color='black', label='desvio padrão')
plt.legend()
plt.grid(color='gray', linestyle='-.', linewidth=0.5)
plt.title("Valores medios de manutençao e desvio padrao",fontsize=16)
plt.ylabel('Valor medo de manutenção (R$)',fontsize=14)
plt.xlabel('Número de manutenções',fontsize=14)
plt.savefig(PPF+'Valor_Manutencoes_MSTD_por_Quatidade_00.png',dpi=200,bbox_inches='tight')    


fig = plt.figure(figsize =(8,4))
plt.bar(numRepLabel, vecMean, edgecolor='0.25', color='0.25', label='Valor médio')
plt.errorbar(numRepLabel, vecMean,yerr=vecErp, 
             linestyle=' ',marker='.', capsize=2, color='black', label='Intervalo confiança da média')
plt.legend()
plt.grid(color='gray', linestyle='-.', linewidth=0.5)
plt.title("Valores de manutenção com intervalo confiança de 95%",fontsize=16)
plt.ylabel('Valor medio de manutenção (R$)',fontsize=14)
plt.xlabel('Número de manutenções',fontsize=14)
plt.savefig(PPF+'Valor_Manutencoes_MERP_por_Quatidade_00.png',dpi=200,bbox_inches='tight')    


fig, ax1 = plt.subplots(figsize =(8, 4))
ax1.bar(numRepLabel, percRep, edgecolor='0.25', color='0.25', label='Percentual de manutenções')
plt.title("Quantidade de placas com diferentes datas de chegada pata manutenção")
ax1.set_ylabel('Percentual de placas', color = '0.25')
ax1.set_xlabel('Quantidades de entradas para manutenção')
ax1.grid(color='gray', linestyle='-.', linewidth=0.5)
ax1.tick_params(axis ='y', labelcolor = '0.25') 
ax2 = ax1.twinx() 
ax2.plot(numRepLabel, csumRep, linestyle='-.', marker='o', linewidth=2, color = '0.65') 
ax2.set_ylabel('Percentual acumulado', color = '0.65') 
ax2.tick_params(axis ='y', labelcolor = '0.65') 
ax2.set_ylim([0,110])
plt.savefig(PPF+'Percentual_Ocorrencias.png',dpi=200,bbox_inches='tight')
  
fig, ax1 = plt.subplots(nrows=1, ncols=2,figsize =(16, 6))
ax1[1].bar(numRepLabel, percRep, edgecolor='0.25', color='0.25', label='Percentual de manutenções')
ax1[1].set_title("Quantidade de placas com diferentes datas de chegada pata manutenção")
ax1[1].set_ylabel('Percentual de placas', color = '0.25')
ax1[1].set_xlabel('Quantidades de entradas para manutenção')
ax1[1].grid(color='gray', linestyle='-.', linewidth=0.5)
ax1[1].tick_params(axis ='y', labelcolor = '0.25') 
ax2 = ax1[1].twinx() 
ax2.plot(numRepLabel, csumRep, linestyle='-.', marker='o', linewidth=2, color = '0.65') 
ax2.set_ylabel('Percentual acumulado', color = '0.65') 
ax2.tick_params(axis ='y', labelcolor = '0.65') 
ax2.set_ylim([0,110])

ax1[0] = pirateplot(lstValoresMedios,numRepLabel, ax1[0])
ax1[0].set_title("Valores, medidas descritivas e inferenciais de manutenção")
ax1[0].set_ylabel('Valor de manutenção (R$)')
ax1[0].set_xlabel('Número de manutenções')

plt.savefig(PPF+'Percentual_Ocorrencias_Valor_manutencao.png',dpi=200,bbox_inches='tight')

genDecPercEstUnique('Número de Manutenções',lstValoresMedios,numRepLabel,PPF+'Tabela_custo_por_manutencao.csv')



# H0:  as médias populacionais são iguais.

tagsComp, limitsComp, nVSn, _ = anovaResult(lstValoresMedios,numRepLabel,
                                            PPF+'Anova_num_Manutencoes.txt')
        

dfSelData = pd.DataFrame(rows_list)
dfSelData= dfSelData[['Placa',
                      'Dias na Oficina','Valor Total', 'Grupo Peça',
                      'Tipo Manutenção Oficina',
                      'MARCA', 'PORTE','Ano Fab/Mod', 'COMBUSTÍVEL',
                      'Idade na Manut','Classificação idade na Manut',
                      'Num Manutencoes','Manutencoes','Intervalo']]
selComulmn = dfSelData.columns
selFactors = ['MARCA', 'PORTE','Ano Fab/Mod', 'COMBUSTÍVEL','Grupo Peça',
              'Idade na Manut','Classificação idade na Manut','Tipo Manutenção Oficina']
uniquePorte = dfSelData["PORTE"].unique()

uniqueNumManut = dfSelData["Manutencoes"].unique()

totalrows = dfSelData.shape[0]
    
with open(SEL_DATA_TXT_FILE, "w") as f:
    print("Shape", file=f)
    print("{:}".format(dfSelData.shape), file=f)
    print("---------------------------", file=f)
    print("Fatores:", file=f)
    for col in selComulmn:
        if (col not in selFactors):
            continue
        print("{:}".format(col), file=f)
        print("{:}".format(np.sort(dfSelData[col].unique())), file=f)
    print("---------------------------", file=f)
    print("Combustivel:", file=f)
    print("N° gasolina, n° diesel", file=f)
    print("{:},{:}".format(len(dfSelData[dfSelData["COMBUSTÍVEL"] == "GASOLINA"]),
                           len(dfSelData[dfSelData["COMBUSTÍVEL"] == "DIESEL"])), file=f)
    print("---------------------------", file=f)
    print("Porte:", file=f)
    print("N° gasolina, n° diesel", file=f)
    for porte in uniquePorte:
        dfTemp = dfSelData[dfSelData["PORTE"] == porte]
        print("{:}".format(porte), file=f)
        print("{:},{:}".format(len(dfTemp[dfTemp["COMBUSTÍVEL"] == "GASOLINA"]),
                               len(dfTemp[dfTemp["COMBUSTÍVEL"] == "DIESEL"])), file=f)
    
    for porte in uniqueNumManut:
        dfTemp = dfSelData[dfSelData["Manutencoes"] == porte]
        numrows = dfTemp.shape[0]
        print("Manutençẽos: {:} (valor: {:}) PERC. {:3.2f} %".format(tagManutençoes[porte], porte,100*numrows/totalrows ), file=f)
        print("Gasolina, Diesel, Total", file=f)
        nGas = len(dfTemp[dfTemp["COMBUSTÍVEL"] == "GASOLINA"])
        nDie = len(dfTemp[dfTemp["COMBUSTÍVEL"] == "DIESEL"])
        print("{:},{:},{:}".format(nGas,nDie,nGas+nDie), file=f)
        
   
dfSelData.to_csv(SEL_DATA_CSV_FILE, sep='\t', encoding='utf-8', index=False)
