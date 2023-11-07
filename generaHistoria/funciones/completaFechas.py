# IMPORTAR LIBRERIAS
import pandas as pd
from datetime import datetime
# CREA FUNCION PARA COMPLEAR LAS FECHAS FALTANTES
def completaFechas(data: pd.DataFrame, fecha_final) -> pd.DataFrame:
    """
    Rellena las fechas faltantes en el dataframe data.

    Args:
        data (pd.DataFrame): Dataframe con los datos de facturacion, stock y transfer

    Returns:
        pd.DataFrame: Dataframe con las fechas faltantes rellenadas
    """

    # guardar en variables el 'cod_tit' y 'cod_articulo'
    cod_tit = data['cod_tit'].iloc[0]
    cod_articulo = data['cod_articulo'].iloc[0]

    # fecha inicio de cada articulo y fecha final general
    fecha_inicio = data.fecha.min()

    fecha_final = pd.to_datetime(fecha_final)

    # crea un dataframe con todas las fechas desde la fecha minima hasta la fecha maxima
    calendar = pd.DataFrame({'fecha': pd.date_range(fecha_inicio, fecha_final, freq="D")})

    # une el dataframe calendar con el dataframe data
    data = calendar.merge(data, on='fecha', how='left')

    data = data.sort_values(by='fecha')

    # completa nulos en las columnas 'cod_tit', 'sucursal' y 'cod_articulo'
    data['cod_tit'] = data['cod_tit'].fillna(cod_tit)
    data['cod_articulo'] = data['cod_articulo'].fillna(cod_articulo)

    return data