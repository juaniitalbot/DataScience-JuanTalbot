# IMPORTAR LIBRERIAS
import pandas as pd
import numpy as np

# CREA FUNCION PARA GENERAR REGRESORES Y TERMINAR DE COMPLETAR DATA
def generaRegresores(data: pd.DataFrame) -> pd.DataFrame:
    """
    Genera los regresores.

    Args:
        data (pd.DataFrame): Dataframe con los datos de facturacion, stock y transfer

    Returns:
        pd.DataFrame: Dataframe completo y con los regresores a utilizar en el forecast.
    """
    # ordeno por dia
    data['fecha'] = pd.to_datetime(data['fecha'])

    # flag transfer
    data['f_transfer'] = (data['transfer'] > 0).astype(int)

    # calculo venta por dia
    data['vta_por_dia'] = data['cant_vta_cli'] / data['fecha'].dt.days_in_month
    data['vta_por_dia'] = data['vta_por_dia'].fillna(method='ffill')
    data['vta_por_dia'] = np.where(data['vta_por_dia'] < 0, 0, data['vta_por_dia'])

    data = data.fillna(0)
    
    if 'stk_por_dia' not in data.columns:
        data['stk_por_dia'] = 0
    
    
    for i in data.index:
        data['stk_por_dia'] = np.where(data['cant_stk_cli'] > 0, (data['cant_stk_cli'] + data['cant_fact']) - data['vta_por_dia'],  (data['stk_por_dia'].shift(1) + data['cant_fact']) - data['vta_por_dia'])
    
    data['stk_por_dia'] = np.where(data['stk_por_dia'] < 0, 0, data['stk_por_dia'])

    data['dias_de_stk'] = data['stk_por_dia'] / data['vta_por_dia'] # Calculo dias de stock
    data['dias_de_stk'] = data['dias_de_stk'].apply(lambda x: 0 if np.isinf(x) else x) # Reemplazo inf por 0
    data['dias_de_stk'] = np.where(data['dias_de_stk'] < 0, 0, data['dias_de_stk'])

    data = data.fillna(0)
    
    return data