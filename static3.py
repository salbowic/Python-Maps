import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from geopy.distance import geodesic


def main():
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())
    ax.set_global()
    ax.stock_img()
    ax.coastlines()

    warsaw_coords = [21.00, 52.15]
    new_york_coords = [-74.00, 40.42]

    distance_geodetic = geodesic(warsaw_coords, new_york_coords).kilometers

    distance_text = f"{distance_geodetic:.2f} km"

    ax.plot(warsaw_coords[0], warsaw_coords[1], 'o', color='green', transform=ccrs.PlateCarree(), label='Warszawa')
    ax.plot(new_york_coords[0], new_york_coords[1], 'o', color='blue', transform=ccrs.PlateCarree(), label='Nowy Jork')

    ax.plot([warsaw_coords[0], new_york_coords[0]], [warsaw_coords[1], new_york_coords[1]], color='red', linestyle='--', linewidth=2, transform=ccrs.PlateCarree())
    ax.plot([warsaw_coords[0], new_york_coords[0]], [warsaw_coords[1], new_york_coords[1]], color='red', transform=ccrs.Geodetic(), label=f'Odległość ({distance_text})')

    ax.legend(loc='lower right')

    plt.show()

if __name__ == '__main__':
    main()
