import geopandas as gpd
import matplotlib.pyplot as plt

cities = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

fig, ax = plt.subplots(1, figsize=(10, 6))
world.plot(ax=ax, color='lightgray', edgecolor='black')
cities.plot(ax=ax, color='blue', marker='o', markersize=3)
ax.set_title('Mapa świata z miastami')
ax.set_axis_off()

plt.show()