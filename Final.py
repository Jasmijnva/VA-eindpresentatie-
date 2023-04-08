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


# In[ ]:





# In[41]:


solar = pd.read_csv('SolarSystemAndEarthquakes.csv')
df = pd.read_csv('earthquake_data.csv')


# In[42]:


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# In[43]:


df['Date'] = pd.to_datetime(df['date_time']).dt.date
df['Time'] = pd.to_datetime(df['date_time']).dt.time


# In[44]:


df['date_time'] =  pd.to_datetime(df['date_time'], format='%d%m%Y%I%M', errors = 'ignore')


# In[45]:


df['year'] = pd.DatetimeIndex(df['Date']).year
df['month'] = pd.DatetimeIndex(df['Date']).month


# In[46]:


df = df.drop(['date_time', 'Date', 'title'], axis=1)
df = df.rename(columns = {'cdi':'reported intensity', 'mmi':'estimated intensity'})
df['difference rep vs. est'] = df['reported intensity'] - df['estimated intensity']
df['tsunami'] = df['tsunami'].replace({1: True, 0: False})


# In[47]:


df.groupby('year')['tsunami'].sum()
#hoe kan het dat er van 2001 tot en met 2012 geen tsunami's waren? foutieve data? 
#eventueel nog een plot van maken met visualisatie 


# In[48]:


df_mag=df['magnitude'].value_counts().reset_index()
df_mag=df_mag.rename(columns={"index": "Magnitude", "magnitude": "Count"})


# In[49]:


fig2 = px.bar(df_mag, x="Magnitude", y='Count')
fig2.update_layout(xaxis = dict(dtick = 0.1))
fig2.show()


# In[50]:


tsunami_pie=df['tsunami'].value_counts().reset_index()
tsunami_pie= tsunami_pie.rename(columns = {'index':'Tsunami', 'tsunami':'Counts'})
fig7= px.pie(tsunami_pie, values='Counts', names='Tsunami')
fig7.show()
#Uit deze taartdiagram kan geconcludeerd worden dat circa 40 procent van alle geregistreede aardbevingen ook een tsunami teweeg brengen.


# In[51]:


df_grouped = df.groupby('continent')['tsunami'].value_counts().reset_index(name='counts')
fig6 = px.pie(df_grouped, values = 'counts', names = 'continent', color = 'tsunami')
fig6.show()
#DROPDOWN inzetten


# In[52]:


fig = px.bar(df, y="continent", x="gap", color="continent", orientation="h", hover_name="country",
             color_discrete_sequence=["red", "green", "blue", "goldenrod", "magenta"],
             title="Gaps per continent"
            )

fig.show()
#in the continent Asia there is a lot of data about the gaps. Despite,in North America are the biggest gaps measured.
#biggest gaps: Mexico 239 degrees
#gap = the largest azimuthal gap between azimuthally adjacent station (in degrees)
#NOG VERHAAL BIJ TYPEN


# In[53]:


plt.figure(figsize=(15, 10))
sns.heatmap(df[['magnitude','nst','estimated intensity','sig','depth']].corr(), annot=True,linecolor = 'black', cmap='Blues')
plt.show()
#nst = the total number of seismic stations used to determine earthquake location


# In[ ]:





# In[ ]:





# In[54]:


px.scatter(df, y='magnitude', x='depth')
#hieruit is geen duidelijk verband te vinden tussen magnitude en de diepte van de rupture


# In[ ]:





# In[ ]:





# In[20]:


fig = px.scatter(df, x="year", y="magnitude", color="alert", color_discrete_sequence=["green", "yellow", "orange", "red"])
fig.show()
#hier zien we dat in 2010 een magnitude 'red' was afgegeven en in 2012 de hoogste magnitude 'yellow' was. 
#zegt deze data wel iets gezien hoogste magnitude eigenlijk 9.1 is? 

#BOXPLOT PER ALERT


# In[55]:


solar = solar[['earthquake.time', 'earthquake.latitude', 'earthquake.longitude', 'earthquake.mag', 'earthquake.place', 'MoonPhase.dynamic', 'MoonPhase.percent', 'day.duration', 'night.duration', 'Sun.height', 'Sun.speed', 'Moon.height', 'Moon.speed', 'Mars.height', 'Mars.speed']]


# In[56]:


new_df = pd.merge(solar, df,  how='inner', left_on=['earthquake.latitude','earthquake.longitude'], right_on = ['latitude','longitude'])


# In[ ]:





# In[18]:


fig = px.box(df, x='continent', y='magnitude', title = 'Boxplot magnitude per continent with and without tsunami', color = 'tsunami')
fig.show()
#we zien hier een uitschieter van mag 8.8 in South America bij geen tsunami
#laagst gemeten mag is 6.5


# In[59]:


plt = px.box(new_df, x='tsunami', y='Moon.height', color='continent')

plt.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="All continents",
                     method="update",
                     args=[{"visible": [True] * len(plt.data)},
                           {"title": "All continents"}]),
                dict(label="Asia",
                     method="update",
                     args=[{"visible": [trace.name == 'Asia' for trace in plt.data]},
                           {"title": "Asia"}]),
                dict(label="South America",
                     method="update",
                     args=[{"visible": [trace.name == 'South America' for trace in plt.data]},
                           {"title": "South America"}]),
                dict(label="Europe",
                     method="update",
                     args=[{"visible": [trace.name == 'Europe' for trace in plt.data]},
                           {"title": "Europe"}]),
                dict(label="North America",
                     method="update",
                     args=[{"visible": [trace.name == 'North America' for trace in plt.data]},
                           {"title": "North America"}]),
                dict(label="Africa",
                     method="update",
                     args=[{"visible": [trace.name == 'Africa' for trace in plt.data]},
                           {"title": "Africa"}]),
            ]),
        )
    ])



plt.show()
#in deze plot zien we of de hoogte van de maan samenhangt met het ontstaan van een tsunami per continent. 
#bij de slider optie 'all continents' kunnen de continenten allemaal vergeleken worden.


# In[58]:


plt = px.scatter(new_df, x='sig', y='magnitude', animation_frame="year",trendline = 'ols')
plt.show()
#hier zien we een duidelijk verschil tussen significantie van de aardbeving en de magnitude. 
#de trendlijn zal van 2001 steeds minder steil stijgen naar aanloop van 2016


# In[ ]:




