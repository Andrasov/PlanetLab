import pandas as pd
from vincent import (Visualization, Scale, DataRef, Data, PropertySet,
                     Axis, ValueRef, MarkRef, MarkProperties, Mark)

import json
import folium
import csv

df = pd.DataFrame({'Data 1': [1, 2, 3, 4, 5, 6, 7, 12],
                   'Data 2': [42, 27, 52, 18, 61, 19, 62, 33]})

#Top level Visualization
vis = Visualization(width=500, height=300)
vis.padding = {'top': 10, 'left': 50, 'bottom': 50, 'right': 100}

#Data. We're going to key Data 2 on Data 1
vis.data.append(Data.from_pandas(df, columns=['Data 2'], key_on='Data 1', name='table'))

#Scales
vis.scales.append(Scale(name='x', type='ordinal', range='width',
                        domain=DataRef(data='table', field="data.idx")))
vis.scales.append(Scale(name='y', range='height', nice=True,
                        domain=DataRef(data='table', field="data.val")))

#Axes
vis.axes.extend([Axis(type='x', scale='x'), Axis(type='y', scale='y')])

#Marks
enter_props = PropertySet(x=ValueRef(scale='x', field="data.idx"),
                                     y=ValueRef(scale='y', field="data.val"),
                                     width=ValueRef(scale='x', band=True, offset=-1),
                                     y2=ValueRef(scale='y', value=0))
update_props = PropertySet(fill=ValueRef(value='steelblue'))
mark = Mark(type='rect', from_=MarkRef(data='table'),
            properties=MarkProperties(enter=enter_props,
            update=update_props))

vis.marks.append(mark)
vis.axis_titles(x='days', y='latency [ms]')
vis.to_json('vega.json')



map_full = folium.Map(
    [46.3014, -123.7390],
    zoom_start=2,
    tiles='Stamen Terrain'
    )

map_full = folium.Map(location=[45.372, -121.6972],
                   zoom_start=2,
                   tiles='Stamen Terrain')



with open('python_scripts/base_data.txt') as tsv:
 for row in csv.reader(tsv, delimiter='\t'):
  name = row[0]
  x = row[1]
  y = row[2]
  print(" %s " % (name))
  folium.Marker(
    [x, y],
    popup=folium.Popup(max_width=600).add_child(
        folium.Vega(json.load(open('vega.json')), width=700, height=400))
    ).add_to(map_full)


map_full.save('map_full.html')