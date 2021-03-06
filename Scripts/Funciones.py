import pandas as pd  
import os
import numpy as np

#Funcion para quitar filas duplicadas
def eliminar_duplicados(df):
    '''
    Elimina filas duplicadas del df introducido

    Parameters
    ----------
    df : DataFrame.

    Returns
    -------
    El df introducido pero sin filas duplicadas
    '''
    df.drop_duplicates(ignore_index= True, inplace= True)


#Función para identificar columnas duplicadas
def columnas_duplicadas(df):

    '''
    Coge una variable cada vez y la compara con las demás.
    Si esta se repite la añade a la lista 'duplicates'. 

    Parameters
    ----------
    df : DataFrame.

    Returns
    -------
    Una lista llamada duplicates, donde aparece el nombre de las variables repetidas
    En caso de que no haya duplicados, esta estará vacía
    '''
    duplicates = []
    for col in range(df.shape[1]):
        contents = df.iloc[:, col]
        
    for comp in range(col + 1, df.shape[1]):
        if contents.equals(df.iloc[:, comp]):
            duplicates.append(comp)

    duplicates = np.unique(duplicates).tolist()
    print(duplicates)



#Funcion para cambiar el tipo 
def corregir_tipo(df, columnas, tipo):

    '''
    Elimina filas duplicadas del df introducido

    Parameters
    ----------
    df : DataFrame, columnas : columnas a corregir, tipo : tipo al que se quiere convertir la variable

    Returns
    -------
    Las columnas con el tipo corregido
    '''
    for col in columnas:
        df[col] = df[col].astype(tipo)


#Funcion para convertir en datetime
def convertir_datetime(df, cols):
    df[cols] = df[cols].apply(pd.to_datetime)



#Funcion visualizar missings
def view_nan(df):
    '''
    Devuelve el numero y el porcentaje de NA de cada variable

    Parameters
    ----------
    df : DataFrame.

    Returns
    -------
    Cuantos NA, NOT NA y el porcentaje de NA, por variable

    '''
    na = df.isna().sum()
    nona = df.notna().sum()
    pct = (na/len(df))*100
    total = list(zip(na, nona, pct))
    tabla = pd.DataFrame(total, index = df.columns)
    tabla.columns = ['NA', 'NOT_NA', 'pct']
    tabla['pct'] = tabla['pct'].astype(str) + ' %'
    tabla = tabla.sort_values(ascending=False, by='pct')
    return(tabla)




# Eliminar NA en dataframe
def Eliminar_na_por_df(df, pct_max_NA):
    '''
    Elimina columnas del df que superan el porcentaje maximo de NAs permitidos

    Parameters
    ----------
    df : DataFrame, pct_max_NA : Porcentaje maximo de NAs permitidos

    Returns
    -------
    Un df con las variables que contienen un porcentaje de NAs menor al pct_max_NA determinado

    '''
    for variable in df:
        if (((df[str(variable)].isna().sum())/df[str(variable)].shape[0])*100) >= pct_max_NA:
            df.drop(columns = [str(variable)], inplace = True)



