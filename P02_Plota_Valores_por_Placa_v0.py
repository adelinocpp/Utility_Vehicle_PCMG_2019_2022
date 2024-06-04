#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 16:24:23 2023

@author: adelino
"""
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import sys
import os
from matplotlib.patches import Polygon
from utils import removeOutLiers, extractValueColumn, extractPairedValueColumn, \
                    genDiffMeanTest, genCoorTest, genDecPercEst
                    
                    
boxprops = dict(linestyle='-', linewidth=2.5, color='black')
medianprops = dict(linestyle='-', linewidth=2.5, color='red')
# =============================================================================
PPF = os.path.basename(__file__).split("_")[0] + '_'
SEL_DATA_CSV_FILE = 'SEL_Ticket_Log_PCMG_19_22.csv'

dfSelData = pd.read_csv(SEL_DATA_CSV_FILE,sep="\t")
selColumns = dfSelData.columns
boolRunAll = True
# -----------------------------------------------------------------------------
dfGASOLINA = dfSelData[dfSelData["COMBUSTÍVEL"] == 'GASOLINA']
dfDIESEL = dfSelData[dfSelData["COMBUSTÍVEL"] == 'DIESEL']

vecValGas = extractValueColumn(dfGASOLINA)
vecValDie = extractValueColumn(dfDIESEL)
Ng = len(vecValGas)
Nd = len(vecValDie)

GEN_ESTATS_TABLE = boolRunAll
if (GEN_ESTATS_TABLE):
    descFile = PPF+'TB_01_EstDesc_Gas_Diel_01_Bruta.csv'
    genDecPercEst('Combustivel',vecValGas,'GASOLINA',vecValDie,'DIESEL',descFile)
    # percFile = PPF+'TB_02_EstPerc_Gas_Diel_01_Bruta.csv'
    # genPercEst('Combustivel',vecValGas,'GASOLINA',vecValDie,'DIESEL',percFile)

# GEN_ESTATS_TABLE_LOG = boolRunAll
# if (GEN_ESTATS_TABLE_LOG):
#     descFile = PPF+'TB_01_EstDesc_Gas_Diel_01_LOG.csv'
#     genDecPercEst('Combustivel',np.log10(vecValGas),'GASOLINA',np.log10(vecValDie),'DIESEL',descFile)
#     # percFile = PPF+'TB_02_EstPerc_Gas_Diel_01_LOG.csv'
#     # genPercEst('Combustivel',np.log10(vecValGas),'GASOLINA',np.log10(vecValDie),'DIESEL',percFile)

FIG_BOXPLOT_ALL = boolRunAll

if (FIG_BOXPLOT_ALL):
    fig = plt.figure(figsize =(6, 8))
    plt.title("Valores de manutenção em R$")
    plt.ylabel('Valor de manutenção')
    plt.boxplot([vecValGas,vecValDie],boxprops=boxprops,medianprops=medianprops)
    plt.xticks([1,2],["GASOLINA", "DIESEL"])
    plt.grid(color='gray', linestyle='-.', linewidth=0.5)
    plt.savefig(PPF+'PLT_01_BoxPlot_Bruta_All.png',dpi=200,bbox_inches='tight')

RAW_DIFF_TEST = boolRunAll
if (RAW_DIFF_TEST):
    fileName = PPF+"ET_01_Bruta.txt"
    extraComment = "Teste de diferença entre as medias"
    genDiffMeanTest(vecValGas, vecValDie,fileName,extraComment)
    
# --- recorte Utilitarios
UTILITY_CUT_VEHICLES = boolRunAll
if (UTILITY_CUT_VEHICLES):
    dfGasUtilitario = dfGASOLINA[dfGASOLINA["PORTE"] == 'UTILITÁRIO']
    dfDieUtilitario = dfDIESEL[dfDIESEL["PORTE"] == 'UTILITÁRIO']

    vecValGas = extractValueColumn(dfGasUtilitario)
    Ng = len(vecValGas)
    vecValDie = extractValueColumn(dfDieUtilitario)
    Nd = len(vecValDie)

    descFile = PPF+'TB_03_EstDesc_Gas_Diel_01_PORTE.csv'
    genDecPercEst('Combustivel',vecValGas,'GASOLINA',vecValDie,'DIESEL',descFile)
    

    fig = plt.figure(figsize =(6, 8))
    plt.title("Valores de manutenção dos Utilitarios em R$")
    plt.ylabel('Valor de manutenção')
    plt.boxplot([vecValGas,vecValDie],boxprops=boxprops,medianprops=medianprops)
    plt.xticks([1,2],["GASOLINA", "DIESEL"])
    plt.grid(color='gray', linestyle='-.', linewidth=0.5)
    plt.savefig(PPF+'PLT_03_BoxPlot_PORTE_All.png',dpi=200,bbox_inches='tight')

    fileName = PPF+"ET_02_Pareado_Utilitarios.txt"
    extraComment = "\tpareado por veiculos utilitarios."
    genDiffMeanTest(vecValGas, vecValDie,fileName,extraComment)
    


dfGASOLINA = dfGASOLINA[dfGASOLINA["PORTE"] == 'UTILITÁRIO']
dfDIESEL = dfDIESEL[dfDIESEL["PORTE"] == 'UTILITÁRIO']
dfFULLGAS = dfSelData[dfSelData["COMBUSTÍVEL"] == 'GASOLINA']
dfFULLDIE = dfSelData[dfSelData["COMBUSTÍVEL"] == 'DIESEL']
 
MANUFACTURE = boolRunAll
if (MANUFACTURE):
    setJoin = list(set(np.unique(dfDIESEL['MARCA'])).intersection(np.unique(dfGASOLINA['MARCA'])))
    dfGasFabricante = dfGASOLINA[dfGASOLINA["MARCA"].isin(setJoin)]
    dfDieFabricante = dfDIESEL[dfDIESEL["MARCA"].isin(setJoin)]

    data = []
    dataG = []
    dataD = []
    pG = []
    pD = []
    xT = []
    k = 1;
    for MARCA in setJoin:
        valG = extractValueColumn(dfGasFabricante[dfGasFabricante["MARCA"] == MARCA])
        valD = extractValueColumn(dfDieFabricante[dfDieFabricante["MARCA"] == MARCA])
        data.append(valG)
        data.append(valD)
        dataG.append(valG)
        dataD.append(valD)
        pG.append(k)
        k = k+0.5
        xT.append(k)
        k = k+0.5
        pD.append(k)
        k = k+1
        
        percFile = PPF+'TB_05_EstDescPerc_Gas_Diel_01_PORTE_MARCA_{:}.csv'.format(MARCA)
        genDecPercEst('Combustivel-{:}'.format(MARCA),valG,'GASOLINA',valD,'DIESEL',percFile)

    fig, ax1 = plt.subplots(figsize=(10, 6))
    bp1 = ax1.boxplot(dataG,positions=pG,patch_artist=True,boxprops=dict(facecolor="darkkhaki"))
    bp2 = ax1.boxplot(dataD,positions=pD,patch_artist=True,boxprops=dict(facecolor="royalblue"))
    ax1.set(
        axisbelow=True,  # Hide the grid behind plot objects
        title="Valores de manutenção Utilitarios em R$",
        xlabel='MARCAS',
        ylabel='Valor de manutenção',
        )
    
    ax1.legend([bp1["boxes"][0], bp2["boxes"][0]], ['GASOLINA', 'DIESEL'], loc='upper left')
    ax1.set_xticks(xT)
    ax1.set_xticklabels(setJoin)
    ax1.grid(color='gray', linestyle='-.', linewidth=0.5)
    plt.savefig(PPF+'PLT_05_BoxPlot_Fabricante_All.png',dpi=200,bbox_inches='tight')
    
PARTS = boolRunAll
if (PARTS):
    '''
    ['ACESSORIOS' 'AR CONDICIONADO' 'ASSISTENCIA 24H' 'ELETRICA'
     'EQUIPAMENTOS' 'FREIO' 'FUNILARIA' 'MOTOR' 'MÃO DE OBRA' 'PRODUTOS'
     'SUSPENSAO' 'TRANSMISSAO']'''
    setJoin = ['ELETRICA', 'FREIO', 'MOTOR', 'SUSPENSAO']
    # setJoin = list(set(np.unique(dfDIESEL['Classificação idade na Manut'])).intersection(np.unique(dfGASOLINA['Classificação idade na Manut'])))
    dfGasFabricante = dfGASOLINA[dfGASOLINA["Grupo Peça"].isin(setJoin)]
    dfDieFabricante = dfDIESEL[dfDIESEL["Grupo Peça"].isin(setJoin)]
    
    data = []
    dataG = []
    dataD = []
    for MARCA in setJoin:
        valG = extractValueColumn(dfGasFabricante[dfGasFabricante["Grupo Peça"] == MARCA])
        valD = extractValueColumn(dfDieFabricante[dfDieFabricante["Grupo Peça"] == MARCA])
        data.append(valG)
        data.append(valD)
        dataG.append(valG)
        dataD.append(valD)
        percFile = PPF+'TB_06_EstDescPerc_Gas_Diel_01_Peca_{:}.csv'.format(MARCA)
        genDecPercEst('Combustivel-{:}'.format(MARCA),valG,'GASOLINA',valD,'DIESEL',percFile)

    fig, ax1 = plt.subplots(figsize=(10, 6))
    bp1 = ax1.boxplot(dataG,positions=[1,3,5,7],patch_artist=True,boxprops=dict(facecolor="darkkhaki"))
    bp2 = ax1.boxplot(dataD,positions=[2,4,6,8],patch_artist=True,boxprops=dict(facecolor="royalblue"))
    ax1.set(
        axisbelow=True,  # Hide the grid behind plot objects
        title="Valores de manutenção Utilitarios em R$",
        xlabel='Grupo de Peça de Manutençao',
        ylabel='Valor de manutenção',
        )
    
    ax1.legend([bp1["boxes"][0], bp2["boxes"][0]], ['GASOLINA', 'DIESEL'], loc='upper right')
    ax1.set_xticks([1.5,3.5,5.5,7.5])
    ax1.set_xticklabels(setJoin)
    ax1.grid(color='gray', linestyle='-.', linewidth=0.5)
    plt.savefig(PPF+'PLT_08_BoxPlot_Pecas_Utilitarios.png',dpi=200,bbox_inches='tight')
    
PARTS_ALL = boolRunAll
if (PARTS_ALL):
    '''
    ['ACESSORIOS' 'AR CONDICIONADO' 'ASSISTENCIA 24H' 'ELETRICA'
     'EQUIPAMENTOS' 'FREIO' 'FUNILARIA' 'MOTOR' 'MÃO DE OBRA' 'PRODUTOS'
     'SUSPENSAO' 'TRANSMISSAO']'''
    setJoin = ['ELETRICA', 'FREIO', 'MOTOR', 'SUSPENSAO']
    # setJoin = list(set(np.unique(dfDIESEL['Classificação idade na Manut'])).intersection(np.unique(dfGASOLINA['Classificação idade na Manut'])))
    dfGasFabricante = dfFULLGAS[dfFULLGAS["Grupo Peça"].isin(setJoin)]
    dfDieFabricante = dfFULLDIE[dfFULLDIE["Grupo Peça"].isin(setJoin)]
    
    data = []
    dataG = []
    dataD = []
    for MARCA in setJoin:
        valG = extractValueColumn(dfGasFabricante[dfGasFabricante["Grupo Peça"] == MARCA])
        valD = extractValueColumn(dfDieFabricante[dfDieFabricante["Grupo Peça"] == MARCA])
        data.append(valG)
        data.append(valD)
        dataG.append(valG)
        dataD.append(valD)
        percFile = PPF+'TB_06_EstDescPerc_Gas_Diel_01_Peca_TODOS_{:}.csv'.format(MARCA)
        genDecPercEst('Combustivel-{:}'.format(MARCA),valG,'GASOLINA',valD,'DIESEL',percFile)

    fig, ax1 = plt.subplots(figsize=(10, 6))
    bp1 = ax1.boxplot(dataG,positions=[1,3,5,7],patch_artist=True,boxprops=dict(facecolor="darkkhaki"))
    bp2 = ax1.boxplot(dataD,positions=[2,4,6,8],patch_artist=True,boxprops=dict(facecolor="royalblue"))
    ax1.set(
        axisbelow=True,  # Hide the grid behind plot objects
        title="Valores de manutenção em R$",
        xlabel='Grupo de Peça de Manutençao',
        ylabel='Valor de manutenção',
        )
    
    ax1.legend([bp1["boxes"][0], bp2["boxes"][0]], ['GASOLINA', 'DIESEL'], loc='upper right')
    ax1.set_xticks([1.5,3.5,5.5,7.5])
    ax1.set_xticklabels(setJoin)
    ax1.grid(color='gray', linestyle='-.', linewidth=0.5)
    plt.savefig(PPF+'PLT_08_BoxPlot_Pecas_TODOS.png',dpi=200,bbox_inches='tight')
    
    
AGE = boolRunAll
if (AGE):
    setJoin = ['NOVO', 'ATÉ 5 ANOS', 'ATÉ 10 ANOS', 'MAIOR 10 ANOS']
    # setJoin = list(set(np.unique(dfDIESEL['Classificação idade na Manut'])).intersection(np.unique(dfGASOLINA['Classificação idade na Manut'])))
    dfGasFabricante = dfGASOLINA[dfGASOLINA["Classificação idade na Manut"].isin(setJoin)]
    dfDieFabricante = dfDIESEL[dfDIESEL["Classificação idade na Manut"].isin(setJoin)]
    
    data = []
    dataG = []
    dataD = []
    for MARCA in setJoin:
        valG = extractValueColumn(dfGasFabricante[dfGasFabricante["Classificação idade na Manut"] == MARCA])
        valD = extractValueColumn(dfDieFabricante[dfDieFabricante["Classificação idade na Manut"] == MARCA])
        data.append(valG)
        data.append(valD)
        dataG.append(valG)
        dataD.append(valD)
        percFile = PPF+'TB_06_EstDescPerc_Gas_Diel_01_PORTE_Idade_{:}.csv'.format(MARCA)
        genDecPercEst('Combustivel-{:}'.format(MARCA),valG,'GASOLINA',valD,'DIESEL',percFile)

    fig, ax1 = plt.subplots(figsize=(10, 6))
    bp1 = ax1.boxplot(dataG,positions=[1,3,5,7],patch_artist=True,boxprops=dict(facecolor="darkkhaki"))
    bp2 = ax1.boxplot(dataD,positions=[2,4,6,8],patch_artist=True,boxprops=dict(facecolor="royalblue"))
    ax1.set(
        axisbelow=True,  # Hide the grid behind plot objects
        title="Valores de manutenção Utilitarios em R$",
        xlabel='Classificação idade na Manutençao',
        ylabel='Valor de manutenção',
        )
    
    ax1.legend([bp1["boxes"][0], bp2["boxes"][0]], ['GASOLINA', 'DIESEL'], loc='upper right')
    ax1.set_xticks([1.5,3.5,5.5,7.5])
    ax1.set_xticklabels(setJoin)
    ax1.grid(color='gray', linestyle='-.', linewidth=0.5)
    plt.savefig(PPF+'PLT_08_BoxPlot_Idade_All.png',dpi=200,bbox_inches='tight')
    
     
YEAR = True
if (YEAR):
    valueAllDIESEL, yearAllDIESEL = extractPairedValueColumn(dfDIESEL,'Ano Fab/Mod')
    valueAllGASOLINA, yearAllGASOLINA = extractPairedValueColumn(dfGASOLINA,'Ano Fab/Mod')
    
    fig = plt.figure(figsize =(6, 6))
    plt.scatter(yearAllGASOLINA, valueAllGASOLINA, marker='x', alpha=0.25, c='darkkhaki',label='GASOLINA')
    plt.scatter(yearAllDIESEL, valueAllDIESEL, marker='o', alpha=0.25, c='royalblue',label='DIESEL')
    plt.title("Valores de manutenção Utilitarios de acordo com o Ano de Fabricação")
    plt.ylabel('Valor de manutenção')
    plt.xlabel('Ano Fab/Mod')
    plt.legend()
    plt.grid(color='gray', linestyle='-.', linewidth=0.5)
    plt.savefig(PPF+'PLT_11_Scatter_Valor_Manutencao_Ano_Fab.png',dpi=200,bbox_inches='tight')
    
    fileName = PPF+"ET_03_Correlacao_Manutencao_Ano_GASOLINA.txt"
    extraComment = "\tCorrelacao Utilitarios GASOLINA Valor vs Ano."
    genCoorTest(yearAllGASOLINA, valueAllGASOLINA,fileName,extraComment)
    
    fileName = PPF+"ET_04_Correlacao_Manutencao_Ano_DIESEL.txt"
    extraComment = "\tCorrelacao Utilitario  DIESEL Valor vs Ano."
    genCoorTest(yearAllDIESEL, valueAllDIESEL,fileName,extraComment)
    

    # 'Idade na Manut'
    # 'Dias na Oficina''
    
NUMBER_OF_DAYS = True
if (NUMBER_OF_DAYS):
    valueAllDIESEL, yearAllDIESEL = extractPairedValueColumn(dfDIESEL,'Dias na Oficina')
    valueAllGASOLINA, yearAllGASOLINA = extractPairedValueColumn(dfGASOLINA,'Dias na Oficina')
    
    fig = plt.figure(figsize =(6, 6))
    plt.scatter(yearAllGASOLINA, valueAllGASOLINA, marker='x', alpha=0.5, c='darkkhaki',label='GASOLINA')
    plt.scatter(yearAllDIESEL, valueAllDIESEL, marker='o', alpha=0.5, c='royalblue',label='DIESEL')
    plt.title("Valores de manutenção Utilitarios pela duraçao em dias")
    plt.ylabel('Valor de manutenção')
    plt.xlabel('numero de dias')
    plt.legend()
    plt.grid(color='gray', linestyle='-.', linewidth=0.5)
    plt.savefig(PPF+'PLT_13_Scatter_Valor_Manutencao_Dias_manutencao.png',dpi=200,bbox_inches='tight')
    
  
    fileName = PPF+"ET_05_Correlacao_Manutencao_Dias_oficina_GASOLINA.txt"
    extraComment = "\tCorrelacao GASOLINA Valor vs Dias_oficina."
    genCoorTest(yearAllGASOLINA, valueAllGASOLINA,fileName,extraComment)
    
    
    fileName = PPF+"ET_06_Correlacao_Manutencao_Dias_oficina_DIESEL.txt"
    extraComment = "\tCorrelacao DIESEL Valor vs Dias_oficina."
    genCoorTest(yearAllDIESEL, valueAllDIESEL,fileName,extraComment)
 

IDADE = True
if (IDADE):
    valueAllDIESEL, yearAllDIESEL = extractPairedValueColumn(dfDIESEL,'Idade na Manut')
    valueAllGASOLINA, yearAllGASOLINA = extractPairedValueColumn(dfGASOLINA,'Idade na Manut')
    
    fig = plt.figure(figsize =(6, 6))
    plt.scatter(yearAllGASOLINA, valueAllGASOLINA, marker='x', alpha=0.25, c='darkkhaki',label='GASOLINA')
    plt.scatter(yearAllDIESEL, valueAllDIESEL, marker='o', alpha=0.25, c='royalblue',label='DIESEL')
    plt.title("Valores de manutenção pela idade do veiculo")
    plt.ylabel('Valor de manutenção')
    plt.xlabel('Idade veiculo (anos)')
    plt.legend()
    plt.grid(color='gray', linestyle='-.', linewidth=0.5)
    plt.savefig(PPF+'PLT_15_Scatter_Valor_Manutencao_Idade.png',dpi=200,bbox_inches='tight')
    
     
    fileName = PPF+"ET_07_Correlacao_Manutencao_Idade_GASOLINA.txt"
    extraComment = "\tCorrelacao GASOLINA Valor vs Idade."
    genCoorTest(yearAllGASOLINA, valueAllGASOLINA,fileName,extraComment)
    
    
    fileName = PPF+"ET_08_Correlacao_Manutencao_Idade_DIESEL.txt"
    extraComment = "\tCorrelacao DIESEL Valor vs Idade."
    genCoorTest(yearAllDIESEL, valueAllDIESEL,fileName,extraComment)

sys.exit("parada")
sys.exit("Depurando analise")
sys.exit("Escrita do artigo")  
LINEAR_MODEL = True