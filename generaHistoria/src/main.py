#%%
# IMPORTAR LIBRERIAS
import pandas as pd
import datetime
from os.path import abspath, dirname
import sys
import os
ruta_base = dirname(dirname(abspath(__file__)))
os.chdir(ruta_base)
sys.path.append(ruta_base)

from funciones.generaData import generaData
from funciones.completaFechas import completaFechas
from funciones.generaRegresores import generaRegresores


#%%
# SCRIPT QUE EJECUTA TODAS LAS FUNCIONES PARA LLEGAR AL PRONOSTICO POR CLIENTE Y ARTICULO
# Cargar datos queries

facturacion = pd.read_excel('D:/Bizmetriks/GlobalFarm/generaHistoria/Datos/facturacion.xlsx', index_col=0)
stock = pd.read_excel('D:/Bizmetriks/GlobalFarm/generaHistoria/Datos/stock.xlsx', index_col=0)
transfer = pd.read_excel('D:/Bizmetriks/GlobalFarm/generaHistoria/Datos/transfer.xlsx', index_col=0)

#%%
# Ejecuta la funcion generaData
print('Inicio de generar data ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
data = generaData(facturacion, stock, transfer)
print('Data generada exitosamente ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

#%%
data = data.query("cod_tit in (10954, 10919, 20303)")

# %%
# Ejecuta la funcion completaFechas
print('Inicio de completar fechas ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

fecha_final = data.fecha.max() # max fecha articulo

data['fecha'] = pd.to_datetime(data['fecha'])

data = data.groupby(['cod_tit', 'cod_articulo']).apply(completaFechas, fecha_final=fecha_final).reset_index(drop=True)

data = data[data['fecha'] >= '2021-06-28'].reset_index(drop=True)
data = data[data['fecha'] <= '2023-08-27'].reset_index(drop=True)

print('Fechas completadas exitosamente ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

#%%
# Ejecuta la funcion generaRegresores
print('Inicio genera regresores ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
data = data.groupby(['cod_tit', 'cod_articulo']).apply(generaRegresores).reset_index(drop=True)
print('Regresores generados ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
# %%

data.to_csv('dataHistoria1.csv')

# %%
