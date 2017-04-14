import BeautifulSoup as BeautifulSoup
from bs4 import BeautifulSoup
import requests
import string
import pandas as pd
import sqlite3
from datetime import datetime


k=0
frames=[]
conn = sqlite3.connect("C:\Users\User\Desktop\inz\dane.db")


for i in range(0,3):
    link = "http://www.policja.pl/pol/form/1,Statystyki-dnia.html?page="+str(k)
    k += 1
    r = requests.get(link)

    data = r.text
    soup = BeautifulSoup(data,"lxml")

    table = soup.find_all('table')[0]
    rows = table.find_all('tr')[1:]

    slownik = {
            'date' : [],
            'zatrz_goracym' : [],
            'zatrz_poszuk' : [],
            'zatrz_nietrzezwi' : [],
            'wypadki' : [],
            'zabici' : [],
            'ranni' : []

            }

    #formatowanaDataTa = datetime.strptime(sformatowanaData,'%d.%m.%Y %H:%M')
    for row in rows:
        value = row.find_all('td')
        data = str(value[0].get_text())
        formatowanaData = datetime.strptime(data,'%d.%m.%Y')
        slownik['date'].append(formatowanaData)
        slownik['zatrz_goracym'].append(value[1].get_text())
        slownik['zatrz_poszuk'].append(value[2].get_text())
        slownik['zatrz_nietrzezwi'].append(value[3].get_text())
        slownik['wypadki'].append(value[4].get_text())
        slownik['zabici'].append(value[5].get_text())
        slownik['ranni'].append(value[6].get_text())

    df = pd.DataFrame.from_dict(slownik)
    frames.append(df)

df=pd.concat(frames,ignore_index=True)
df= pd.DataFrame(df)
df=df.dropna()

df.to_sql('wypadki', conn, if_exists='replace')


