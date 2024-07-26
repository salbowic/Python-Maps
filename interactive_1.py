import pandas as pd
import geopandas as gpd
import folium
from IPython.display import display
import ipywidgets as widgets

# dane o cenach za 1m2 mieszkan
dane_rynek_mieszkan_file = 'data/RYNE_3775_CTAB_20231230170737.csv'
ceny_mieszkan_gus = pd.read_csv(dane_rynek_mieszkan_file, delimiter=';')
ceny_mieszkan_gus = ceny_mieszkan_gus.iloc[:, 0:15]
ceny_mieszkan_gus.columns = ['TERYT', 'Nazwa', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022'] 
ceny_mieszkan_gus['TERYT_gmin'] = ceny_mieszkan_gus.TERYT.apply(lambda x: '0'+str(x) if len(str(x)) < 7 else str(x))
ceny_mieszkan_gus['TERYT_woj'] = ceny_mieszkan_gus.TERYT_gmin.apply(lambda s: s[:2])

# usuwamy wiersz z całą Polską:
ceny_mieszkan_gus = ceny_mieszkan_gus[ceny_mieszkan_gus['TERYT'] != '0']
print(ceny_mieszkan_gus)

ceny_mieszkan_gus_gmin = ceny_mieszkan_gus[ceny_mieszkan_gus.TERYT_gmin.str[4:7] == '000']
ceny_mieszkan_gus_gmin['TERYT_gmin'] = ceny_mieszkan_gus_gmin['TERYT_gmin'].str[:-2]
mapa_gmin = gpd.read_file('data/PRG_jednostki_administracyjne_2022/A03_Granice_gmin.shp')
mapa_gmin = mapa_gmin[['JPT_KOD_JE', 'JPT_NAZWA_', 'geometry']]
mapa_gmin['JPT_KOD_JE'] = mapa_gmin['JPT_KOD_JE'].str[:-2]

ceny_mieszkan_gus_gmin['TERYT_gmin'] = ceny_mieszkan_gus_gmin['TERYT_gmin'].astype(str)
mapa_gmin['JPT_KOD_JE'] = mapa_gmin['JPT_KOD_JE'].astype(str)

mapa_gmin.geometry = mapa_gmin.geometry.simplify(0.005)
gmn_geoPath = mapa_gmin.to_json()

column_dropdown = widgets.Dropdown(
    options=ceny_mieszkan_gus_gmin.columns[2:-2],
    value='2022',
    description='Select Column:',
    disabled=False
)

def update_map(column_name):
    mapa = folium.Map([52, 19], zoom_start=6)

    folium.Choropleth(
        geo_data=gmn_geoPath,
        data=ceny_mieszkan_gus_gmin,
        columns=['TERYT_gmin', column_name],
        key_on='feature.properties.JPT_KOD_JE',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f'Cena za 1 m2 lokalu ({column_name}r.)'
    ).add_to(mapa)

    mapa.save(outfile='ceny_mieszkan.html')

widgets.interactive(update_map, column_name=column_dropdown)

display(column_dropdown)