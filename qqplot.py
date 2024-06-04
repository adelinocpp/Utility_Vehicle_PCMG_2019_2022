#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 16:05:32 2024

@author: adelino
"""
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

def plot_qqplot(data,hAxis=None):
    # Normalizando os dados
    usePLT = False
    if (hAxis == None):
        # usePLT = True
        hAxis = plt
    normalized_data = data # (data - np.mean(data)) / np.std(data)
    # normalized_data = (data - np.mean(data)) / np.std(data)
    # Quantis teóricos e amostrais
    # (osm, osr), (slope, intercept, _) = stats.probplot(normalized_data, dist="norm", plot=None)
    
    # Calculando os quantis teóricos e os quantis amostrais
    osm, osr = np.sort(stats.norm.ppf((np.arange(1, len(data) + 1) - 0.5) / len(data))), np.sort(data)
    
    # Estimando a linha de referência
    slope, intercept = np.polyfit(osm, osr, 1)
    
    # Plotando o QQ plot
    hAxis.scatter(osm, osr, color='0.65', alpha=0.65, label='Quantis amostrais')
    
    # Linha de referência
    hAxis.plot(osm, slope * osm + intercept, color='0.25', linestyle='-', label='Linha de referência')
    # Curvas pontilhadas para limites de confiança de 95%
    n = len(data)
    alpha = 0.05
    z = stats.norm.ppf(1 - alpha / 2)
    se_line = z * np.sqrt((1.0 / n) + (osm**2 / (n - 1)))
    fit_line = slope * osm + intercept
    
    lower_bound = fit_line - se_line * np.std(data)
    upper_bound = fit_line + se_line * np.std(data)
    
    
    # Plotando as curvas de confiança
    hAxis.plot(osm, lower_bound, linestyle='--', color='0.75', label='Limites intervalo de 95%')
    hAxis.plot(osm, upper_bound, linestyle='--', color='0.75')


    return hAxis