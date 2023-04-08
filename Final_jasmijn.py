#!/usr/bin/env python
# coding: utf-8

# In[11]:



import requests

import pandas as pd

import folium

import streamlit as st

#from streamlit_folium import st_folium

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
fig1 = px.bar(df_mag, x="Magnitude", y='Count')
fig1.update_layout(xaxis = dict(dtick = 0.1))
fig1.show()


#pie chart van procent aardbevingen met of zonder tsunami
tsunami_pie=df['tsunami'].value_counts().reset_index()
tsunami_pie= tsunami_pie.rename(columns = {'index':'Tsunami', 'tsunami':'Counts'})
fig2= px.pie(tsunami_pie, values='Counts', names='Tsunami')
fig2.show()
#Uit deze taartdiagram kan geconcludeerd worden dat circa 40 procent van alle geregistreede aardbevingen ook een tsunami teweeg brengen.


#pie chart van percentage tsunami's per continent 
df_grouped = df.groupby('continent')['tsunami'].value_counts().reset_index(name='counts')
fig3 = px.pie(df_grouped, values = 'counts', names = 'continent', color = 'tsunami')
fig3.show()
#DROPDOWN inzetten

#bar chart van gap's per continent 
fig4 = px.bar(df, y="continent", x="gap", color="continent", orientation="h", hover_name="country",
             color_discrete_sequence=["red", "green", "blue", "goldenrod", "magenta"],
             title="Gaps per continent"
            )

fig4.show()
#in the continent Asia there is a lot of data about the gaps. Despite,in North America are the biggest gaps measured.
#biggest gaps: Mexico 239 degrees
#gap = the largest azimuthal gap between azimuthally adjacent station (in degrees)
#NOG VERHAAL BIJ TYPEN

#heatmap van earthquakes
fig5=plt.figure(figsize=(15, 10))
sns.heatmap(df[['magnitude','nst','estimated intensity','sig','depth']].corr(), annot=True,linecolor = 'black', cmap='Blues')
fig5.show()
#nst = the total number of seismic stations used to determine earthquake location

px.scatter(df, y='magnitude', x='depth')
#hieruit is geen duidelijk verband te vinden tussen magnitude en de diepte van de rupture


fig6 = px.scatter(df, x="year", y="magnitude", color="alert", color_discrete_sequence=["green", "yellow", "orange", "red"])
fig6.show()
#hier zien we dat in 2010 een magnitude 'red' was afgegeven en in 2012 de hoogste magnitude 'yellow' was. 
#zegt deze data wel iets gezien hoogste magnitude eigenlijk 9.1 is? 

#BOXPLOT PER ALERT

#selecteer kolommen van belang van solar dataset
solar = solar[['earthquake.time', 'earthquake.latitude', 'earthquake.longitude', 'earthquake.mag', 'earthquake.place', 'MoonPhase.dynamic', 'MoonPhase.percent', 'day.duration', 'night.duration', 'Sun.height', 'Sun.speed', 'Moon.height', 'Moon.speed', 'Mars.height', 'Mars.speed']]

new_df = pd.merge(solar, df,  how='inner', left_on=['earthquake.latitude','earthquake.longitude'], right_on = ['latitude','longitude'])


fig7 = px.box(df, x='continent', y='magnitude', title = 'Boxplot magnitude per continent with and without tsunami', color = 'tsunami')
fig7.show()
#we zien hier een uitschieter van mag 8.8 in South America bij geen tsunami
#laagst gemeten mag is 6.5

fig8 = px.box(new_df, x='tsunami', y='Moon.height', color='continent')

fig8.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="All continents",
                     method="update",
                     args=[{"visible": [True] * len(fig7.data)},
                           {"title": "All continents"}]),
                dict(label="Asia",
                     method="update",
                     args=[{"visible": [trace.name == 'Asia' for trace in fig7.data]},
                           {"title": "Asia"}]),
                dict(label="South America",
                     method="update",
                     args=[{"visible": [trace.name == 'South America' for trace in fig7.data]},
                           {"title": "South America"}]),
                dict(label="Europe",
                     method="update",
                     args=[{"visible": [trace.name == 'Europe' for trace in fig7.data]},
                           {"title": "Europe"}]),
                dict(label="North America",
                     method="update",
                     args=[{"visible": [trace.name == 'North America' for trace in fig7.data]},
                           {"title": "North America"}]),
                dict(label="Africa",
                     method="update",
                     args=[{"visible": [trace.name == 'Africa' for trace in fig7.data]},
                           {"title": "Africa"}]),
            ]),
        )
    ])



fig8.show()
#in deze plot zien we of de hoogte van de maan samenhangt met het ontstaan van een tsunami per continent. 
#bij de slider optie 'all continents' kunnen de continenten allemaal vergeleken worden.


# In[58]:


fig9= px.scatter(new_df, x='sig', y='magnitude', animation_frame="year",trendline = 'ols')
fig9.show()
#hier zien we een duidelijk verschil tussen significantie van de aardbeving en de magnitude. 
#de trendlijn zal van 2001 steeds minder steil stijgen naar aanloop van 2016

image = Image.open('earthquake_.jpg')
###############
st.image(image, caption='Bron: inszoneinsurance.com')
st.title('Aardbevingen dataset')
st.header('Een inzicht in de data verzameld over aardbevingen wereldwijd')
st.caption('Bron: Kaggle (CHIRAG CHAUHAN)')

col1, col2 = st.columns([80, 10])
with col1:
  st.plotly_chart(fig1)
with col2:
  st.plotly_chart(fig2)
with col1:
  st.plotly_chart(fig3)
with col2:
  st.plotly_chart(fig4)
with col1:
  st.pyplot(fig5)
with col2:
  st.plotly_chart(fig6)
with col1:
  st.plotly_chart(fig7)
with col2:
  st.plotly_chart(fig8)
with col1:
  st.plotly_chart(fig9)





