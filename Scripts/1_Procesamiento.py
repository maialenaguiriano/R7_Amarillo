#!/usr/bin/env python
# coding: utf-8

# __LIBRERIAS__

# In[18]:


import pandas as pd
import numpy as np
import os
import seaborn as sns
import datetime as dt
import matplotlib.pyplot as plt


# __CARGA DE DATOS__

# In[19]:


encoding='cp1252'


# In[20]:


os.getcwd()
path = '..\\datosOriginales\\' #ruta donde se encuentran los datos
path1 = '..\\datosTransformados\\' # ruta donde se van a guardar los datos limpios
df = pd.read_csv(path+'datos_sabi.csv', encoding = "ISO-8859-1", index_col=[0])


# __IMPORTAR MODULOS CREADOS POR NOSOTROS__

# In[21]:


import Funciones as fn #Funciones es el nombre del script dnd hemos creado las funciones


# __DATA DISCOVERING__

# In[22]:


df.head(2)


# In[23]:


df.shape #dimensiones (207144, 85)


# In[24]:


df.columns


# In[25]:


df.info()


# Estadisticos

# In[26]:


df.describe() #con las variables continuas


# In[27]:


#Con las variables discretas
df['localidad'].value_counts().to_frame() 
df['estado_detallado'].value_counts().to_frame() #las tildes se ven mal, cambiar el encoding
df['estado'].value_counts().to_frame() 
df['fase_actual'].value_counts().to_frame()  #las tildes se ven mal, cambiar el encoding
df['tipo'].value_counts().to_frame() #solo hay un tipo, lo demas son NA
df['sector'].value_counts().to_frame() 


# __DATA CLEANING__

# Correccion del tipo:

# In[28]:


df['ultimo_ano_disponible'].value_counts()


# In[29]:


fn.corregir_tipo(df= df, columnas= ['nombre','codigo_nif', 'localidad',  'sector'], tipo= 'string') #las pasamos a tipo string. 
#Algunas no nos deja cambiarlas porque tienen NAN: estado_detallado, fase_actual, 'codigo_primario_cnae_2009'
fn.convertir_datetime(df, ['fecha_cambio_estado','ultimo_ano_disponible','fecha_constitucion', 'fecha_fase_actual'])


# Corregimos columna anyo

# In[30]:


df[df['anyo'] == 'ult_ano_disp'][['anyo']] # hay filas con valor ult_ano_disp. Lo tenemos que sustituir con el ultimo año disponible de esa empresa
                                           # que aparece en la variable ultimo_ano_disponible.


# In[31]:


df['ultimo_ano_disponible'] = df['ultimo_ano_disponible'].dt.year # nos quedamos solo con el año
df['ultimo_ano_disponible']


# In[32]:


df['anyo'] = np.where(df['anyo'] == 'ult_ano_disp', df['ultimo_ano_disponible'], df['anyo']) # remplazamos los valores ult_ano_disp
df['anyo']


# In[38]:


df[df['anyo']== 'ult_ano_disp']#correcto
df.anyo


# In[37]:


df['anyo'] = pd.to_datetime(df['anyo']).dt.year
df['anyo']


# In[35]:


df['ultimo_ano_disponible'] = pd.to_datetime(df['ultimo_ano_disponible'], format='%Y').dt.year
df['ultimo_ano_disponible']


# In[36]:


df = df[df['anyo'] <= df['ultimo_ano_disponible']] # eliminamos los datos de los años superiores al ultimo año disponible, ya que, como es logico, no tienen informacion


# In[ ]:


df4 = df[df['nif']== 'A48165468']
df4.anyo


# In[ ]:


df.anyo


# Duplicados

# In[ ]:


#Quitamos filas duplicadas

#fn.eliminar_duplicados(df)


# In[ ]:


df.shape


# In[ ]:


#identificamos columnas duplicadas
fn.columnas_duplicadas(df) # no hay ninguna


# Missings

# In[ ]:


missings = fn.view_nan(df)
missings


# In[ ]:


#objetos
fig, ax = plt.subplots()

#Grafico
sns.heatmap(df.isnull(), cbar=False) #visualizamos los missings

#formato figura
fig.set_size_inches(15,5)
fig.set_dpi(130) 

# Vemos que muchas variables tienen muchos valores ausentes, algunas, como son datos del balance de las empresas, no las vamos a eliminar. En cambio, 
# la variable "tipo" solo contiene 19 valores completos, que pone "abreviado". Las eliminamos ya que no aporta valor. 


# In[ ]:


df[df.total_activo_mil_eur.isna()] # nos damos cuenta de que en las filas que hay NAN en 'total_activo_mil_eur' hay NAN en todas las variables que pertenecen al balance
# estas instancias no aportan valor, ya que no tienen informacion


# In[ ]:


missings_variables = fn.view_nan(df[df.total_activo_mil_eur.isna()])
missings_variables.iloc[9:,:] # 100% de missings


# In[ ]:


#df.drop(df[df.total_activo_mil_eur.isnull()].index, inplace = True) # eliminamos esas filas con todo NAN


# In[ ]:


#quitar la variable tipo ya que tiene un 99.98% de valores NA
df.drop(columns='tipo', inplace=True)


# In[ ]:


missings1 =fn.view_nan(df)
missings1 # hay tres variables con 100% de valores vacios, las eliminamos


# In[ ]:


df.drop(columns= ['consumo_de_mercaderias_y_de_materias_mil_eur', 'otros_gastos_de_explotacion_mil_eur', 'resultado_bruto_mil_eur'], inplace=True)


# In[ ]:


missings2 = fn.view_nan(df)
missings2


# In[ ]:


df["fase_actual"].value_counts()


# In[ ]:


# Hay palabras en "fase actual" que contienen un caracter extraño: "<d3>". Lo sustituimos por la letra O, que es la que le pertenece.
df['fase_actual'].value_counts().to_frame()
# Además quitamos todas las tildes por seacaso
diccionario  = {'Ó':'O',"À":"A",'É':'E', 'Í':'I', 'Ú':'U', '<d3>':'O','/':': '}
for key, value in diccionario.items():
    df['fase_actual'] = df['fase_actual'].str.replace(key, value)


# In[ ]:


df['fase_actual'].fillna('SIN INFORMACION', inplace=True) # cambiamos los valores vacios por "SIN INFORMACION"
df["fase_actual"].value_counts() #correcto


# In[ ]:


missings3 = fn.view_nan(df)
missings3


# In[ ]:


# las variables con un porcentaje muy elevado de missings no van a poder usarse para predecir, por lo que creamos un nuevo df sin ellas. 


# In[ ]:


df.shape


# In[ ]:


df.shape # se han eliminado 5 columnas


# Outliers

# In[ ]:


sns.boxplot(x=df['inmovilizado_inmaterial_mil_eur'])

from scipy import statsmean = np.mean(df['numero_empleados'])
std = np.std(df['numero_empleados'])
print('mean of the dataset is', mean)
print('std. deviation is', std)threshold = 3
outlier = []
for i in df['numero_empleados']:
    z = (i-mean)/std
    if z > threshold:
        outlier.append(i)
print('outlier in dataset is', outlier)
# In[ ]:


sns.boxplot(x=df['numero_empleados'])


# In[ ]:


fig, ax = plt.subplots()

#Grafico
sns.heatmap(df.isnull(), cbar=False) #visualizamos los missings

#formato figura
fig.set_size_inches(15,5)
fig.set_dpi(130) 


# In[ ]:


missings_antes = fn.view_nan(df)
missings_antes


# In[ ]:


index = df[(df.ingresos_de_explotacion_mil_eur.isna() == True) & (df.ingresos_de_explotacion_por_empleado_mil.isna() == False) & (df.numero_empleados.isna() == False)].index

for i in index:
    df.loc[i,'ingresos_de_explotacion_mil_eur'] = df.loc[i, 'ingresos_de_explotacion_por_empleado_mil'] * df.loc[i, 'numero_empleados']


# In[ ]:


index = df[(df.ingresos_de_explotacion_mil_eur.isna() == False) & (df.resultado_explotacion_mil_eur.isna() == False)].index

for i in index:
    df.loc[i,'gastos_de_explotacion'] = -1 * df.loc[i, 'resultado_explotacion_mil_eur'] - df.loc[i, 'ingresos_de_explotacion_mil_eur']


# In[ ]:


index = df[(df.result_ordinarios_antes_impuestos_mil_eur.isna() == False) & (df.resultado_actividades_ordinarias_mil_eur.isna() == False)].index

for i in index:
    df.loc[i,'impuestos_sobre_sociedades_mil_eur'] = df.loc[i, 'result_ordinarios_antes_impuestos_mil_eur'] - df.loc[i, 'resultado_actividades_ordinarias_mil_eur']


# In[ ]:


index = df[(df.resultado_explotacion_mil_eur.isna() == False) & (df.resultado_financiero_mil_eur.isna() == False)].index

for i in index:
    df.loc[i,'result_ordinarios_antes_impuestos_mil_eur'] = df.loc[i, 'resultado_explotacion_mil_eur'] + df.loc[i, 'resultado_financiero_mil_eur']


# In[ ]:


index = df[(df.resultado_del_ejercicio_mil_eur.isna() == False) & (df.resultados_actividades_extraordinarias_mil_eur.isna() == False)].index

for i in index:
    df.loc[i,'resultado_actividades_ordinarias_mil_eur'] = df.loc[i, 'resultado_del_ejercicio_mil_eur'] - df.loc[i, 'resultados_actividades_extraordinarias_mil_eur']


# In[ ]:


index = df[(df.resultado_del_ejercicio_mil_eur.isna() == False) & (df.resultado_actividades_ordinarias_mil_eur.isna() == False)].index

for i in index:
    df.loc[i,'resultados_actividades_extraordinarias_mil_eur'] = df.loc[i, 'resultado_del_ejercicio_mil_eur'] - df.loc[i, 'resultado_actividades_ordinarias_mil_eur']


# In[ ]:


missings_mientras = fn.view_nan(df)
missings_mientras


# Se añade lo del balance

# In[ ]:


index = df[(df.activo_circulante_mil_eur.isna() == False) & (df.total_activo_mil_eur.isna() == False)].index

for i in index:
    df.loc[i,'inmovilizado_mil_eur'] = df.loc[i, 'total_activo_mil_eur'] - df.loc[i, 'activo_circulante_mil_eur']


# In[ ]:


index = df[(df.inmovilizado_mil_eur.isna() == False) & (df.inmovilizado_material_mil_eur.isna() == False) & (df.otros_activos_fijos_mil_eur.isna() == False)].index

for i in index:
    df.loc[i,'inmovilizado_inmaterial_mil_eur'] = df.loc[i, 'inmovilizado_mil_eur'] - (df.loc[i, 'inmovilizado_material_mil_eur'] + df.loc[i, 'otros_activos_fijos_mil_eur'])


# In[ ]:


index = df[(df.inmovilizado_mil_eur.isna() == False) & (df.otros_activos_fijos_mil_eur.isna() == False) & (df.inmovilizado_inmaterial_mil_eur.isna() == False)].index

for i in index:
    df.loc[i,'inmovilizado_material_mil_eur'] = df.loc[i, 'inmovilizado_mil_eur'] - (df.loc[i, 'otros_activos_fijos_mil_eur'] + df.loc[i, 'inmovilizado_inmaterial_mil_eur'])


# In[ ]:


index = df[(df.activo_circulante_mil_eur.isna() == False) & (df.total_activo_mil_eur.isna() == False)].index

for i in index:
    df.loc[i,'activos_no_corriente'] = df.loc[i, 'total_activo_mil_eur'] - df.loc[i, 'activo_circulante_mil_eur']


# In[ ]:


index = df[(df.existencias_mil_eur.isna() == True) & (df.activo_circulante_mil_eur.isna() == False) & (df.deudores_mil_eur.isna() == False) & (df.otros_activos_liquidos_mil_eur.isna() == False)].index

for i in index:
    df.loc[i,'existencias_mil_eur'] = df.loc[i, 'activo_circulante_mil_eur'] - (df.loc[i, 'deudores_mil_eur'] + df.loc[i, 'otros_activos_liquidos_mil_eur'])


# In[ ]:


index = df[(df.fondos_propios_mil_eur.isna() == False) & (df.total_pasivo_y_capital_propio_mil_eur.isna() == False)].index

for i in index:
    df.loc[i,'total_pasivo'] = df.loc[i, 'total_pasivo_y_capital_propio_mil_eur'] - df.loc[i, 'fondos_propios_mil_eur']


# In[ ]:


index = df[(df.total_pasivo.isna() == False) & (df.pasivo_liquido_mil_eur.isna() == False)].index

for i in index:
    df.loc[i,'pasivo_fijo_mil_eur'] = df.loc[i, 'total_pasivo'] - df.loc[i, 'pasivo_liquido_mil_eur']


# In[ ]:


index = df[(df.pasivo_fijo_mil_eur.isna() == False) & (df.otros_pasivos_fijos_mil_eur.isna() == False)].index

for i in index:
    df.loc[i,'acreedores_a_l_p_mil_eur'] = df.loc[i, 'pasivo_fijo_mil_eur'] - df.loc[i, 'otros_pasivos_fijos_mil_eur']


# In[ ]:


index = df[(df.capital_suscrito_mil_eur.isna() == False) & (df.otros_fondos_propios_mil_eur.isna() == False)].index

for i in index:
    df.loc[i,'fondos_propios_mil_eur'] = df.loc[i, 'capital_suscrito_mil_eur'] + df.loc[i, 'otros_fondos_propios_mil_eur']


# In[ ]:


missings_despues = fn.view_nan(df)
missings_despues


# In[ ]:


#objetos
fig, ax = plt.subplots()

#Grafico
sns.heatmap(df.isnull(), cbar=False) #visualizamos los missings

#formato figura
fig.set_size_inches(15,5)
fig.set_dpi(130) 


# In[ ]:


#RATIOS


# In[ ]:


index = df[(df.activo_circulante_mil_eur.isna() == False) & (df.pasivo_liquido_mil_eur.isna() == False)].index

for i in index:
    df.loc[i,'ratio_liquidez'] = df.loc[i, 'activo_circulante_mil_eur'] / df.loc[i, 'pasivo_liquido_mil_eur']


# In[ ]:


df = df.rename(columns = {'ratio_de_liquidez_percent': 'ratio_tesoreria'})


# In[ ]:


index = df[(df.total_activo_mil_eur.isna() == False) & (df.total_pasivo.isna() == False)].index

for i in index:
    df.loc[i,'ratio_de_solvencia_percent'] = df.loc[i, 'total_activo_mil_eur'] / df.loc[i, 'total_pasivo']


# In[ ]:


index = df[(df.activo_circulante_mil_eur.isna() == False) & (df.pasivo_liquido_mil_eur.isna() == False)].index

for i in index:
    df.loc[i,'fondo_de_maniobra_mil_eur'] = df.loc[i, 'activo_circulante_mil_eur'] - df.loc[i, 'pasivo_liquido_mil_eur']


# In[ ]:


index = df[(df.resultado_del_ejercicio_mil_eur.isna() == False) & (df.fondos_propios_mil_eur.isna() == False)].index

for i in index:
    df.loc[i,'ROE'] = df.loc[i, 'resultado_del_ejercicio_mil_eur'] / df.loc[i, 'fondos_propios_mil_eur']


# In[ ]:


index = df[(df.resultado_del_ejercicio_mil_eur.isna() == False) & (df.total_activo_mil_eur.isna() == False)].index

for i in index:
    df.loc[i,'ROA'] = df.loc[i, 'resultado_del_ejercicio_mil_eur'] / df.loc[i, 'total_activo_mil_eur']


# In[ ]:


index = df[(df.total_pasivo.isna() == False) & (df.otros_activos_liquidos_mil_eur.isna() == False) & (df.deudores_mil_eur.isna() == False)].index

for i in index:
    df.loc[i,'deuda_neta'] = df.loc[i, 'total_pasivo'] - (df.loc[i, 'otros_activos_liquidos_mil_eur'] + df.loc[i, 'deudores_mil_eur'])


# In[ ]:


index = df[(df.deuda_neta.isna() == False) & (df.ebitda_mil_eur.isna() == False)].index

for i in index:
    df.loc[i,'net_debt/ebitda'] = df.loc[i, 'deuda_neta'] / df.loc[i, 'ebitda_mil_eur']


# In[ ]:


index = df[(df.total_pasivo.isna() == False) & (df.fondos_propios_mil_eur.isna() == False)].index

for i in index:
    df.loc[i,'ratio_endeudamiento'] = df.loc[i, 'total_pasivo'] / df.loc[i, 'fondos_propios_mil_eur']


# In[ ]:


missings_ratios = fn.view_nan(df)
missings_ratios


# In[ ]:


fn.Eliminar_na_por_df(df, pct_max_NA=87) #DECIDIR QUE PORCENTAJE


# In[ ]:


#objetos
fig, ax = plt.subplots()

#Grafico
sns.heatmap(df.isnull(), cbar=False) #visualizamos los missings

#formato figura
fig.set_size_inches(15,5)
fig.set_dpi(130) 


# In[ ]:


#df.to_csv('datos_limpios.csv')


# Importamos el nuevo excel de empresas que han entrado en concurso 

# In[ ]:


# necesitamos saber que empresas han entrado en concurso o son deudoras, a traves de la tabla de concurso. 
# Si aparecen en esta segunda tabla en la columna deudor, significa que son deudoras
concurso = pd.read_csv(path+'publicidad_concursal.csv', encoding = "ISO-8859-1")


# In[ ]:


# Juntamos las dos tablas
df = df.rename(columns={'codigo_nif': 'nif'})
df_total = pd.merge(df, concurso, on="nif",how='inner')


# In[ ]:


df_total[['nombre','deudor','nif']]


# In[ ]:


# intentamos poner los nombres de las empresas de las dos tablas originales con el mismo nombre:
# Quitar signos de puntuacion
df_total["nombre"] = df_total['nombre'].str.replace('[^\w\s]','')
df_total["deudor"] = df_total['deudor'].str.replace('[^\w\s]','')

# Pasar a mayusculas
df_total["nombre"] = df_total['nombre'].str.upper()
df_total["deudor"] = df_total['deudor'].str.upper()

# Cambiar SL
df_total["nombre"] = df_total['nombre'].str.replace('SOCIEDAD LIMITADA','SL')
df_total["deudor"] = df_total['deudor'].str.replace('SOCIEDAD LIMITADA','SL')

# Cambiar SA
df_total["nombre"] = df_total['nombre'].str.replace('SOCIEDAD ANONIMA','SA')
df_total["deudor"] = df_total['deudor'].str.replace('SOCIEDAD ANONIMA','SA')

# Cambiar Extinguida | Liquidacion
df_total["nombre"] = df_total['nombre'].str.replace('EXTINGUIDA','')
df_total["deudor"] = df_total['deudor'].str.replace('EXTINGUIDA','')
df_total["nombre"] = df_total['nombre'].str.replace('EN LIQUIDACION','')
df_total["deudor"] = df_total['deudor'].str.replace('EN LIQUIDACION','')


# In[ ]:


pip install fuzzywuzzy


# In[ ]:


# obtenemos la similitud de los nombres que toma la empresa en las dos tablas originales (ahora están juntas)

from fuzzywuzzy import fuzz
def get_similarity(term1, term2):

    print(fuzz.ratio(term1, term2))

    return fuzz.ratio(term1, term2)

nombres = df_total[['nombre','deudor','nif']]
nombres['similarity'] = nombres.apply(lambda x: get_similarity(x['deudor'], x['nombre']), axis = 1)

plt.hist(nombres.similarity, density=True, bins=30)  # density=False would make counts
plt.ylabel('Probability')
plt.xlabel('Data');


# In[ ]:


# Los nombres de las empresas en la columna nombre que tienen una similitud mayor a 60 con el nombre en 'deudor', las calificamos como deudoras
# ya que los dos nombres hacen referencia a la misma empresa pero con un nombre algo diferente.

nif_quiebra = nombres[nombres.similarity > 60].nif
nif_estado = df_total[(df_total.estado == 'Concurso') | (df_total.estado == 'Quiebra')].nif
nif_quiebra = nif_quiebra.append(nif_estado)

# Ademas, observamos las variables estado_detallado y fase_actual por si contienen alguna palabra que describen el estado de quiebra de las empresas
# Quitar signos de puntuacion
df_total["estado_detallado"] = df_total["estado_detallado"].str.replace('[^\w\s]','')

# Pasar a mayusculas
df_total["estado_detallado"] = df_total["estado_detallado"].str.upper()
df_total["fase_actual"] = df_total["fase_actual"].str.upper()
nif_detallado = df_total[df_total.estado_detallado.str.contains('CONCURSO | CONCURSAL | QUIEBRA', na=False)].nif
nif_faseactual = df_total[df_total.fase_actual.str.contains('CONCURSO | CONCURSAL | QUIEBRA', na=False)].nif
nif_quiebra = nif_quiebra.append(nif_detallado)
nif_quiebra = nif_quiebra.append(nif_faseactual)


# In[ ]:


# asignamos un 1 a la empresa si ha acabado en quiebra
dict = dict.fromkeys(nif_quiebra, 1)
df['quiebra'] = df['nif'].map(dict)
df.quiebra.fillna(0, inplace=True)


# In[ ]:


plt.hist(df.quiebra)  # density=False would make counts
plt.ylabel('Nº de instancias')
plt.xlabel('Quiebra (Y|N)');


# In[ ]:


df['quiebra'] = df['quiebra'].astype('bool')


# In[ ]:


#df.to_csv('datos_limpios2.csv')

