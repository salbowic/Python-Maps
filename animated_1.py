import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

mapa_gmin = gpd.read_file('data/PRG_jednostki_administracyjne_2022/A03_Granice_gmin.shp')
mapa_gmin = mapa_gmin[['JPT_KOD_JE', 'JPT_NAZWA_', 'geometry']]
mapa_gmin['JPT_KOD_JE'] = mapa_gmin['JPT_KOD_JE'].str[:-2]

dane_rynek_mieszkan_file = 'data/RYNE_3775_CTAB_20231230170737.csv'
ceny_mieszkan_gus = pd.read_csv(dane_rynek_mieszkan_file, delimiter=';')
ceny_mieszkan_gus = ceny_mieszkan_gus.iloc[:, 0:15]
ceny_mieszkan_gus.columns = ['TERYT', 'Nazwa', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022']
ceny_mieszkan_gus['TERYT_gmin'] = ceny_mieszkan_gus.TERYT.apply(lambda x: '0'+str(x) if len(str(x)) < 7 else str(x))
ceny_mieszkan_gus = ceny_mieszkan_gus[ceny_mieszkan_gus['TERYT'] != '0']

ceny_mieszkan_gus = ceny_mieszkan_gus[ceny_mieszkan_gus['TERYT'] != '0']
ceny_mieszkan_gus_gmin = ceny_mieszkan_gus[ceny_mieszkan_gus.TERYT_gmin.str[4:7] == '000']
ceny_mieszkan_gus_gmin['TERYT_gmin'] = ceny_mieszkan_gus_gmin['TERYT_gmin'].str[:-2]

merged_data = pd.merge(mapa_gmin, ceny_mieszkan_gus_gmin, left_on='JPT_KOD_JE', right_on='TERYT_gmin')

fig, ax = plt.subplots(figsize=(12, 8))

max_value = 18000

colors = [(0, 0, 0),  (1, 0, 0), (1, 0.5, 0), (1, 1, 0)]  # RGB (black to red)
custom_cmap = LinearSegmentedColormap.from_list('custom', colors, N=256)

viridis_cmap = plt.cm.hot
merged_data.plot(ax=ax, column='2010', cmap=custom_cmap, legend=True, vmin=0, vmax=max_value)

# Funkcja aktualizująca mapę dla każdej klatki
def update(frame):
    ax.clear()
    merged_data.plot(ax=ax, column=str(frame), cmap=custom_cmap, legend=False)
    ax.set_title(f'Cena w zł za 1 m2 lokalu ({frame}r.)')
    ax.axis('off')

animation = FuncAnimation(fig, update, frames=range(2010, 2023), interval=1000)

plt.show()