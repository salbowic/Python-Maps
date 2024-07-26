import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

# dane o cenach za 1m2 mieszkan
dane_rynek_mieszkan_file = 'data/RYNE_3775_CTAB_20231230170737.csv'
ceny_mieszkan_gus = pd.read_csv(dane_rynek_mieszkan_file, delimiter=';')
ceny_mieszkan_gus = ceny_mieszkan_gus.iloc[:, 0:15]
ceny_mieszkan_gus.columns = ['TERYT', 'Nazwa', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022'] 
ceny_mieszkan_gus['TERYT_gmin'] = ceny_mieszkan_gus.TERYT.apply(lambda x: '0'+str(x) if len(str(x)) < 7 else str(x))
ceny_mieszkan_gus['TERYT_woj'] = ceny_mieszkan_gus.TERYT_gmin.apply(lambda s: s[:2])

# usuwamy wiersz z całą Polską:
ceny_mieszkan_gus = ceny_mieszkan_gus[ceny_mieszkan_gus['TERYT'] != '0']
# print(ceny_mieszkan_gus)

ceny_mieszkan_gus_woj = ceny_mieszkan_gus[ceny_mieszkan_gus.TERYT_gmin.str[2:7] == '00000']
ceny_mieszkan_gus_gmin = ceny_mieszkan_gus[ceny_mieszkan_gus.TERYT_gmin.str[4:7] == '000']
ceny_mieszkan_gus_gmin['TERYT_gmin'] = ceny_mieszkan_gus_gmin['TERYT_gmin'].str[:-2]


# mapa województw
mapa_woj = gpd.read_file('data/PRG_jednostki_administracyjne_2022/A01_Granice_wojewodztw.shp')
mapa_woj = mapa_woj[['JPT_KOD_JE', 'JPT_NAZWA_', 'geometry']]
# mapa gmin
mapa_gmin = gpd.read_file('data/PRG_jednostki_administracyjne_2022/A03_Granice_gmin.shp')
mapa_gmin = mapa_gmin[['JPT_KOD_JE', 'JPT_NAZWA_', 'geometry']]
mapa_gmin['JPT_KOD_JE'] = mapa_gmin['JPT_KOD_JE'].str[:-2]


dane_mapa_woj = pd.merge(mapa_woj, ceny_mieszkan_gus_woj, how='left', left_on='JPT_KOD_JE', right_on='TERYT_woj')
dane_mapa_gmin = pd.merge(mapa_gmin, ceny_mieszkan_gus_gmin, how='left', left_on='JPT_KOD_JE', right_on='TERYT_gmin')

fig, ax = plt.subplots(1, figsize = (8,8))

column_name = '2022'
dane_mapa_gmin.plot(column = column_name, ax=ax, cmap='YlOrRd', linewidth=0.4, edgecolor='black', legend=True, missing_kwds={'color': 'grey'})
title = f'Cena w zł za 1 m2 lokalu ({column_name}r.)'

ax.set_title(title, fontdict={'fontsize': '16', 'fontweight' : '3'}) #tytuł
ax.axis('off')

plt.show()