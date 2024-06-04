#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 26 14:37:56 2024

@author: adelino
"""

import pandas as pd
import sys
import numpy as np
from utils import extractValueColumn
import os
import matplotlib.pyplot as plt
import datetime

DEBUG = False
RAW_DATA_CSV_FILE = 'RAW_Ticket_Log_PCMG_19_22.csv'
RAW_NO_REP_DATA_CSV_FILE = 'PUB_Ticket_Log_PCMG_NOREP_19_22.csv'
RAW_NO_REP_BASE_DATA_CSV_FILE = 'PUB_Ticket_Log_PCMG_NOREP_BASE_19_22.csv'
PPF = os.path.basename(__file__).split("_")[0] + '_'

# -----------------------------------------------------------------------------
def extraiValor(strData):
    retVal = 0
    try:
        retVal = float(strData.strip().split(" ")[-1].replace(".","").replace(",","."))        
    except:
        return retVal
    return retVal    
# -----------------------------------------------------------------------------
def groupValue(strData):
   valorTotal = 0
   nRows = strData.shape[0]
   for i in range(0,nRows):
       valorTotal = valorTotal + strData.iloc[i]['Valor Total']
   if (nRows > 0):
       tempArr = strData.iloc[0,:]
   else:
       tempArr = strData.iloc[-1,:]
   tempArr['Valor Total'] = valorTotal
   return np.array(tempArr.values)
# -----------------------------------------------------------------------------
def joinDateGroup(df_Part):
    nRows = df_Part.shape[0]
    if (nRows == 1):
        lstUnique = np.array([])
        lstUnique = np.array(df_Part.values)
        return lstUnique
    else:
        lstUnique = np.array([])
        difDates = df_Part['Data Entrada Veículo'].unique()
        nDates = len(difDates)
        for k, date in enumerate(difDates):
            df_sub = df_Part[df_Part['Data Entrada Veículo'] == date]
            difPecas = df_Part['Grupo Peça'].unique()
            for j, peca in enumerate(difPecas):
                df_subPc = df_sub[df_sub['Grupo Peça'] == peca]
                if (df_subPc.shape[0] > 0):
                    if (len(lstUnique) == 0):
                        lstUnique = groupValue(df_subPc)
                    else:
                        lstUnique = np.vstack((lstUnique,groupValue(df_subPc)))
                else: 
                    continue
    return lstUnique
            
            
# --- REMOVE REPETICOES NA PLANILHA

selColsA = ['Placa', 'Família Segmento', 'Data Entrada Veículo','Veículo Modelo',
       'Tipo Manutenção Oficina',  'Grupo Peça', 'Ano Fab/Mod',
       'Dias na Oficina', 'Valor Total', 'MARCA', 'MODELO', 'PORTE',
       'COMBUSTÍVEL', 'Idade na Manut',
       'Classificação idade na Manut']

selColsB = ['Placa', 'Família Segmento','Data Entrada Veículo', 'Veículo Modelo',
       'Tipo Manutenção Oficina',  'Grupo Peça', 'Ano Fab/Mod',
       'Dias na Oficina', 'Valor Total', 'MARCA', 'MODELO', 'PORTE',
       'COMBUSTÍVEL', 'Idade na Manut',
       'Classificação idade na Manut']



if (not os.path.exists(RAW_NO_REP_DATA_CSV_FILE)):
    dfRawData = pd.read_csv(RAW_DATA_CSV_FILE,sep="\t")
    nRows, nCols  = dfRawData.shape
    nameCols = dfRawData.columns
    uniPlates = dfRawData['Placa'].unique()
    newPlate = []
    for k in range(0,len(uniPlates)):
        newPlate.append("HMG{:04d}".format(k))
    
    lstRows = []
    for i in range(0,nRows-1):
        rowI = dfRawData.iloc[i,:]
        idxFim = np.min([i+20,nRows])
        isUnique = True
        if not pd.isna(rowI['Data Entrada Veículo']):
            lastDate = rowI['Data Entrada Veículo']
        for j in range(i+1,idxFim):
            rowJ = dfRawData.iloc[j,:]
            isUnique = isUnique and (np.sum(rowI == rowJ) < nCols)
        if (isUnique):
            if pd.isna(rowI['Data Entrada Veículo']):
                rowI['Data Entrada Veículo'] = lastDate
            rowI['Valor Total'].value = extraiValor(rowI['Valor Total'])
            idxPlate = np.where(uniPlates == rowI['Placa'])[0][0]
            rowI['Placa'].value = newPlate[idxPlate]
            lstRows.append(rowI)
        
    # -- Filtra
    
    df_NoRepetition = pd.DataFrame(lstRows, columns=nameCols)
    df_NoRepetition.index = range(0,df_NoRepetition.shape[0])
    for i in range(0,df_NoRepetition.shape[0]):
        A = datetime.datetime.strptime(df_NoRepetition.loc[i,'Data Entrada Veículo'], "%d/%m/%Y").date()
        B = datetime.datetime.strptime(str(df_NoRepetition.loc[i,'Ano Fab/Mod']), "%Y").date()
        df_NoRepetition.loc[i,'Idade na Manut'] = int(np.floor((A-B).days/365))
        

    df_NoRepetition = df_NoRepetition[df_NoRepetition["PORTE"] == 'UTILITÁRIO']
    df_NoRepetition.index = range(0,df_NoRepetition.shape[0])
    df_NoRepetition = df_NoRepetition[selColsA]
    df_NoRepetition.to_csv(RAW_NO_REP_DATA_CSV_FILE, sep='\t', encoding='utf-8', index=False)



    
# --- CONSOLIDA VALORES

if (not os.path.exists(RAW_NO_REP_BASE_DATA_CSV_FILE)):
    dfRawData = pd.read_csv(RAW_NO_REP_DATA_CSV_FILE,sep="\t") 
    nameCols = dfRawData.columns
    numCols = len(nameCols)
    lstRows = np.array([])
    uniquePlates = np.unique(dfRawData['Placa'])
    for i, plate in enumerate(uniquePlates):
        sub_df = dfRawData[dfRawData["Placa"] == plate]
        lstUniqueDateGroup = joinDateGroup(sub_df)
        if (len(lstRows) == 0):
            lstRows = lstUniqueDateGroup
        else:
            lstRows = np.vstack((lstRows,lstUniqueDateGroup))
                    
    df_NoRepetition = pd.DataFrame(lstRows, columns=nameCols)
    df_NoRepetition.index = range(0,df_NoRepetition.shape[0])
    for i in range(0,df_NoRepetition.shape[0]):
        A = datetime.datetime.strptime(df_NoRepetition.loc[i,'Data Entrada Veículo'], "%d/%m/%Y").date()
        B = datetime.datetime.strptime(str(df_NoRepetition.loc[i,'Ano Fab/Mod']), "%Y").date()
        df_NoRepetition.loc[i,'Idade na Manut'] = int(np.floor((A-B).days/365))

    df_NoRepetition = df_NoRepetition[df_NoRepetition["PORTE"] == 'UTILITÁRIO']
    df_NoRepetition.index = range(0,df_NoRepetition.shape[0])
    df_NoRepetition = df_NoRepetition[selColsB]
    df_NoRepetition.to_csv(RAW_NO_REP_BASE_DATA_CSV_FILE, sep='\t', encoding='utf-8', index=False)