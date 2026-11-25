#importamos las librerias a utilizar
import pandas as pd
import numpy as np
import sqlite3 as sql
import requests as req
from bs4 import BeautifulSoup as bs
from datetime import datetime

url = 'https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'
table_attri = ['Country','GDP_USD_millions']
db_name = 'World_Economies.db'
table_name = 'Countries_by_GDP'
csv_path = './Countries_by_GDP.csv'


#Esta función extrae la información requerida de la página web (webscraping)
#y la guarda en un df, que devuelve para su procesamiento 
def extract(url, table_attri):
  page = req.get(url).text
  data = bs(page,'html.parser')
  df = pd.DataFrame(columns=table_attri)
  #extraemos todos los atributos tbody del objeto html y luego todas las filas de la tabla en el indice 2 usando el atributo tr
  tables = data.find_all('tbody')
  rows = tables[2].find_all('tr')
  #Verificaos el contenido de cada fila teniendo el atributo td
  #Para cada fila, buscamos sus celdas td
  for row in rows:
    col = rows.find_all('td')  
    if len(col) != 0:
      if col[0].find('a') is not None and '-' not in col[2]:
        data_dict = {'Country':col[0].a.contents[0],
                     'GDP_USD_millions':col[2].contents[0]}
        df1 = pd.DataFrame(data_dict,index=[0])
        df = pd.concat([df,df1],ignore_index=True)
  return df


#Esta función convierte la información de GDP a un formato estandarizado
#Transforma la información de millones a billones de USD 
def transform(df):
  values = df['GDP_USD_millions'].to_list()
  billions = []
  for i in values:
    num = float(''.join(i.split(',')))
    billions.append(np.round(num/1000,2))
  df['GDP_USD_millions'] = billions
  df = df.rename(columns = {'GDP_USD_millions':'GDP_USD_billions'})
  return df

#Esta función guarda el df final en un archivo CSV
def load_to_csv(df,csv_path):
  df.to_csv(csv_path,index=False)
  
#Esta función guarda el df final en una tabla de la base de datos
def load_to_db(df, connection, table_name):
  df.to_sql(table_name,connection,if_exists='replace',index=False)
  
#Esta función corre la query en la tabla de la bd
def run_query(query_statement, connection):
  print(query_statement)
  query_output = pd.read_sql(query_statement,connection)
  print(query_output)

#Esta función registra el mensaje indicado en una etapa de la ejecución del código
#Y guarda el mensaje en un archivo de log con la fecha y hora de ejecución
def log_process(message):
  timestamp_format = '%Y-%h-%d-%H:%M:%S'
  now = datetime.now()
  timestamp = now.strftime(timestamp_format)
  with open('./etl_project_log.txt','a') as f:
    f.write(timestamp + ' : ' + message + '\n') 
