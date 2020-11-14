import os
import pandas as pd
import numpy as np
from src.config import get_project_root
#Rende il codice indipendente dal tuo filesystem local, a patto che scarichi la cartella 'fantacalcio'
ROOT = get_project_root()
#Create an object "calendar" and define following function as methods?

def import_calendar():
    #Funzione per importare il calendario sotto forma di dataframe
    data_path = os.path.join(ROOT,'data')
    calendar_raw_name = 'Calendario_Campionato---A-buon-rendere.xlsx'
    calendar_path = os.path.join(data_path,calendar_raw_name)
    if os.path.isfile(calendar_path):
        calendar_raw = pd.read_excel(calendar_path,skiprows=2)
    else:
        #Se non trova il calendario nella cartella 'data' si incazza
        print('porcoddio')
    return calendar_raw

def clean_calendar(calendar_raw):
    #Funzione per pulire il calendario e renderlo più utilizzabile.
    #Secondo me convienve fare un dataframe con ogni squadra e associato un vettore di 'Gol','FP','Avversari'
    #df_persquadra = pd.DataFrame(columns=['Squadre','Avversari','Gol', 'Fantapunti'])
    colonna_giornata = ['Unnamed: 0', 'Unnamed: 6']
    for cg in colonna_giornata:
        j = calendar_raw.columns.get_loc(cg)
        inizio_giornata = np.where(calendar_raw[cg].astype(str).str.contains('Giornata'))[0]
        for ig in inizio_giornata:
            nome_giornata = calendar_raw[cg][ig]
            ngiornata = int(''.join(x for x in nome_giornata if x.isdigit()))
            if ngiornata == 1:
                squadre = calendar_raw.iloc[ig+1:ig+5,j].append(calendar_raw.iloc[ig+1:ig+5,j+3],ignore_index=True)
                df_persquadra = pd.DataFrame(index=squadre)
                fp = calendar_raw.iloc[ig+1:ig+5,j+1].append(calendar_raw.iloc[ig+1:ig+5,j+2],ignore_index=True).astype(float)
                df_persquadra['Fantapunti'] = fp.values
                avversari = calendar_raw.iloc[ig+1:ig+5,j+3].append(calendar_raw.iloc[ig+1:ig+5,j],ignore_index=True)
                df_persquadra['Avversari'] = avversari.values
                Gol = np.zeros(8,dtype=int)
                results = calendar_raw.iloc[ig+1:ig+5,j+4]
                for idx,res in enumerate(results):
                    Gol[idx] = int(res.split('-')[0])
                    Gol[idx+4] = int(res.split('-')[1])
                df_persquadra['Gol'] = Gols
                df_persquadra= df_persquadra.astype(object)
                ordine_giornate = [ngiornata]
            else:
                print(ngiornata,j)
                squadresx = calendar_raw.iloc[ig+1:ig+5,j]
                squadredx = calendar_raw.iloc[ig+1:ig+5,j+3]
                for idx,squadra in enumerate(squadresx):
                    #Per le squadre sulla sinistra il punteggio si trova alla loro destra
                    df_persquadra.at[squadra,'Fantapunti'] \
                    = np.append(df_persquadra.at[squadra,'Fantapunti'],calendar_raw.iloc[ig+idx+1,j+1])
                    df_persquadra.at[squadra,'Avversari'] \
                    = np.append(df_persquadra.at[squadra,'Avversari'],calendar_raw.iloc[ig+idx+1,j+3])
                    if calendar_raw.iloc[ig+idx+1,j+4].split('-')[0].isdigit():
                        gol = int(calendar_raw.iloc[ig+idx+1,j+4].split('-')[0])
                    else: 
                        gol = float('NaN')
                    df_persquadra.at[squadra,'Gol'] \
                    = np.append(df_persquadra.at[squadra,'Gol'],gol)
                for idx,squadra in enumerate(squadredx):
                    #Per le squadre sulla sinistra il punteggio si trova alla loro destra
                    df_persquadra.at[squadra,'Fantapunti'] \
                    = np.append(df_persquadra.at[squadre.values[0],'Fantapunti'],calendar_raw.iloc[ig+idx+1,j+2])
                    df_persquadra.at[squadra,'Avversari'] \
                    = np.append(df_persquadra.at[squadra,'Avversari'],calendar_raw.iloc[ig+idx+1,j])
                    if calendar_raw.iloc[ig+idx+1,j+4].split('-')[1].isdigit():
                        gol = int(calendar_raw.iloc[ig+idx+1,j+4].split('-')[1])
                    else: 
                        gol = float('NaN')
                    df_persquadra.at[squadra,'Gol'] \
                    = np.append(df_persquadra.at[squadra,'Gol'],gol)
              
                ordine_giornate.append(ngiornata)
    #Todo: sort all the arrays
    return  df_persquadra,np.array(ordine_giornate)
