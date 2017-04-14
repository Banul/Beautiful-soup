# coding=utf-8
import BeautifulSoup as BeautifulSoup
from bs4 import BeautifulSoup
import requests
import string
import pandas as pd
from datetime import datetime
import sqlite3

conn = sqlite3.connect("dane.db")



k=0

frames=[]
while True:
   # link = "http://powietrze.gios.gov.pl/pjp/current/station_details/table/485/10/"+str(k)
    link = "http://powietrze.gios.gov.pl/pjp/current/station_details/table/966/10/"+str(k)

    k=k+1
    r = requests.get(link)
    data = r.text
    soup = BeautifulSoup(data,"lxml")

    table = soup.find_all('table')[0]
    rows = table.find_all('tr')[2:-3]

    data = {
            'date' :[],
           # 'hour' : [],
            'PM10' : [],
            'PM25' : [],
            'O3' : [],
            'NO2' : [],
            'SO2' : [],
           # 'C6H6' : [],
            'CO' : []
           }

    for row in rows:
        value = row.find_all('td')
        try:
            data['PM10'].append(float((value[0].get_text()).replace(",",".")))
        except ValueError:
            data['PM10'].append(float ('NaN'))
        try:
            data['PM25'].append(float((value[1].get_text()).replace(",",".")))
        except ValueError:
            data['PM25'].append(float ('NaN'))
        try:
            data['O3'].append(float((value[2].get_text()).replace(",",".")))
        except ValueError:
            data['O3'].append(float ('NaN'))
        try:
            data['NO2'].append(float((value[3].get_text()).replace(",",".")))
        except ValueError:
            data['NO2'].append (float('NaN'))
        try:
            data['SO2'].append(float((value[4].get_text()).replace(",", ".")))
        except ValueError:
            data['SO2'].append(float('NaN'))
       # try:
       #    data['C6H6'].append(float((value[5].get_text()).replace(",",".")))
       # except ValueError:
       #     data['C6H6'].append('NaN')
        try:
          data['CO'].append(float((value[6].get_text()).replace(",",".")))
        except ValueError:
            data['CO'].append(float('NaN'))

    tbody = soup.find_all('tbody')[0]
    szukane = (tbody.find_all('th'))[0:-3]

    for element in szukane:
        dodamToData = element.get_text()[0:10]
       # data['date'].append(dodamToData)
        dodamToGodzina = element.get_text()[12:17]
        sformatowanaData= dodamToData+' '+dodamToGodzina
        sformatowanaDataTa = datetime.strptime(sformatowanaData,'%d.%m.%Y %H:%M')
        data['date'].append(sformatowanaDataTa)

    df = pd.DataFrame.from_dict(data)
    if df.empty:
        break
    else:
        frames.append(df)


df=pd.concat(frames,ignore_index=True)
df= pd.DataFrame(df)

df=df.dropna(axis=1,how='all')
df=df.dropna()
df = df.set_index('date')

df.to_sql('zanieczyszczenia', conn, if_exists='replace')




