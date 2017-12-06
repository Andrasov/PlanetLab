import folium
import sys
import os

latitude=sys.argv[1]
longitude=sys.argv[2]
name=sys.argv[3]

map_1 = folium.Map(location=[latitude, longitude],
                   zoom_start=12,
                   tiles='Stamen Terrain')
folium.Marker([latitude, longitude], popup=name).add_to(map_1)

map_1.save('map_1.html')

sys.stdout = os.devnull
sys.stderr = os.devnull
