#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 10:09:19 2023

@author: adelino
"""
import numpy as np
from scipy import stats
import pandas as pd
from scipy.stats import f_oneway, tukey_hsd, pearsonr
import numbers
# -----------------------------------------------------------------------------
def descCorr(lstValA,lstTagA,lstValB,lstTagB, fileName):
    colName = ['  '] + lstTagB
    lstEstDesc = []
    
    for i, iData in enumerate(lstValA):
        vecR = []
        vecR.append(lstTagA[i])
        for j, jData in enumerate(lstValB):
            pRes = pearsonr(iData,jData)
            confInt = pRes.confidence_interval(0.95)
            pCoor = pRes.statistic
            strVals = '{:.2f} ({:.2f};{:.2f})'.format(pCoor,confInt.low,confInt.high)
            vecR.append(strVals.replace(".",","))
        lstEstDesc.append(vecR)
    
    dfDescEst = pd.DataFrame(lstEstDesc, columns=colName)
    dfDescEst.to_csv(fileName,sep='\t',decimal=',',float_format='%.2f')
# -----------------------------------------------------------------------------
def anovaResult(lstMedidas,tagLabel,mfileName):
    tagsComp = []
    limitsComp = []
    nVSn = []
    anova = f_oneway(*lstMedidas)
    result = tukey_hsd(*lstMedidas)
    conf = result.confidence_interval(confidence_level=.95)
    for ((i, j), l) in np.ndenumerate(conf.low):
        # filter out self comparisons
        if (i != j) and (j> i):
            h = conf.high[i,j]
            tagsComp.append("{:} vs. \n {:}".format(tagLabel[i],tagLabel[j]))
            limitsComp.append([l,h])
            nVSn.append(l*h)  
    valorp = anova.pvalue    
    with open(mfileName, "w") as f:
        print("Resultado Anova", file=f)
        print("Valor-p: {:}".format(anova.pvalue), file=f)
        print("Estatistica: {:}".format(anova.statistic), file=f)
        if (anova.pvalue < 0.05):
            print("Rejeita H0: pelo menos uma média é diferente",file=f)
        else:
            print("Falha em rejeitar H0: sem evidência para afirmar que uma média é diferente",file=f)
        for i in range(0,len(tagsComp)):
            print("{:}: low: {:.2f}; high: {:.2f}".format(tagsComp[i],limitsComp[i][0],limitsComp[i][1]),file=f)
    return tagsComp, limitsComp,  nVSn, valorp 
# -----------------------------------------------------------------------------
def removeOutLiers(vecData, percentage=5,base=[0.1,0.9]):
    N = len(vecData)
    cutIni = int(base[0]*percentage*N/100)
    cutFim = int(base[1]*percentage*N/100)
    vecData = np.sort(vecData)
    return vecData[cutIni:(N-cutFim)]
# -----------------------------------------------------------------------------
def extractValueColumn(dataFrame, colName = "Valor Total"):
    vecValCol = np.array([])
    if (isinstance(dataFrame[colName].iloc[0],str)):
        for vValue in dataFrame[colName]:
            x = vValue.find("R$")
            if (x < 0) and (colName == "Valor Total"):
                continue
            else:
                tValue =  '.'.join(vValue.strip().replace(".","").split(" ")[-1].split(","))    
                try:
                    rValue = float(tValue)            
                    vecValCol = np.append(vecValCol,rValue)
                except:
                    continue
    elif (isinstance(dataFrame[colName].iloc[0],numbers.Number)):
        for vValue in dataFrame[colName]:
            vecValCol = np.append(vecValCol,float(vValue))
    return vecValCol
# -----------------------------------------------------------------------------
def extractPairedValueColumn(dataFrame,pairLabel):
    vecValCol = np.array([])
    vecPair  = np.array([])
    if isinstance(dataFrame["Valor Total"].iloc[0],str):
        for idx, vValue in enumerate(dataFrame["Valor Total"]):
            x = vValue.find("R$")
            if (x < 0):
                continue
            else:
                tValue =  '.'.join(vValue.strip().replace(".","").split(" ")[-1].split(","))    
                try:
                    rValue = float(tValue)            
                    vecValCol = np.append(vecValCol,rValue)
                    pairVal = dataFrame[pairLabel].iloc[idx]
                    vecPair   = np.append(vecPair,pairVal)
                except:
                    continue
    elif (isinstance(dataFrame["Valor Total"].iloc[0],float)):
        for idx, vValue in enumerate(dataFrame["Valor Total"]):
            vecValCol = np.append(vecValCol,vValue)
            pairVal = dataFrame[pairLabel].iloc[idx]
            vecPair   = np.append(vecPair,pairVal)
    return vecValCol, vecPair
# -----------------------------------------------------------------------------
def genDescEst(genLabel,vecA,labelA,vecB,labelB,filename):
    descCol = [genLabel,'media', 'desvio padrao', 'simetria', 'curtose']
    descData  = [[labelA,np.mean(vecA),np.std(vecA),stats.skew(vecA),stats.kurtosis(vecA)],
                 [labelB,np.mean(vecB),np.std(vecB),stats.skew(vecB),stats.kurtosis(vecB)]]
    dfMomEst = pd.DataFrame(descData, columns=descCol) 
    dfMomEst.to_csv(filename, sep='\t', encoding='utf-8')
# -----------------------------------------------------------------------------
def genPercEst(genLabel,vecA,labelA,vecB,labelB,filename):
    descCol = [genLabel,'1o quartil', 'mediana', '3o quartil']
    descData  = [[labelA,np.percentile(vecA,25),np.percentile(vecA,50),np.percentile(vecA,75)],
                 [labelB,np.percentile(vecB,25),np.percentile(vecB,50),np.percentile(vecB,75)]]
    dfMomEst = pd.DataFrame(descData, columns=descCol) 
    dfMomEst.to_csv(filename, sep='\t', encoding='utf-8')
    
# -----------------------------------------------------------------------------
def genDecPercEst(genLabel,vecA,labelA,vecB,labelB,filename):
    descCol = [genLabel,'media', 'desvio padrao','1o quartil', 'mediana', '3o quartil', 'N']
    descData  = [[labelA,np.mean(vecA),np.std(vecA),np.percentile(vecA,25),np.percentile(vecA,50),np.percentile(vecA,75),len(vecA)],
                 [labelB,np.mean(vecB),np.std(vecB),np.percentile(vecB,25),np.percentile(vecB,50),np.percentile(vecB,75),len(vecB)]]
    dfMomEst = pd.DataFrame(descData, columns=descCol) 
    dfMomEst.to_csv(filename, sep='\t', encoding='utf-8')
# -----------------------------------------------------------------------------
def genDecPercEstUnique(genLabel,valuesA,labelA,filename):
    descCol = [genLabel,'média', 'desvio padrão','1o quartil', 'mediana', '3o quartil']
    descData = []
    for i, vecA in enumerate(valuesA):
        values = ["{:} ({:})".format(labelA[i],len(vecA)), 
                  "{:.2f} \r ({:.2f})".format(np.mean(vecA),np.sum(vecA)),
                  "{:.2f}".format(np.std(vecA)),
                  "{:.2f}".format(np.percentile(vecA,25)),
                  "{:.2f}".format(np.percentile(vecA,50)),
                  "{:.2f}".format(np.percentile(vecA,75))]
        strValues = [val.replace(".",",") for val in values]
        descData.append(strValues)
        
    dfMomEst = pd.DataFrame(descData, columns=descCol) 
    dfMomEst.to_csv(filename, sep='\t', encoding='utf-8', index=False)    
# -----------------------------------------------------------------------------
def genDiffMeanTest(vecA,vecB,filename,extraComment):
    with open(filename, "w") as f:
        print("Teste se as medias de gastos de veiculos gasolina e diesel sao iguais:", file=f)
        print(extraComment, file=f)
        print("Teste de Kolmogorov-Smirnov. H0: distribuiçoes identicas.", file=f)
        ksTest = stats.ks_2samp(vecA,vecB)
        print("Valor-p: {:}".format(ksTest.pvalue), file=f)
        if (ksTest.pvalue < 0.05):
            print("Rejeitou H0 -> distribuiçoes diferentes.", file=f)
        else:
            print("Falhou em rejeitar H0 -> distribuiçoes iguais.", file=f)
        print("Teste de Levene. H0: variancias iguais:", file=f)
        resLev = stats.levene(vecA,vecB)
        print("Valor-p: {:}".format(resLev.pvalue), file=f)
        if (resLev.pvalue < 0.05):
            print("Rejeitou H0 -> variancias diferentes:", file=f)
            eqVar = False
        else:
            print("Falhou em rejeitar H0 -> variancias iguais:", file=f)
            eqVar = True
        print("Teste T diferença entre medias. H0 médias iguais:", file=f)
        TtestResult = stats.ttest_ind(vecA,vecB, equal_var=eqVar)
        ci = TtestResult.confidence_interval()
        print("Valor-p: {:}".format(TtestResult.pvalue), file=f)
        print("Diferença entre as médias: {:}".format(np.mean(vecA) -np.mean(vecB)), file=f)
        print("Intervalo 95%: {:} a {:}".format(ci.low,ci.high), file=f)
        if (TtestResult.pvalue < 0.05):
            print("Rejeitou H0 -> medias diferentes.", file=f)
        else:
            print("Falhou em rejeitar H0 -> medias iguais.", file=f)
            
def genCoorTest(vecA,vecB,filename,extraComment):
    with open(filename, "w") as f:
        print("Teste se as variaveis de gastos de veiculos e correlacionada:", file=f)
        print(extraComment, file=f)
        print("Teste pearson da correlaçao. H0 variaveis descorrelacionadas:", file=f)
        TtestResult = stats.pearsonr(vecA,vecB)
        ci = TtestResult.confidence_interval()
        print("Valor-p: {:}".format(TtestResult.pvalue), file=f)
        print("Resultado, coef. de correlaçao (-1,+1): {:}".format(TtestResult.statistic), file=f)
        print("Intervalo 95%: {:} a {:}".format(ci.low,ci.high), file=f)
        if (TtestResult.pvalue < 0.05):
            print("Rejeitou H0 -> correlacionadas.", file=f)
        else:
            print("Falhou em rejeitar H0 -> descorrelacionadas.", file=f)