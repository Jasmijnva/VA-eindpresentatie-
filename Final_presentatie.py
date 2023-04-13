#!/usr/bin/env python
# coding: utf-8

# In[11]:

import requests

import pandas as pd

import folium

import streamlit as st

from streamlit_folium import st_folium

import folium.plugins

from PIL import Image

import calendar

import time

from datetime import datetime as dt

from datetime import date

import plotly.express as px

import plotly.figure_factory as ff

import seaborn as sns

from statsmodels.formula.api import ols

from matplotlib import style

import matplotlib.pyplot as plt

from sklearn import metrics

from sklearn import model_selection

from sklearn.linear_model import LogisticRegression

from sklearn.model_selection import train_test_split

from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LinearRegression

from sklearn import metrics

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import numpy as np

import urllib.request

import plotly.express as px


#import datasets
solar = pd.read_csv('SolarSystemAndEarthquakes.csv')
df = pd.read_csv('earthquake_data.csv')


#display alle kolommen en rijen 
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

#verander data naar datetime
df['Date'] = pd.to_datetime(df['date_time']).dt.date
df['Time'] = pd.to_datetime(df['date_time']).dt.time


df['date_time'] =  pd.to_datetime(df['date_time'], format='%d%m%Y%I%M', errors = 'ignore')


df['year'] = pd.DatetimeIndex(df['Date']).year
df['month'] = pd.DatetimeIndex(df['Date']).month


#laat kolommen vallen en hernoem kolommen 
df = df.drop(['date_time', 'Date', 'title'], axis=1)
df = df.rename(columns = {'cdi':'reported intensity', 'mmi':'estimated intensity'})
df['difference rep vs. est'] = df['reported intensity'] - df['estimated intensity']
df['tsunami'] = df['tsunami'].replace({1: True, 0: False})


df.groupby('year')['tsunami'].sum()
#hoe kan het dat er van 2001 tot en met 2012 geen tsunami's waren? foutieve data? 
#eventueel nog een plot van maken met visualisatie 

df_mag=df['magnitude'].value_counts().reset_index()
df_mag=df_mag.rename(columns={"index": "Magnitude", "magnitude": "Count"})


#figuur overzicht aantal magnitudes
fig1 = px.bar(df_mag, x="Magnitude", y='Count', title="Aantal aardbevingen per magnitude", labels={"Count": "Aantal"
                 })
fig1.update_layout(xaxis = dict(dtick = 0.1))
fig1.show()


#pie chart van procent aardbevingen met of zonder tsunami
tsunami_pie=df['tsunami'].value_counts().reset_index()
tsunami_pie= tsunami_pie.rename(columns = {'index':'Tsunami', 'tsunami':'Counts'})
fig2= px.pie(tsunami_pie, values='Counts', names='Tsunami', title='Percentage aardbevingen met en zonder een tsunami')
fig2.show()
#Uit deze taartdiagram kan geconcludeerd worden dat circa 40 procent van alle geregistreede aardbevingen ook een tsunami teweeg brengen.


#pie chart van percentage tsunami's per continent 
df_grouped = df.groupby('continent')['tsunami'].value_counts().reset_index(name='counts')
fig3 = px.pie(df_grouped, values = 'counts', names = 'continent', color_discrete_sequence=["red", "green", "blue", "goldenrod", "magenta", "yellow"],labels={
                     "continent": "Continent"}, title='Percentage aardbevingen per continent')
fig3.show()


#bar chart van gap's per continent 
fig4 = px.bar(df, y="continent", x="gap", color="continent", orientation="h", hover_name="country",
             color_discrete_sequence=["magenta", "red", "blue", "green", "goldenrod", "yellow"],
             title="Gaps per continent", labels={
                     "continent": "Continent", "gap": "Gap"}
            )

fig4.show()
#in the continent Asia there is a lot of data about the gaps. Despite,in North America are the biggest gaps measured.
#biggest gaps: Mexico 239 degrees
#gap = the largest azimuthal gap between azimuthally adjacent station (in degrees)
#NOG VERHAAL BIJ TYPEN

#heatmap van earthquakes
fig5=plt.figure(figsize=(15, 10))
sns.heatmap(df[['magnitude','nst','estimated intensity','sig','depth']].corr(), annot=True,linecolor = 'black', cmap='Blues')
plt.title('Heatmap van interessante kolommen dataframe')
fig5.show()
#nst = the total number of seismic stations used to determine earthquake location

fig6 = px.scatter(df, y='magnitude', x='depth', title='Verband tussen de magnitude en de rupture diepte', labels={
                     "magnitude": "Magnitude", "depth": "Diepte"})
#hieruit is geen duidelijk verband te vinden tussen magnitude en de diepte van de rupture


fig7 = px.scatter(df, x="year", y="magnitude", color="alert", color_discrete_sequence=["green", "yellow", "orange", "red"], labels={
                     "year": "Jaar", "magnitude": "Magnitude"}, title='Verhouding tussen de magnitude en het alert per jaar')
fig7.show()
#hier zien we dat in 2010 een magnitude 'red' was afgegeven en in 2012 de hoogste magnitude 'yellow' was. 
#zegt deze data wel iets gezien hoogste magnitude eigenlijk 9.1 is? 

#BOXPLOT PER ALERT

#selecteer kolommen van belang van solar dataset
solar = solar[['earthquake.time', 'earthquake.latitude', 'earthquake.longitude', 'earthquake.mag', 'earthquake.place', 'MoonPhase.dynamic', 'MoonPhase.percent', 'day.duration', 'night.duration', 'Sun.height', 'Sun.speed', 'Moon.height', 'Moon.speed', 'Mars.height', 'Mars.speed']]

new_df = pd.merge(solar, df,  how='inner', left_on=['earthquake.latitude','earthquake.longitude'], right_on = ['latitude','longitude'])


fig8 = px.box(df, x='continent', y='magnitude', labels={"continent": "Continent", "magnitude": "Magnitude"}, title = 'Boxplot magnitude per continent met en zonder tsunami', color = 'tsunami')
fig8.show()
#we zien hier een uitschieter van mag 8.8 in South America bij geen tsunami
#laagst gemeten mag is 6.5

fig9 = px.box(new_df, x='tsunami', y='Moon.height', color='continent', labels={"tsunami": "Tsunami", "Moon.height": "Hoogte van de maan"}, title='Verband tussen de stand van de maan tegenover het voorkomen van een tsunami')

fig9.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="All continents",
                     method="update",
                     args=[{"visible": [True] * len(fig9.data)},
                           {"title": "All continents"}]),
                dict(label="Asia",
                     method="update",
                     args=[{"visible": [trace.name == 'Asia' for trace in fig9.data]},
                           {"title": "Asia"}]),
                dict(label="South America",
                     method="update",
                     args=[{"visible": [trace.name == 'South America' for trace in fig9.data]},
                           {"title": "South America"}]),
                dict(label="Europe",
                     method="update",
                     args=[{"visible": [trace.name == 'Europe' for trace in fig9.data]},
                           {"title": "Europe"}]),
                dict(label="North America",
                     method="update",
                     args=[{"visible": [trace.name == 'North America' for trace in fig9.data]},
                           {"title": "North America"}]),
                dict(label="Africa",
                     method="update",
                     args=[{"visible": [trace.name == 'Africa' for trace in fig9.data]},
                           {"title": "Africa"}]),
            ]),
        )
    ])



fig9.show()
#in deze plot zien we of de hoogte van de maan samenhangt met het ontstaan van een tsunami per continent. 
#bij de slider optie 'all continents' kunnen de continenten allemaal vergeleken worden.


fig10= px.scatter(new_df, x='sig', y='magnitude', animation_frame="year",trendline = 'ols', labels={"sig": "Significantie", "magnitude":"Magnitude"}, title='Verband tussen de significantie van een aardbeving en de magnitude')
fig10.show()
#hier zien we een duidelijk verschil tussen significantie van de aardbeving en de magnitude. 
#de trendlijn zal van 2001 steeds minder steil stijgen naar aanloop van 2016

fig11=px.scatter(df, x= 'depth', y='difference rep vs. est', color='depth', color_discrete_sequence=["green", "yellow", "orange", "red"],labels={"depth": "Diepte", "difference rep vs. est":"Verschil waargenomen en verwachte magnitude"}, trendline='ols', title='Verband tussen de accuratie van de magnitude voorspelling en de rupturediepte')
fig11.show()

#Folium map
tectonic_plates = pd.read_csv('all.csv')

def get_color(value):
    if value < 3:
        return 'green'
    elif 3 < value < 5:
        return 'yellow'
    elif 5 < value < 7:
        return 'orange'
    elif 7 < value < 8:
        return 'red'
    else:
        return 'black'

def get_popup(row):
    return f"Location: {row['location']}<br>Magnitude: {row['magnitude']}"

complete_map = folium.Map()

plate_layer = folium.FeatureGroup(name='Tectonic Plates')

plates = list(tectonic_plates['plate'].unique())
for plate in plates:
    plate_vals = tectonic_plates[tectonic_plates['plate'] == plate]
    lats = plate_vals['lat'].values
    lons = plate_vals['lon'].values
    points = list(zip(lats, lons))
    indexes = [None] + [i + 1 for i, x in enumerate(points) if i < len(points) - 1 and abs(x[1] - points[i + 1][1]) > 300] + [None]

    for i in range(len(indexes) - 1):
        folium.vector_layers.PolyLine(points[indexes[i]:indexes[i+1]], popup=plate, color='red', fill=False).add_to(plate_layer)
plate_layer.add_to(complete_map)

all_quakes = folium.FeatureGroup(name='All earthquakes')
tsunami_quakes = folium.FeatureGroup(name='Tsunami earthquakes')
mag_2_3 = folium.FeatureGroup(name='Magnitude 2-3')
mag_3_5 = folium.FeatureGroup(name='Magnitude 3-5')
mag_5_7 = folium.FeatureGroup(name='Magnitude 5-7')
mag_7_8 = folium.FeatureGroup(name='Magnitude 7-8')
mag_8 = folium.FeatureGroup(name='Magnitude >8')

for index, row in df.iterrows():
    popup_str = get_popup(row)
    color = get_color(row['magnitude'])
    
    marker = folium.Marker(location=[row['latitude'], row['longitude']],
                           popup=popup_str,
                           icon=folium.Icon(color=color))
    if row['magnitude'] < 3:
        mag_2_3.add_child(marker)
    elif 3 <= row['magnitude'] < 5:
        mag_3_5.add_child(marker)
    elif 5 <= row['magnitude'] < 7:
        mag_5_7.add_child(marker)
    elif 7 <= row['magnitude'] < 8:
        mag_7_8.add_child(marker)
    else:
        mag_8.add_child(marker)
        
    all_quakes.add_child(marker)
    
    if row['tsunami'] == 1:
        tsunami_marker = folium.Marker(location=[row['latitude'], row['longitude']],
                                       popup=popup_str,
                                      icon=folium.Icon(color=color))
        tsunami_quakes.add_child(tsunami_marker)
           

complete_map.add_child(all_quakes)
complete_map.add_child(tsunami_quakes)
complete_map.add_child(mag_2_3)
complete_map.add_child(mag_3_5)
complete_map.add_child(mag_5_7)
complete_map.add_child(mag_7_8)
complete_map.add_child(mag_8)
    
folium.LayerControl(position='bottomleft', collapsed=False).add_to(complete_map)
    
folium.LayerControl().add_to(complete_map)




image = Image.open('earthquake_.jpg')
image2 = Image.open('Legenda folium map.jpg')
######################################################################################################

st.image(image, caption='Bron: inszoneinsurance.com', width=1200)
st.title('Solar system and Earthquakes')
st.header('Een inzicht in de data verzameld over aardbevingen wereldwijd 2001-2022')
st.caption('Bron: Kaggle (CHIRAG CHAUHAN)')


tab1, tab2, tab3, tab4, tab5 = st.tabs(["Dataset", "Data exploratie", "Verbanden", "tab4", "Map"])

with tab1:
  st.header('Overzicht dataframe:')
  st.dataframe(new_df, width=1200)
  st.header('Betekenissen van de kolommen:')
  
  st.write('Title: Titel naam die aan de aardbeving is gegeven.')
  st.write('Magnitude: De magnitude van de aardbeving.')
  st.write('Date_time: Datum en tijd.')
  st.write('Reported intensity: De maximale opgemeten intensiteit voor de reikwijdte van het evenement.')
  st.write('Estimated intensity: De maximale voorspelde instrumentale intensiteit van het evenement.')
  st.write('Alert: Het alert level - “green”, “yellow”, “orange”, and “red”')
  st.write('Tsunami: "1" voor evenementen die voorkomen bij de oceaan en zo niet dan: "0".')
  st.write('Sig: Het nummer dat beschrijft hoe significant een evenement is. Grote nummers geven aan dat het evenement een hoge significantie heeft. Deze waarde wordt bepaald door meerdere factoren, waaronder: magnitude, maximale verwachte magnitude, waarnemingen vanuit de locatie, en de verwachtte impact.')
  st.write('Net: De ID van de dataverzamelaar, waardoor de juiste bron voor informatie over het evenement benoemd kan worden.')
  st.write('Nst: Het aantal seismische stations gebruikt om de exacte locatie van de aardbeving te bepalen.')
  st.write('Dmin: Horizontale afstand van het epicentrum tot het dichtstbijzijnde station.')
  st.write('Gap: Het grootste azimutale verschil tussen azimutaal aangrenzende stations (in graden). Over het algemeen geldt: hoe kleiner dit getal, hoe betrouwbaarder de berekende horizontale positie van de aardbeving. Aardbevingslocaties met een azimutale kloof van meer dan 180 graden hebben doorgaans grote locatie- en diepteonzekerheden.')
  st.write('MagType: De methode of het algoritme dat wordt gebruikt om de geprefereerde magnitude voor het voorval te berekenen')
  st.write('Depth: De diepte waar de aardbeving begint.')
  st.write('Latitude / Longitude: Coördinatenstelsel waarmee de positie of plaats van een plaats op het aardoppervlak kan worden bepaald en beschreven.')
  st.write('Location: Locatie in het land.')
  st.write('Continent: Continent van het door de aardbeving getroffen land.')
  st.write('Country: Getroffen land.')
  st.write('Diff rep vs. est: Verschil tussen de gerapporteerde en de geschatte intensiteit voor het gebeurtenissenbereik.')
  
  st.header('Betekenissen alerts:')
  st.write('Red: Geschatte dodelijke slachtoffers 1.000+, geschatte verliezen (USD) 1 miljard+.')
  st.write('Orange: Geschatte dodelijke slachtoffers 100 - 999, geschatte verliezen (USD) 100 miljoen - 1 miljard.')
  st.write('Yellow: Geschatte dodelijke slachtoffers 1-99, geschatte verliezen (USD) 1 miljoen - 100 miljoen.')
  st.write('Green: Geschatte dodelijke slachtoffers 0, geschatte verliezen (USD) < 1 miljoen.')
  
  
with tab2:
  st.header('Data exploratie')
  col1, col2 = st.columns([250, 20])
  with col1:
    st.plotly_chart(fig1)
    
  st.subheader('Conclusie aardbevingen per magnitude')
  st.write('Zoals we kunnen zien zijn er veel aardbevingen die in de magnitude 6.5 geschaald zijn')
  st.write('Er is een enkele aardbeving in de magnitude 9.1, hier hebben we verder onderzoek naar gedaan')

  with col2:
    st.plotly_chart(fig2)   
  st.subheader('Conclusie aardbevingen vs tsunami')
  st.write('Meer dan 60% van de aardbevingen hebben geen tsunami')
  
  col3, col4= st.columns([270, 5])
  with col3:
    st.plotly_chart(fig3)
  st.write('De meeste aardbevingen zijn in Azie ontstaan')
  st.write('In het continent Azie is er veel data over gaps. Ondanks dat zijn de grootste gaps gemeten in Noord-America, namelijk in Mexico. Hier is een gap van 239 degrees gemeten.')
  st.write('Met deze data zijn we verder gaan zoeken naar een verband met gaps.')
  
  with col4: 
    st.plotly_chart(fig4)
  st.write('In Azie is er veel data over de gaps, maar in Noord-Amerika zijn de grootste gaps gemeten.')
  
    
with tab3:
  st.header('Verbanden')
  
  col5, col14 = st.columns([270, 50])
  with col5:
    st.pyplot(fig5)
  
  with col14:
    st.subheader('Conclusies verbanden') 
    st.write('We hebben niet verder gekeken naar de significantie vs. estimated intensity omdat: ')
  
  
  col6, col7 = st.columns([250, 5])
  with col6:
    st.plotly_chart(fig8)
    st.subheader('Conclusie boxplot magnitude per continent met en zonder tsunami')
    st.write('Het valt op dat de gemiddelde magnitude van een aardbeving met een tsunami hoger ligt dan van aardbevingen zonder tsunami. HOE IS DIT TE VERKLAREN?')
  
  with col7:
    st.plotly_chart(fig6)

  st.subheader('Conclusie magnitude vs diepte van de rupture')
  st.write('Uit deze chart is geen duidelijk verband te vinden tussen magnitude en de diepte van de rupture.')
  
  
  col8, col9 = st.columns([250, 5])
  with col8: 
    st.plotly_chart(fig11)
  
  
  
  st.subheader('Conclusie accuratie van de magnitude en rupture diepte')
  st.write('Voor de accuratie van de magnitude hebben we een nieuwe kolom aangemaakt die het verschil laat zien tussen de estimated intensity en de reported intensity')
  st.write('We hebben al gezien dat de magnitude correleert met de intensity van de aardbeving in de heatmap.') 
  st.write('In deze plot is een trendline weergegeven die als R^2 een 0.019784 aangeeft. De R Squared geeft aan hoeveel van de variantie in de afhankelijk variabele verklaard wordt door de verklarende variabelen.')
  st.write('In dit geval verklaart de variabele diepte voor 1,9% het verschil tussen de predicted en estimated intensity.')
  st.write('Wat wel duidelijk is geworden uit deze plot is dat bij een minimale rupture diepte, de accuratie van de intensity slechter voorspeld is'.)
  st.subheader('Conclusie alerts vs magnitude')
  st.write('Het valt op dat de accuratie van de alerts afgegeven niet altijd even goed is.')
  st.write('In 2010 was er een rood alert afgegeven voor een aarbeving met magnitude 7.2 terwijl in 2012 een groen alert was afgegeven voor een aardbeving van magnitude 8.2.')
  st.write('WAT IS HIER EEN LOGISCHE VERKLARING VOOR?') 
  
with col9:
  st.plotly_chart(fig7)
  
 
with tab4:
  st.header('tab4')
  col10, col11 = st.columns([250, 5])
  with col11:
    st.plotly_chart(fig8)
    
    st.write('Het valt op dat de gemiddelde magnitude van een aardbeving met een tsunami hoger ligt dan van aardbevingen zonder tsunami.')
    
    st.plotly_chart(fig10)
  st.write('Als men de  trendlijn bekijkt van 2001 tot 2016 valt op dat deze steeds minder stijl wordt over de jaren heen. Dit zou betekenen dat er bij aardbevingen met een hogere magnitude resulteert in een evenement met een hogere significantie .')
  
  
  with col10:
    st.plotly_chart(fig9)
    st.write('Deze grafiek is alleen relevant voor Azie en Zuid-Amerika, hier is bij beide continenten te zien dat de hoogte van de maan gemiddeld hoger ligt bij het voorkomen van een tsunami.')
  
  
with tab5:
  st.header('Map')
  col12, col13 = st.columns([270, 5])
  with col12: 
    st.write('In deze map zijn de locaties van alle aarbevingen van de dataset te zien in combinatie met de locatie van de tectonische aardplaten. Het valt op dat de meeste aardbevingen zich bevinden rondom een aardplaat, wat uiteraard logisch is aangezien aardbevingen ontstaan door verschuivingen van deze aardplaten.')
    st_folium(complete_map, width=1200)
    with col13:
      st.image(image2, width=75)
             





