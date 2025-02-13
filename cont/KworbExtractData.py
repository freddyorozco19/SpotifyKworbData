import streamlit as st
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

st.header("KWORB EXTRACT DATA")
st.divider()

url = st.text_input("URL")

# Obtener el contenido de la página
respuesta = requests.get(url)
html = respuesta.text
# Crear el objeto BeautifulSoup
soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
# Listas para almacenar los datos
canciones = []
urls = []
streams_totales = []
streams_diarios = []
# Encontrar todas las filas (tr) de la tabla
filas = soup.find_all('tr')
# Recorrer cada fila y extraer la información
for fila in filas:
    # Encontrar todas las celdas (td) en la fila
    celdas = fila.find_all('td')
    
    # Si la fila tiene celdas, procesarla
    if celdas:
        # Para el título de la canción (está dentro de un enlace)
        titulo = celdas[0].find('a')
        if titulo:
            canciones.append(titulo.text)
            urls.append(titulo['href'])
            streams_totales.append(celdas[1].text.replace(",", ""))
            streams_diarios.append(celdas[2].text.replace(",", ""))
            


# Crear el DataFrame
df = pd.DataFrame({
    'Canción': canciones,
    'URL': urls,
    'Streams totales': streams_totales,
    'Streams diarios': streams_diarios
})

df['Streams totales'] = df['Streams totales'].astype(int)
df['Streams diarios'] = df['Streams diarios'].replace('', 0)
df['Streams diarios'] = df['Streams diarios'].astype(int)


st.dataframe(df)
#st.metric("Date")
st.divider()
