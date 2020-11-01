import pandas as pd
import warnings
warnings.filterwarnings('ignore')

fname = "Calendario_Campionato---A-buon-rendere.xlsx"
df = pd.read_excel(fname, skiprows=2)
df = df.drop(['Unnamed: 5', 'Unnamed: 4', 'Unnamed: 10'], axis=1)
ultima_giornata = df.iloc[86:90] #poi qua dovrai fare l'append
df = df.dropna()
df = df.reset_index(drop=True)

start = 0
data = pd.DataFrame()
while start < 69: 
    blocco = df.iloc[start:start+4]
    start = start+4
    blocco1 = blocco[['Unnamed: 0', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3']]
    blocco2 = blocco[['Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9']]
    rencol_2 = ['Unnamed: 0', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3']
    blocco2.columns = rencol_2
    blocco1 = blocco1.append(blocco2)
    data = data.append(blocco1)
data = data.append(ultima_giornata)
data = data.drop(['Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9'], axis=1)
data = data.reset_index(drop=True)

players = list(set(df['Unnamed: 0']))
players = sorted(players, key=str.lower)
df = pd.DataFrame()

for player in players:
    a = data[data["Unnamed: 0"].str.contains(player)]
    b = data[data["Unnamed: 3"].str.contains(player)]
    a = a[['Unnamed: 0', 'Unnamed: 1']]
    b = b[['Unnamed: 3', 'Unnamed: 2']]
    nomi_colonne = ['squadra', 'fantapunti']
    a.columns = nomi_colonne
    b.columns = nomi_colonne
    frames = [a,b]
    result = pd.concat(frames)
    result = result.sort_index()
    result = result.reset_index(drop=True)
    df = df.append(result)