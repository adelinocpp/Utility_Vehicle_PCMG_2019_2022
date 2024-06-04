#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 27 08:03:14 2024

% It is not a help text
% xData:    cell where each row is a data set
% vLabel:   cell of strings with same length of "xData"
% ici:      Confidence interval of mean, computed whit frequentist approach
% Paleta:   Color palate, e.g. jet or gray  
%
% This function is a copy of work of Nathaniel Phillips (he create pirate plot, I just adapted):
%
% Phillips, N.D., 2017. YaRrr! The Pirate’s Guide to R. APS Observer, 30(3).
%
% URL: https://scholar.google.ch/citations?view_op=view_citation&hl=en&user=ThWbpDQAAAAJ&citation_for_view=ThWbpDQAAAAJ:dTyEYWd-f8wC
%
%
% Brasil, maio de 2024
% Adelino P. Silva
% adelinocpp@gmail.com
% Telegram +55 31 9 8801-3605
@author: adelino
"""
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from sklearn.neighbors import KernelDensity
from scipy.stats import t
from scipy import stats

def pirateplot(xData,vLabel, hAxis = None, tckAngle = 0, ici=0.95,Paleta='gist_gray', bool_JitterNorm=True,real_MaxJitter=0.1 ):
    nData = len(xData)
    
    usePLT = False
    if (hAxis == None):
        usePLT = True
        hAxis = plt
    yLimMax = -np.inf;
    yLimMin = np.inf;
    vec_X = np.zeros((nData,))
    for i, data in enumerate(xData):
        vec_X[i] = 2*i + 1
        yLimMax = np.max(np.concatenate([data, [yLimMax]]))
        yLimMin = np.min(np.concatenate([data, [yLimMin]]))
    xLimMax = int(vec_X[-1] + 1)
    xLimMin = int(vec_X[0] - 1)
    
    strLabel = []
    k = 0
    for i in range(xLimMin,xLimMax):
        if (i in vec_X):
            strLabel.append(vLabel[k])        
            k += 1
        else:
            strLabel.append('')
        
    
    numDens = 200
    yDens = np.linspace(yLimMin,yLimMax,numDens)
    
    cDens  = []
    cYDens = []
    cMean  = []
    cEP    = []
    cCI    = []
    xScat  = []
    xDenFill = []
    yDenFill = []
    for i, data in enumerate(xData):
        ix = np.min(data)
        mx = np.max(data)
        sx = np.std(data)
        yDens = np.linspace(ix - 0.25*sx, mx + 0.25*sx,numDens);
        
        yLimMax = np.max(np.concatenate([yDens, [yLimMax]]))
        yLimMin = np.min(np.concatenate([yDens, [yLimMin]]))
        
        npt = len(data)
        # xDens = ksdensity(,yDens,'Kernel','triangle');
        # kde = KernelDensity(kernel='linear').fit(np.array(data).reshape(-1,1)) # , bandwidth=0.2
        # xDens = np.exp(kde.score(yDens.reshape(-1,1)))
        kernel = stats.gaussian_kde(data)
        xDens = kernel(yDens)
        xDens = 0.9*xDens/np.max(xDens)
        
        xDenFill.append(np.concatenate((vec_X[i] - xDens, np.flip(vec_X[i] + xDens))))
        yDenFill.append(np.concatenate((yDens, np.flip(yDens))))
        
        if (bool_JitterNorm):
            xScat.append(vec_X[i]*np.ones((npt,)) + real_MaxJitter*np.random.randn(npt)/3 )
        else:
            xScat.append(vec_X[i]*np.ones((npt,)) + real_MaxJitter*(np.random.rand(npt)-0.5))
        
        cDens.append(xDens)
        cMean.append(np.mean(data))
        cYDens.append(yDens)
        cEP.append(np.std(data)/np.sqrt(npt))
        cCI.append(t.ppf(1 - 0.5*(1-ici),npt-1))
    
    
    
    cmap = mpl.colormaps[Paleta]
    colors = cmap(np.linspace(0, 0.75, nData))
    
    
    
    
    yLimMin = np.floor(yLimMin*10)/10
    yLimMax = np.ceil(yLimMax*10)/10
    
    for i in range(0,nData):
        curColor = colors[i]
        curColor[3] = 0.25
        icColor = colors[i]
        icColor[3] = 0.45
        xMed = [vec_X[i] - 0.8, vec_X[i] + 0.8]
        yMed = [cMean[i], cMean[i]]
        hAxis.plot(xMed,yMed,linestyle='-',linewidth=2, color='black')
        xICMed = [vec_X[i] - 0.7, vec_X[i] - 0.7, vec_X[i] + 0.7, vec_X[i] + 0.7];
        yICMed = [cMean[i] - cEP[i]*cCI[i], cMean[i] + cEP[i]*cCI[i], cMean[i] + cEP[i]*cCI[i], cMean[i] - cEP[i]*cCI[i]]
        hAxis.fill(xICMed,yICMed,color=icColor)
        
        hAxis.fill(xDenFill[i],yDenFill[i],color=curColor)        
        hAxis.plot(vec_X[i] + cDens[i],cYDens[i],linestyle='-',linewidth=0.5, color=colors[i])
        hAxis.plot(vec_X[i] - cDens[i],cYDens[i],linestyle='-',linewidth=0.5, color=colors[i])
        hAxis.scatter(xScat[i],xData[i],color=colors[i])

    if (usePLT):
        hAxis.xticks(range(xLimMin,xLimMax),strLabel,rotation=tckAngle)
        hAxis.xlim([xLimMin, xLimMax])
        hAxis.ylim([yLimMin, yLimMax])
        hAxis.grid(color='gray', linestyle='-.', linewidth=0.5)
    else:
        hAxis.set_xticks(range(xLimMin,xLimMax),strLabel,rotation=tckAngle)
        hAxis.set_xlim([xLimMin, xLimMax])
        hAxis.set_ylim([yLimMin, yLimMax])
        hAxis.grid(color='gray', linestyle='-.', linewidth=0.5)
    
    return hAxis