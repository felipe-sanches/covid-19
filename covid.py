#!/usr/bin/python3
#teste

# importar as bibliotecas necessárias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pydeck as pdk


# importar os datasets COVID-19 para os respectivos DataaFrames
cities = pd.read_csv('https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-cities.csv')
gps = pd.read_csv('https://raw.githubusercontent.com/wcota/covid19br/master/gps_cities.csv')
df_total = pd.read_csv('https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-total.csv')


#mudando o nome da coluna id para city
gps = gps.rename(columns={'id': 'city'})

#merge dos dataframes "cities" e "gps"
df = cities.merge(gps)
df.head()



#data dos dados
st.write("Dados atualizados em {}".format(df['date'].max()))


#título
st.title("CENÁRIO DA COVID-19 NO BRASIL HOJE")

#total de Casos
st.info("Total de Casos: \n   {}".format(df['totalCases'].sum())) 

#total de Mortes
st.info("Total de Mortes: \n     {}".format(df['deaths'].sum()))


#descrição
st.markdown(
    """
    Transmitido principalmente por meio de gotículas provenientes de tosses ou espirros de pessoas infectadas, a gravidade dos sintomas varia muito de pessoa para pessoa. 
    Fato é, não se sabe muita coisa a respeito do COVID-19. 
    
    Estudos estão sendo realizados no mundo todo, porém os resultados ainda não são conclusivos e definitivos.
    
    Até o presente momento, observa-se que cerca de 80% dos casos confirmados são assintomáticos e rápidos. A maioria das pessoas que se encaixam nesse grupo, se recupera sem nenhuma sequela.
    No entanto, 15% das pessoas terão infecções graves e precisarão de oxigênio. O restante das pessoas, que representam 5%, serão classificadas como infecções muito graves e precisarão de ventilação assistida, por meio de respiradores mecânicos em ambiente hospitalar.
    Com o objetivo de elevar a consciência situacional a respeito do COVID-19 no Brasil, irei realizar uma análise sobre os dados públicos da doença.
    """
)

#mapa
st.subheader("Mapa Indicador")
st.text("")
st.map(df)


#sidebar


# Add a slider to the sidebar:
#qnt_cases = st.sidebar.slider('Nº de casos', 0, 2000000)






#grafico - cidades com maior numero de casos
df.sort_values(['totalCases'], ascending=False)

ten_cities = df.sort_values(['totalCases'], ascending=False).head(10)

fig, ax = plt.subplots(figsize=(15,8))

ten_cities.plot(x='city', y='totalCases', kind="barh", ax=ax)

ax.set_title("10 CIDADES COM OS MAIORES NÚMEROS DE CASOS CONFIRMADOS DE COVID-19\n\n")
ax.set_xlabel("Nº Casos")
ax.set_ylabel("Cidades")

for index, value in enumerate(ten_cities['totalCases']):
    plt.text(value, index, str(value))
    
st.pyplot()



#grafico cidades com maior numero de mortes
df.sort_values(['deaths'], ascending=False)

ten_deaths = df.sort_values(['deaths'], ascending=False).head(10)

fig, ax = plt.subplots(figsize=(15,7))

ten_deaths.plot(x='city', y='deaths', kind="barh", ax=ax)

ax.set_title("10 CIDADES COM OS MAIORES NÚMEROS DE MORTES POR COVID-19\n\n")
ax.set_xlabel("Nº Casos")
ax.set_ylabel("Cidades")

for index, value in enumerate(ten_deaths['deaths']):
    plt.text(value, index, str(value))

st.pyplot()


#adicionando checkbox na sidebar
selectbox = st.sidebar.selectbox("Exibir tabelas de dados", ('Escolha um dataframe','Cities', 'Gps', 'Total'))
selected=None

if selectbox == 'Cities':
    selected = cities
elif selectbox == 'Gps':
    selected = gps
elif   selectbox == 'Total':
    selected = df_total

st.write(selected)
st.sidebar.info("Dataframe exibido no final da página")
