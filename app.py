#!/usr/bin/python3

# importar as bibliotecas necessárias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pydeck as pdk

#Tratamento dos dados
# importar os datasets COVID-19 para os respectivos DataFrames
gps = pd.read_csv('https://raw.githubusercontent.com/wcota/covid19br/master/gps_cities.csv')
covid_complete = pd.read_csv('https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-cities-time.csv')

#mudando o nome da coluna id para city
gps = gps.rename(columns={'id': 'city'})

#merge dos dataframes "df_total" e "gps"
df = covid_complete.merge(gps)

#recorte de dados do ultimo dia
lastday = max(df['date'])

df_lastday = df.loc[df['date'] == lastday]


#informar data dos dados
st.write("Dados atualizados até as 23:59h do dia {}".format(df['date'].max()))

#título
st.title("CENÁRIO DA COVID-19 NO BRASIL")


#descrição em texto
st.markdown(
    """
    Neste Dashboard Interativo é possível verificar o avanço do Corona Vírus no Brasil no decorrer do tempo.

    Casos e óbitos confirmados por dia, utilizando informação oficial pelo Ministério da Saúde, dados no nível municipal do [Brasil.IO](https://brasil.io/) e dados mais recentes reportados pela equipe do [@CoronavirusBra1](https://twitter.com/CoronavirusBra1).
    Acesso através do Repositório do Github do [Wesley Cota](https://github.com/wcota/covid19br).

    Código-fonte disponível no meu [Portfólio no Github](https://github.com/felipe-sanches/data_science)
    """
)


#slider semana epidemiológica
semana = df['epi_week'].values.tolist()

semana_epi = list(dict.fromkeys(semana))

selected_week = st.slider("Escolha a semana epidemiológica", semana_epi[0], semana_epi[-1], value=semana_epi[-1])


#slider data
datas_semana_epi = df.loc[df['epi_week'] == selected_week]

datas = datas_semana_epi['date'].values.tolist()

dataslist = list(dict.fromkeys(datas))

selected_date = st.selectbox("Escolha a data", dataslist)


#recorte do dataframe para a data selecionada
date_cut = df.loc[df['date'] == selected_date]


#mapa indicador de cidades infectadas
st.subheader("Mapa de Cidades Infectadas em {}".format(selected_date))
st.text("")
st.map(date_cut)


#grafico - cidades com maior numero de casos
ten_cities = date_cut.sort_values(['totalCases'], ascending=False).head(10)

fig, ax = plt.subplots(figsize=(15,10))

ten_cities.plot(x='city', y='totalCases', kind="barh", ax=ax)

ax.set_title("10 CIDADES COM OS MAIORES NÚMEROS DE CASOS CONFIRMADOS DE COVID-19\n\n")
ax.set_xlabel("Nº Casos")
ax.set_ylabel("Cidades")

for index, value in enumerate(ten_cities['totalCases']):
    plt.text(value, index, str(value))
    
st.pyplot()



#grafico cidades com maior numero de mortes
ten_deaths = date_cut.sort_values(['deaths'], ascending=False).head(10)

fig, ax = plt.subplots(figsize=(15,10))

ten_deaths.plot(x='city', y='deaths', kind="barh", ax=ax)

ax.set_title("10 CIDADES COM OS MAIORES NÚMEROS DE MORTES POR COVID-19\n\n")
ax.set_xlabel("Nº Casos")
ax.set_ylabel("Cidades")

for index, value in enumerate(ten_deaths['deaths']):
    plt.text(value, index, str(value))

st.pyplot()


#sidebar

#total de Casos
st.sidebar.warning("Total de Casos: {}".format(df_lastday['totalCases'].sum())) 

#total de Mortes
st.sidebar.error("Total de Mortes: {}".format(df_lastday['deaths'].sum()))


#adicionando selectbox na sidebar
checkbox = st.sidebar.checkbox("Exibir tabelas de dados no final da página")

if checkbox:
    st.write(df)

