import plotly.express as px
import geopandas as gpd

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))


world = world.to_crs('+proj=moll +lon_0=0 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs')


world['area_km2'] = world['geometry'].area / 1e6

world['pop_density'] = world['pop_est'] / world['area_km2']

print(world)
fig = px.choropleth(world, 
                    locations='iso_a3', 
                    color='pop_density', 
                    hover_name='name',
                    hover_data={'pop_density': ':,.2f', 'pop_est': ':,.0f', 'area_km2': ':,.2f'},
                    projection='orthographic',
                    color_continuous_scale='SunsetDark',
                    title='Interactive 3D Globe with Population Density')


fig.update_geos(showcoastlines=True)
fig.update_layout(geo=dict(projection_type="orthographic", landcolor="darkgray", oceancolor="blue"))


fig.update_layout(coloraxis_colorbar=dict(title='Gęstość zaludnienia'))

fig.update_traces(hoverlabel=dict(namelength=-1))

fig.update_layout(title='Interaktywna mapa 3D')

fig.show()
