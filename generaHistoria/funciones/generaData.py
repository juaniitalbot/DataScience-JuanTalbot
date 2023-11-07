# IMPORTAR LIBRERIAS
import pandas as pd

# CREA FUNCION PARA UNIR LOS DATAFRAMES (facturacion, stock y transfer)
def generaData(facturacion: pd.DataFrame, stock: pd.DataFrame, transfer: pd.DataFrame) -> pd.DataFrame:
    """
    Procesamiento de los datos de la query y creacion del dataframe final data.

    Args:
        facturacion (pd.DataFrame): Dataframe con los datos de facturacion
        stock (pd.DataFrame): Dataframe con los datos de stock del cliente
        transfer (pd.DataFrame): Dataframe con los datos de los transfer
    Returns:
        pd.DataFrame: Dataframe final con solo las columnas necesarias
    """

    # Selecciona las columnas específicas en los DataFrames
    transfer = transfer[['fecha_nc', 'cod_tit', 'cod_articulo', 'cant_tot_desp']]
    facturacion = facturacion[['fec_doc', 'cod_tit', 'cod_articulo', 'cant_bruta']]
    stock = stock[['fec_doc', 'cod_tit', 'cod_articulo', 'cant_stk_cli', 'cant_vta_cli']]

    print('Filtrado de columnas listo')

    # filtrar facturacion negativa
    facturacion = facturacion[facturacion['cant_bruta'] > 0]

    # convertir a datetime y ordenar por fecha
    facturacion['fec_doc'] = pd.to_datetime(facturacion['fec_doc'])
    facturacion = facturacion.sort_values(by=['fec_doc'])

    stock['fec_doc'] = pd.to_datetime(stock['fec_doc'])
    stock = stock.sort_values(by=['fec_doc'])

    transfer['fecha_nc'] = pd.to_datetime(transfer['fecha_nc'])
    transfer = transfer.sort_values(by=['fecha_nc'])

    # filtrar por fecha < 2100-12-31 que significa que el transfer no se despacho
    transfer = transfer[transfer['fecha_nc'] < '2100-12-31']
    print('Ordenar por fechas listo')

    # cambiar nombre de columnas para mejor entendimiento
    facturacion = facturacion.rename(columns={'cant_bruta': 'cant_fact'})
    transfer = transfer.rename(columns={'cant_tot_desp': 'transfer'})

    # agrupar dataframes por fecha, cliente y articulo
    transfer = transfer.groupby(['fecha_nc', 'cod_tit', 'cod_articulo']).agg({'transfer': 'sum'}).reset_index()
    facturacion = facturacion.groupby(['fec_doc', 'cod_tit', 'cod_articulo']).agg({'cant_fact': 'sum'}).reset_index()
    stock = stock.groupby(['fec_doc', 'cod_tit', 'cod_articulo']).agg({'cant_stk_cli': 'sum', 'cant_vta_cli': 'sum'}).reset_index()
    print('Agrupacion de transfer y facturacion por fecha listo')

    # unir los dataframes
    data = facturacion.merge(transfer, left_on=['fec_doc', 'cod_tit', 'cod_articulo'], right_on=['fecha_nc', 'cod_tit', 'cod_articulo'], how='outer') # merge que trae todos los datos de ambos dataframes
    data['fecha'] = data['fec_doc'].fillna(data['fecha_nc']) # crea una nueva columna fecha con ambas fechas de los dataframes
    data = data.sort_values(by='fecha')
    print('Primer merge listo')

    data = data.drop(columns=['fec_doc'])

    data = data.merge(stock, left_on=['fecha', 'cod_tit', 'cod_articulo'], right_on=['fec_doc', 'cod_tit', 'cod_articulo'], how='outer') # merge que trae todos los datos de ambos dataframes
    data['fecha'] = data['fecha'].fillna(data['fec_doc'])  # rellena la nueva columna fecha con la fechas de stock

    data = data.drop(columns=['fec_doc'])
    data = data.drop(columns=['fecha_nc'])

    data = data.sort_values(by='fecha')
    print('Segundo merge listo')

    return data

