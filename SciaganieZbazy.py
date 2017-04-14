# coding=utf-8

import sqlite3
import pandas as pd
# Create your connection.
cnx = sqlite3.connect('dane.db')

df_pogoda = pd.read_sql_query("SELECT * FROM pogoda_otwock", cnx)
df_zanieczyszczenia = pd.read_sql_query("SELECT * FROM zanieczyszczenia", cnx)


#należy ustalić początek df_pogoda i df_zanieczyszczenia oraz ich końce, tak aby daty startu i daty stopu były takie same:

#1. szukam poczatku:

def znajdz_poczatek():
    indeks_pogoda = 0
    indeks_zanieczyszczenia = 0
    while True:
        try:
            poczatek_pogoda = df_pogoda['czas'][indeks_pogoda]
            poczatek_zanieczyszczenia = df_zanieczyszczenia['date'][indeks_zanieczyszczenia]
        except:
            indeks_pogoda += 1
            indeks_zanieczyszczenia = 0
            continue
        if poczatek_pogoda == poczatek_zanieczyszczenia:
            break
        else:
            indeks_zanieczyszczenia += 1
    return poczatek_pogoda


#2. Szukam konca:

def znajdz_koniec():
    ostatni_indeks_pogoda = len(df_pogoda)-1
    ostatni_indeks_zanieczyszczenia = len(df_zanieczyszczenia)-1
    while True:
        try:
            koniec_pogoda = df_pogoda['czas'][ostatni_indeks_pogoda]
            koniec_zanieczyszczenia = df_zanieczyszczenia['date'][ostatni_indeks_zanieczyszczenia]
        except:
            ostatni_indeks_pogoda-=1
            ostatni_indeks_zanieczyszczenia=len(df_zanieczyszczenia)-1
            continue
        if koniec_pogoda==koniec_zanieczyszczenia:
            break
        else:
             ostatni_indeks_zanieczyszczenia-=1

    return koniec_pogoda


df_pogoda = df_pogoda[df_pogoda.czas>=znajdz_poczatek()]
df_pogoda=df_pogoda.reset_index(drop=True)
df_pogoda = df_pogoda[df_pogoda.czas<=znajdz_koniec()]
df_pogoda = df_pogoda.reset_index(drop=True)

df_zanieczyszczenia = df_zanieczyszczenia [df_zanieczyszczenia.date>=znajdz_poczatek()]
df_zanieczyszczenia = df_zanieczyszczenia.reset_index(drop=True)
df_zanieczyszczenia = df_zanieczyszczenia [df_zanieczyszczenia.date<=znajdz_koniec()]
df_zanieczyszczenia = df_zanieczyszczenia.reset_index(drop=True)

datyZan = df_zanieczyszczenia['date']
datyPog = df_pogoda ['czas']


doUsunieciaPog = list(set(datyPog)-set(datyZan))
doUsunieciaZan = list(set(datyZan)-set(datyPog))

for iterator in doUsunieciaPog:
        df_pogoda = df_pogoda[df_pogoda.czas != iterator]


for iterator in doUsunieciaZan:
        df_zanieczyszczenia = df_zanieczyszczenia[df_zanieczyszczenia.date != iterator]

print len(df_zanieczyszczenia)
print len(df_pogoda)

print df_pogoda
print df_zanieczyszczenia

