# Modelo de Gasto de Manutenção de veículos Utilitários

### Códigos e dados referentes ao estudo de gasto de manutenção de veículos utilitários da frota de veículos da PCMG.

Por: 
Adelino Pinheiro Silva & Chales Pereira Silva
e-mail: adelino.pinheiro@policiacivil.mg.gov.br, adelinocpp@gmail.com
e-mail: charles.tni@gmail.com, charles.silva@policiacivil.mg.gov.br

Observação: A rotina ''P00_Anonimiza_Separa_Dados_Basicos_v0'' **serve de apoio para gerar as planilhas ''PUB_Ticket_Log_PCMG_NOREP_19_22.csv'' e ''PUB_Ticket_Log_PCMG_NOREP_BASE_19_22.csv'' que contém dados anonimizados**. Para a reprodução dos resultados não é necessário executá-la.

Sequência para reproduzir resultados:

* P01_Separa_Dados_Panilha_v0.py
* P02_Plota_Valores_por_Placa_v0.py
* P03_Analise_tempo_placa_grupo_v0.py
* P04_Modelo_previsao_Preco_v0.py


Como citar:
```
@Misc{Silva2024,
title={Repositório do Estudo com Gastos de Manutenção da Frota PCMG 2019-2022},
author={Adelino Pinheiro Silva & Chales Pereira Silva},
howPublished={\url{https://github.com/adelinocpp/Utility_Vehicle_PCMG_2019_2022}},
year={2024},
note={Version 1.0; Creative Commons BY-NC-SA 4.0.},
}
```