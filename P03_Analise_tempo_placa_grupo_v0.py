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
from utils import extractValueColumn, genDiffMeanTest, anovaResult, \
                    genDecPercEstUnique
from scipy.stats import pearsonr                    
from pirateplot import pirateplot
boxprops = dict(linestyle='-', linewidth=2.5, color='black')
medianprops = dict(linestyle='-', linewidth=2.5, color='gray')

plt.rcParams['image.cmap'] = 'gist_gray'
'''
xData = []
xLabel = []
for i in range(0,5):
    xData.append(np.random.randn(10))
    xLabel.append("data {:02d}".format(i))

pirateplot(xData,xLabel,'PiratePlot_00.png','Titulo','Classes','quantidde')
sys.exit(" --- Teste Pirate plot ---")
'''

def func(pct, allvals):
    absolute = int(np.round(pct/100.*np.sum(allvals)))
    return f"{pct:.1f}%\n({absolute:d})".replace(".",",")

def funcRBL(pct, allvals):
    absolute = int(np.round(pct/100.*np.sum(allvals)))
    return f"{pct:.1f}%\nR$ {absolute:d}".replace(".",",")

def pearsonRes(xval,yval):
    pRes = pearsonr(xval,yval)
    confInt = pRes.confidence_interval(0.95)
    pCoor = pRes.statistic
    strVals = '{:.2f} ({:.2f};{:.2f})'.format(pCoor,confInt.low,confInt.high)
    return strVals.replace(".",","), pCoor
    
# =============================================================================
PPF = os.path.basename(__file__).split("_")[0] + '_'
DATA_PLACA_CSV_FILE = 'PUB_Ticket_Log_PCMG_PLACA_UNICA_19_22.csv'
DATA_PECA_CSV_FILE = 'PUB_Ticket_Log_PCMG_NOREP_BASE_19_22.csv'


df_Placa = pd.read_csv(DATA_PLACA_CSV_FILE,sep="\t")
df_Peca  = pd.read_csv(DATA_PECA_CSV_FILE,sep="\t")

# df_Placa = df_Placa[df_Placa["PORTE"] == 'UTILITÁRIO']
# df_Peca = df_Peca[df_Peca["PORTE"] == 'UTILITÁRIO']


dictJoin = {}
lstManuJoin = []
lstIntvJoin = []
lstNumManuJoin = []
for i in range(0,df_Peca.shape[0]):
    plate = df_Peca["Placa"].iloc[i]
    dfTemp = df_Placa[df_Placa["Placa"] == plate]
    lstNumManuJoin.append(dfTemp['Num Manutencoes'].values[0])
    lstManuJoin.append(dfTemp['Manutencoes'].values[0])
    lstIntvJoin.append(dfTemp['Intervalo'].values[0])

dictJoin['Num Manutencoes'] = lstNumManuJoin
dictJoin['Manutencoes'] = lstManuJoin
dictJoin['Intervalo'] = lstIntvJoin
other = pd.DataFrame(dictJoin)
df_Peca = df_Peca.join(other)
    
colPlaca = df_Placa.columns
colPeca = df_Placa.columns

boolRunAll = True

# ---Apenas utilitarios 


lstTypeComb = df_Placa["COMBUSTÍVEL"].unique()
lstTypePeca = df_Peca["Grupo Peça"].unique()
lstTypeManu = df_Placa["Manutencoes"].unique()
tagManutençoes = [" 1 "," 2 - 3"," < 3"]
tagManutençoes = [" uma "," duas ou três"," acima de três"]



# -----------------------------------------------------------------------------

dfGASOLINA = df_Peca[df_Peca["COMBUSTÍVEL"] == 'GASOLINA']
dfDIESEL = df_Peca[df_Peca["COMBUSTÍVEL"] == 'DIESEL']

dfManu_01 = df_Peca[df_Peca["Manutencoes"] == 0]
dfManu_02 = df_Peca[df_Peca["Manutencoes"] == 1]
dfManu_04 = df_Peca[df_Peca["Manutencoes"] == 2]

tagDuasManut = [" duas ou três"," acima de três"]
lstTempoBetween = []
lstTempoBetween.append(extractValueColumn(dfManu_02,'Intervalo'))
lstTempoBetween.append(extractValueColumn(dfManu_04,'Intervalo'))

lstTypePecaSel = ['MOTOR', 'ELETRICA', 'FREIO', 'SUSPENSAO', 'TRANSMISSAO']
lstTypePeca = df_Peca["Grupo Peça"].unique()
lstGrupoPeca = []
tagGrupoPeca = []
lstValoresOutrasPecas = []
lstOutrasPecas = []
numOutras = 0
for tpManu in lstTypePeca:
    dfTemp = df_Peca[df_Peca["Grupo Peça"] == tpManu]
    if (tpManu in lstTypePecaSel):
        lstGrupoPeca.append(extractValueColumn(dfTemp))
        tagGrupoPeca.append(tpManu)
    elif(dfTemp.shape[0] > 0):
        arrayTemp = extractValueColumn(dfTemp)
        lstValoresOutrasPecas = list(np.hstack((lstValoresOutrasPecas,extractValueColumn(dfTemp))))
        lstOutrasPecas.append(tpManu)
        numOutras +=dfTemp.shape[0]
        
tagGrupoPeca.append('OUTRAS')
lstGrupoPeca.append(lstValoresOutrasPecas)

FIG_BOXPLOT_ALL = boolRunAll
vecValorGaso = extractValueColumn(dfGASOLINA)
vecValorDiesel = extractValueColumn(dfDIESEL)
genDiffMeanTest(vecValorGaso,vecValorDiesel,PPF+'Teste_t_diferenca_Gas_Diesel.txt',
                'Comparção dos valores de manutenção de utilitários gasolina e Diesel' )
if (FIG_BOXPLOT_ALL):
    fig = plt.figure(figsize =(6, 8))
    plt.title("Valores de manutenção em R$")
    plt.ylabel('Valor de manutenção')
    plt.boxplot([vecValorGaso,vecValorDiesel],boxprops=boxprops,medianprops=medianprops)
    plt.xticks([1,2],["GASOLINA", "DIESEL"])
    plt.grid(color='gray', linestyle='-.', linewidth=0.5)
    plt.savefig(PPF+'PLT_01_BoxPlot_Bruta_All.png',dpi=200,bbox_inches='tight')
    
    
    
    
lstCombustivel = []
lstCombustivel.append(extractValueColumn(dfGASOLINA))
lstCombustivel.append(extractValueColumn(dfDIESEL))

lstManutencao = []
lstManutencao.append(extractValueColumn(dfManu_01))
lstManutencao.append(extractValueColumn(dfManu_02))
lstManutencao.append(extractValueColumn(dfManu_04))

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

# lstTagSelMarcas = [tag.lower().title() for tag in lstTagSelMarcas]

fig = plt.figure(figsize =(8,4))
plt = pirateplot(lstValoresMarca,lstTagSelMarcas)
plt.title("Valores, medidas descritivas e inferenciais de manutenção",fontsize=16)
plt.ylabel('Valor de manutenção (R$)',fontsize=14)
plt.xlabel('Montadora',fontsize=14)
plt.savefig(PPF+'Valor_Manutencoes_RDI_por_Marca_00.png',dpi=200,bbox_inches='tight')   

tagsComp, limitsComp, nVSn, _ = anovaResult(lstValoresMarca,lstTagSelMarcas,
                                            PPF+'Anova_Montadora.txt')
meanPeca = [0.5*(limitsC[1] + limitsC[0]) for limitsC in limitsComp]
limitsAnova = np.array([ [m-lim[0],lim[1]-m] for lim, m in zip(limitsComp,meanPeca)] )
fig = plt.figure(figsize =(6,8))
plt.errorbar(meanPeca,range(0,len(meanPeca)),xerr=limitsAnova.T,
             linestyle=' ',marker='s', capsize=4, color='0.35')
plt.plot([0,0],[-0.5,len(meanPeca)-0.5], linestyle='-.',linewidth=2, color='black')
plt.yticks(range(0,len(meanPeca)),tagsComp)
plt.title("Comparação dos valores de manutenção por montadora",fontsize=16)
plt.grid(color='gray', linestyle='-.', linewidth=0.5)
plt.xlabel('Diferença de valor de manutenção (R$)',fontsize=14)
plt.ylim([-0.5,len(meanPeca)-0.5])
plt.savefig(PPF+'ANOVA_Montadora_00.png',dpi=200,bbox_inches='tight')



fig, ax1 = plt.subplots(nrows=1, ncols=2,figsize =(16, 6))
ax1[0] = pirateplot(lstValoresMarca,lstTagSelMarcas,ax1[0])
ax1[0].set_title("Valores, medidas descritivas e inferenciais de manutenção")
ax1[0].set_ylabel('Valor de manutenção (R$)')
ax1[0].set_xlabel('Montadora')

ax1[1].errorbar(meanPeca,range(0,len(meanPeca)),xerr=limitsAnova.T,
             linestyle=' ',marker='s', capsize=4, color='0.35')
ax1[1].plot([0,0],[-0.5,len(meanPeca)-0.5], linestyle='-.',linewidth=2, color='black')
ax1[1].set_yticks(range(0,len(meanPeca)),tagsComp)
ax1[1].set_title("Comparação dos valores de manutenção por montadora",fontsize=16)
plt.grid(color='gray', linestyle='-.', linewidth=0.5)
ax1[1].set_xlabel('Diferença de valor de manutenção (R$)',fontsize=14)
ax1[1].set_ylim([-0.5,len(meanPeca)-0.5])

plt.savefig(PPF+'RDI_ANOVA_Valor_Manutencoes_por_Marca_00.png',dpi=200,bbox_inches='tight')  

genDecPercEstUnique('Montadora',lstValoresMarca,lstTagSelMarcas,PPF+'Tabela_montadora.csv')



fig = plt.figure(figsize =(6,8))
plt = pirateplot(lstCombustivel,lstTypeComb)
plt.title("Valores de manutenção em R$",fontsize=16)
plt.ylabel('Valor de manutenção (R$)',fontsize=14)
plt.xlabel('Combustível',fontsize=14)
plt.savefig(PPF+'Combusticel_Utilitario_00.png',dpi=200,bbox_inches='tight')



fig = plt.figure(figsize =(6,8))
plt = pirateplot(lstManutencao,tagManutençoes)
plt.title("Valores de manutenção em R$",fontsize=16)
plt.ylabel('Valor de manutenção (R$)',fontsize=14)
plt.xlabel('Número de manutenções',fontsize=14)
plt.savefig(PPF+'Manutencoes_Utilitario_00.png',dpi=200,bbox_inches='tight')
 
tagsComp, limitsComp, nVSn, _ = anovaResult(lstManutencao,tagManutençoes,
                                            PPF+'Anova_NumManutencoes.txt')
meanPeca = [0.5*(limitsC[1] + limitsC[0]) for limitsC in limitsComp]
limitsAnova = np.array([ [m-lim[0],lim[1]-m] for lim, m in zip(limitsComp,meanPeca)] )
fig = plt.figure(figsize =(6,8))
plt.errorbar(meanPeca,range(0,len(meanPeca)),xerr=limitsAnova.T,
             linestyle=' ',marker='s', capsize=4, color='0.35')
plt.plot([0,0],[-0.5,len(meanPeca)-0.5], linestyle='-.',linewidth=2, color='black')
plt.yticks(range(0,len(meanPeca)),tagsComp)
plt.title("Comparação dos valores por nume de ocorrências",fontsize=16)
plt.grid(color='gray', linestyle='-.', linewidth=0.5)
plt.xlabel('Diferença de valor de manutenção (R$)',fontsize=14)
plt.ylim([-0.5,len(meanPeca)-0.5])
plt.savefig(PPF+'Anova_NumManutencoes.png',dpi=200,bbox_inches='tight')



fig = plt.figure(figsize =(10,8))
plt = pirateplot(lstGrupoPeca,tagGrupoPeca,tckAngle=45)
plt.title("Valores de manutenção em R$",fontsize=16)
plt.ylabel('Valor de manutenção (R$)',fontsize=14)
plt.xlabel('Tipo de manutenção',fontsize=14)
plt.savefig(PPF+'RDI_Peca_Utilitario_00.png',dpi=200,bbox_inches='tight')


tagsComp, limitsComp, nVSn, _ = anovaResult(lstGrupoPeca,tagGrupoPeca,
                                            PPF+'Anova_nGrupo_peca.txt')
meanPeca = [0.5*(limitsC[1] + limitsC[0]) for limitsC in limitsComp]
limitsAnova = np.array([ [m-lim[0],lim[1]-m] for lim, m in zip(limitsComp,meanPeca)] )
fig = plt.figure(figsize =(6,8))
plt.errorbar(meanPeca,range(0,len(meanPeca)),xerr=limitsAnova.T,
             linestyle=' ',marker='s', capsize=4, color='0.35')
plt.plot([0,0],[-0.5,len(meanPeca)-0.5], linestyle='-.',linewidth=2, color='black')
plt.yticks(range(0,len(meanPeca)),tagsComp)
plt.title("Comparação dos valores de manutenção por grupo de peça")
plt.grid(color='gray', linestyle='-.', linewidth=0.5)
plt.xlabel('Diferença de valor de manutenção (R$)')
plt.ylim([-0.5,len(meanPeca)-0.5])
plt.savefig(PPF+'ANOVA_Grupo_pecas_00.png',dpi=200,bbox_inches='tight')


genDecPercEstUnique('Manutenção',lstGrupoPeca,tagGrupoPeca,PPF+'Tabela_Grupo_Peca.csv')

fig, ax1 = plt.subplots(nrows=1, ncols=2,figsize =(16, 6))
ax1[0] = pirateplot(lstGrupoPeca,tagGrupoPeca,ax1[0],tckAngle=45)
ax1[0].set_title("Valores de manutenção em R$")
ax1[0].set_ylabel('Valor de manutenção (R$)')
ax1[0].set_xlabel('Tipo de manutenção')

ax1[1].errorbar(meanPeca,range(0,len(meanPeca)),xerr=limitsAnova.T,
             linestyle=' ',marker='s', capsize=4, color='0.35')
ax1[1].plot([0,0],[-0.5,len(meanPeca)-0.5], linestyle='-.',linewidth=2, color='black')
ax1[1].set_yticks(range(0,len(meanPeca)),tagsComp,fontsize=8)
ax1[1].set_title("Comparação dos valores de manutenção por grupo de peça")
ax1[1].grid(color='gray', linestyle='-.', linewidth=0.5)
ax1[1].set_xlabel('Diferença de valor de manutenção (R$)')
ax1[1].set_ylim([-0.5,len(meanPeca)-0.5])
plt.savefig(PPF+'RDI_ANOVA_Grupo_pecas_00.png',dpi=200,bbox_inches='tight')


genDiffMeanTest(lstTempoBetween[0],lstTempoBetween[1],PPF+'Teste_t_diferenca_Intervalo_manutencao.txt',
                'Comparação dos intervalos entre manutenções de utilitários' )

fig = plt.figure(figsize =(6,8))
plt = pirateplot(lstTempoBetween,tagDuasManut)
plt.title("Intervalo entre manutenções",fontsize=16)
plt.ylabel('Dias entre manutenções',fontsize=14)
plt.xlabel('Número de manutenções',fontsize=14)
plt.savefig(PPF+'PP_Intervalo_Manutencao_00.png',dpi=200,bbox_inches='tight')



fig, ax1 = plt.subplots(nrows=1, ncols=2,figsize =(16, 6))
ax1[0] = pirateplot(lstTempoBetween,tagDuasManut,ax1[0])
ax1[0].set_title("Intervalo entre manutenções",fontsize=16)
ax1[0].set_ylabel('Dias entre manutenções',fontsize=14)
ax1[0].set_xlabel('Número de manutenções',fontsize=14)
ax1[1] = pirateplot(lstCombustivel,lstTypeComb,ax1[1])
ax1[1].set_title("Valores de manutenção em R$")
ax1[1].set_ylabel('Valor de manutenção (R$)')
ax1[1].set_xlabel('Combustível')
plt.savefig(PPF+'RDI_Intervalo_Combusticel_Utilitario_00.png',dpi=200,bbox_inches='tight')

genDecPercEstUnique('Grupo manutenções',lstTempoBetween,tagDuasManut,PPF+'Tabela_Grupo_manutencoes.csv')
genDecPercEstUnique('Combustível',lstCombustivel,lstTypeComb,PPF+'Tabela_combustível.csv')

piecmap = ['{:.2f}'.format(i) for i in np.linspace(0,0.7,len(lstTypePecaSel))]

fig = plt.figure(figsize =(16,8))
gs = fig.add_gridspec(nrows=2, ncols=3,wspace=0.0,hspace=0.0)
ax = gs.subplots(sharex=False,sharey=False)
for j, comb in enumerate(lstTypeComb):
    cond2 = df_Peca["COMBUSTÍVEL"] == comb
    for i, numManu in enumerate(lstTypeManu):
        sizes = []
        prices = []
        cond3 = df_Peca["Manutencoes"] == numManu
        for tpManu in lstTypePecaSel:
            cond1 = df_Peca["Grupo Peça"] == tpManu
            dfTemp = df_Peca[cond1 & cond2 & cond3]
            if (dfTemp.shape[0] < 1):
                continue
            
            prices.append(np.sum(extractValueColumn(dfTemp,'Num Manutencoes')))
            sizes.append(dfTemp.shape[0])
        # ax[i,j].axis('off')
        
        wedges, texts, autotexts = ax[j,i].pie(sizes, 
                                  autopct=lambda pct: func(pct, sizes),
                                  textprops=dict(color="w"),colors=piecmap)       
        # pctVec = [ np.round(100*pct/np.sum(sizes)) for pct in sizes]
        # wedges, texts, autotexts = labPer = ["{:}\n{:.1f}% ({:d})".format(n,p,v) for n,p,v in zip(lstTypePeca,pctVec,sizes) ]
        # ax[i,j].pie(sizes, labels=labPer)
fig.legend(wedges, lstTypePeca,
          title="Grupo peça",
          loc="upper center",ncols=3,
          bbox_to_anchor=(0.25, -0.05, 0.5, 1))
fig.suptitle("Numero de ocorrências de manutenção")        
ax[0,0].set_ylabel('Gasolina')
ax[1,0].set_ylabel('Diesel')
ax[1,0].set_xlabel('Uma manutenção')
ax[1,1].set_xlabel('duas a três manutenções')
ax[1,2].set_xlabel('acima de três manutençoes')
plt.savefig(PPF+'Pizza_Numero_manutencao.png',dpi=200,bbox_inches='tight')



fig = plt.figure(figsize =(16,8))

gs = fig.add_gridspec(nrows=2, ncols=3,wspace=-.4,hspace=-.1)
ax = gs.subplots(sharex=False,sharey=False)
for j, comb in enumerate(lstTypeComb):
    cond2 = df_Peca["COMBUSTÍVEL"] == comb
    for i, numManu in enumerate(lstTypeManu):
        sizes = []
        prices = []
        cond3 = df_Peca["Manutencoes"] == numManu
        for tpManu in lstTypePecaSel:
            cond1 = df_Peca["Grupo Peça"] == tpManu
            dfTemp = df_Peca[cond1 & cond2 & cond3]
            if (dfTemp.shape[0] < 1):
                continue
            prices.append(np.sum(extractValueColumn(dfTemp)))
            sizes.append(dfTemp.shape[0])
        # ax[i,j].axis('off')
        prices = np.array(prices)/sizes
        wedges, texts, autotexts = ax[j,i].pie(prices, 
                                  autopct=lambda pct: funcRBL(pct, prices),pctdistance=0.75,
                                  textprops=dict(color="w", fontsize=10),colors=piecmap)       
        # pctVec = [ np.round(100*pct/np.sum(sizes)) for pct in sizes]
        # wedges, texts, autotexts = labPer = ["{:}\n{:.1f}% ({:d})".format(n,p,v) for n,p,v in zip(lstTypePeca,pctVec,sizes) ]
        # ax[i,j].pie(sizes, labels=labPer)
fig.legend(wedges, lstTypePecaSel,
          title="Grupo peça",
          loc="upper center",ncols=3,
          bbox_to_anchor=(0.25, -0.05, 0.5, 1))
fig.suptitle("Custo médio de manutenção")        
ax[0,0].set_ylabel('Gasolina')
ax[1,0].set_ylabel('Diesel')
ax[1,0].set_xlabel('Uma manutenção')
ax[1,1].set_xlabel('Duas a três manutenções')
ax[1,2].set_xlabel('Acima de três manutençoes')
plt.savefig(PPF+'Pizza_Preco_manutencao.png',dpi=200,bbox_inches='tight')


fig = plt.figure(figsize =(16,8))

gs = fig.add_gridspec(nrows=2, ncols=3,wspace=0.0,hspace=0.0)
ax = gs.subplots(sharex=False,sharey=False)
for j, comb in enumerate(lstTypeComb):
    cond2 = df_Peca["COMBUSTÍVEL"] == comb
    for i, numManu in enumerate(lstTypeManu):
        sizes = []
        prices = []
        cond3 = df_Peca["Manutencoes"] == numManu
        for tpManu in lstTypePecaSel:
            cond1 = df_Peca["Grupo Peça"] == tpManu
            dfTemp = df_Peca[cond1 & cond2 & cond3]
            if (dfTemp.shape[0] < 1):
                continue
            prices.append(np.sum(extractValueColumn(dfTemp)))
            sizes.append(dfTemp.shape[0])
        # ax[i,j].axis('off')
        prices = np.array(prices)/sizes
        
        tagPrices = [funcRBL(pct, prices) for pct in prices]
        
        wedges, texts = ax[j,i].pie(prices, colors=piecmap) # wedgeprops=dict(width=0.5),
    
        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
        kw = dict(arrowprops=dict(arrowstyle="-"),
                  bbox=bbox_props, zorder=0, va="center")
        
        for n, p in enumerate(wedges):
            ang = (p.theta2 - p.theta1)/2. + p.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = f"angle,angleA=0,angleB={ang}"
            kw["arrowprops"].update({"connectionstyle": connectionstyle})
            ax[j,i].annotate(tagPrices[n], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                        horizontalalignment=horizontalalignment, **kw)

        
fig.legend(wedges, lstTypePeca,
          title="Grupo peça",
          loc="upper center",ncols=3,
          bbox_to_anchor=(0.25, -0.05, 0.5, 1))
fig.suptitle("Custo médio de manutenção")        
ax[0,0].set_ylabel('Gasolina')
ax[1,0].set_ylabel('Diesel')
ax[1,0].set_xlabel('uma manutenção')
ax[1,1].set_xlabel('duas a três manutenções')
ax[1,2].set_xlabel('acima de três manutençoes')
plt.savefig(PPF+'Pizza_Preco_manutencao_v2.png',dpi=200,bbox_inches='tight')



colorDie="0.35"
colorGas="0.75"


fatoresCoor = ['Dias na Oficina', 'Idade na Manut', 'Num Manutencoes', 'Intervalo']
fatoresCoorTag = ['Dias na Oficina', 'Idade na Manut. (Anos)', 'Num. Manutenções (un)', 'Intervalo entre Man. (dias)']
lstCorrGas = []
lstCorrDie = []
lstCorrAmbos = []
fig = plt.figure(figsize =(15,12))
gs = fig.add_gridspec(nrows=4, ncols=5,wspace=0.2,hspace=0.1)
ax = gs.subplots(sharex=True,sharey=False)
valMin = [np.floor(np.min(df_Peca[sel])/5)*5 for sel in fatoresCoor]
valMax = [np.ceil(np.max(df_Peca[sel])/5)*5 for sel in fatoresCoor]
prcMin = np.floor(np.min(extractValueColumn(df_Peca))/5)*5
prcMax = np.ceil(np.max(extractValueColumn(df_Peca))/5)*5

tpManuTag = ['Motor', 'Elétrica', 'Freio', 'Suspensão', 'Transmissão', 'Outras']
tpManuTagJst = ['Motor', 'Elétrica', 'Freio', 'Suspensão', 'Transmissão']

for i, factorC in enumerate(fatoresCoor):
    colCorrGas = []
    colCorrDie = []
    colCorrGas.append(factorC)
    colCorrDie.append(factorC)
    for j, tpManu in enumerate(lstTypePecaSel):
        cond1 = df_Peca["Grupo Peça"] == tpManu
        condGas = df_Peca["COMBUSTÍVEL"] == 'GASOLINA'
        condDie = df_Peca["COMBUSTÍVEL"] == 'DIESEL'
        dfGas = df_Peca[cond1 & condGas]
        dfDie = df_Peca[cond1 & condDie]
        Xgas = extractValueColumn(dfGas)
        Xdie = extractValueColumn(dfDie)
        Ygas = extractValueColumn(dfGas,factorC)
        Ydie = extractValueColumn(dfDie,factorC)
        txtRhoG, rhoG = pearsonRes(Xgas,Ygas)
        txtRhoD, rhoD = pearsonRes(Xdie,Ydie)
        colCorrGas.append(txtRhoG)
        colCorrDie.append(txtRhoD)
        if (i == 0) and (j==0):
            ax[i,j].scatter(Xgas,Ygas,color=colorGas,alpha=0.25, label='Gasolina')
            ax[i,j].scatter(Xdie,Ydie,color=colorDie,alpha=0.25, label='Diesel')
        else:
            ax[i,j].scatter(Xgas,Ygas,color=colorGas,alpha=0.25)
            ax[i,j].scatter(Xdie,Ydie,color=colorDie,alpha=0.25)
        if (i == 0):
            ax[i,j].set_title(tpManuTag[j])
        if (j == 0):
            ax[i,j].set_ylabel(fatoresCoorTag[i])
        # ax[i,j].set_xlabel(factorC)
        ax[i,j].annotate("Gas: p = {:.2f} \nDie: p = {:.2f} ".format(rhoG,rhoD), xy=(0.45,0.8),xycoords='axes fraction',
             )
        ax[i,j].set_xlim([prcMin,prcMax])
        ax[i,j].set_ylim([valMin[i],valMax[i]])
        ax[i,j].scatter(Xdie,Ydie,color=colorDie,alpha=0.25)
        ax[i,j].grid(color='gray', linestyle='-.', linewidth=0.5)
        
    lstCorrGas.append(colCorrGas)
    lstCorrDie.append(colCorrDie)
    lstCorrAmbos.append(['GASOLINA'] + colCorrGas)
    lstCorrAmbos.append(['DIESEL'] + colCorrDie)
    
fig.legend( #wedges, lstTypePeca,
#           title="",
           loc="upper center",ncols=2,
           bbox_to_anchor=(0.25, -0.05, 0.5, 1))
fig.suptitle("Correlação do valor de manutenção")   
plt.savefig(PPF+'Scatter_Corr_manutencao.png',dpi=200,bbox_inches='tight')
    
dfCorrAmbos = pd.DataFrame(lstCorrAmbos, columns=['Combustível','Variável'] + tpManuTagJst)   
dfCorrGas = pd.DataFrame(lstCorrGas, columns=['Variável'] + tpManuTagJst)     
dfCorrDie = pd.DataFrame(lstCorrDie, columns=['Variável'] + tpManuTagJst)

dfCorrGas.to_csv(PPF+'TabelaCorrelacao_Gasolina.csv', sep='\t', encoding='utf-8', index=False)
dfCorrDie.to_csv(PPF+'TabelaCorrelacao_Diesel.csv', sep='\t', encoding='utf-8', index=False)
dfCorrAmbos.to_csv(PPF+'TabelaCorrelacao_Juntos.csv', sep='\t', encoding='utf-8', index=False)

sys.exit(" ---   ")