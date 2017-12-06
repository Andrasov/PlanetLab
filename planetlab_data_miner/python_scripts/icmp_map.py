import folium
import csv
from folium.plugins import MarkerCluster

map_icmp = folium.Map(location=[45.372, -121.6972],
                   zoom_start=12,
                   tiles='Boxlite')



with open('python_scripts/base_data.txt') as tsv:
 for row in csv.reader(tsv, delimiter='\t'):
  name = row[0]
  x = row[1]
  y = row[2]
  print(" %s " % (name))
  folium.Marker([x, y], popup=name).add_to(map_icmp)


map_icmp.save('map_icmp.html')