
# coding: utf-8

# # Analysis

# ## Shape file and  district - POI file

# In[220]:


import pandas as pd
import matplotlib.pyplot as plt
import descartes
import geopandas as gpd
from shapely.geometry import Point, Polygon


# In[221]:


shape = gpd.read_file('poli_sociali.shp')
shape.head()


# In[222]:


fig, ax = plt.subplots(figsize = (10,10))
shape.plot(ax = ax)


# In[223]:


import pandas as pd
data = pd.read_csv('finale.csv')
data.head()


# In[224]:


# import fiona in order to check the crs of the two different dataset


# https://gis.stackexchange.com/questions/265589/change-shapefile-coordinate-system-using-python

# In[225]:


from pyproj import Proj, transform
import fiona
from fiona.crs import from_epsg

sh = fiona.open("poli_sociali.shp")


# In[226]:


original = Proj(sh.crs)
original


# In[227]:


# change data coordinate reference system from EPSG:4283 to EPSG:25832


# https://gis.stackexchange.com/questions/144061/convert-coordinates-to-differnt-spatial-reference-system-in-python

# In[228]:


import pyproj

lat_25832 = [0 for i in range(0,len(data))]
long_25832 = [0 for i in range(0,len(data))]
iniz = pyproj.Proj(init='epsg:4283')
final = pyproj.Proj(init='epsg:25832')

for i in range(0, len(data)):
    latitude, longitude = data['Lat'][i], data['Long'][i] 
    easting, northing = pyproj.transform(iniz, final, longitude, latitude)
    long_25832[i] = easting
    lat_25832[i] = northing


# In[229]:


data['lat_25832'] = lat_25832
data['long_25832'] = long_25832
data.head()


# In[230]:


Coords = [0 for i in range(0, len(data))]
for i in range(0, len(data)):
    Coords[i] = (data['long_25832'][i], data['lat_25832'][i])


# In[231]:


data['coords'] = Coords
data.head()


# ## Add district to data 

# In[232]:


import shapefile
from shapely.geometry import Point 
from shapely.geometry import shape 


# In[233]:


shp = shapefile.Reader('poli_sociali.shp') 
all_shapes = shp.shapes()
all_records = shp.records()


# In[234]:


quartiere = [0 for i in range(0, len(data))]
for i in range(0, len(all_shapes)):
    boundary = all_shapes[i] 
    for j in range(0, len(data)):
        point= data['coords'][j]
        if Point(point).within(shape(boundary)): 
            name = all_records[i][2] 
            quartiere[j] = name


# In[235]:


data['Quartiere'] = quartiere


# In[236]:


data.head()


# In[237]:


# filter for district that are in trento


# In[238]:


data['Quartiere'][84]


# In[239]:


poli_ok = data['Quartiere'] != 0


# In[240]:


dataset_per_scatter = data[poli_ok]


# In[241]:


dataset_per_scatter.head()


# In[242]:


geometry = [Point(xy) for xy in zip(dataset_per_scatter['long_25832'], dataset_per_scatter['lat_25832'])]
geometry[:3]


# In[243]:


crs = {'init':'epsg:25832'}
geo_df = gpd.GeoDataFrame(dataset_per_scatter, crs = crs, geometry = geometry)
geo_df


# In[244]:


print(len(geo_df))
print(len(dataset_per_scatter))


# In[245]:


poli = gpd.read_file('poli_sociali.shp')
poli.head()


# In[246]:


colori = {'Ristorante': 'navy',
          'Farmacia': 'black',
          'Tempo libero': 'cyan',
          'Hotels-camere': 'gold',
          'Parcheggio': 'forestgreen',
          'Sport': 'darkred',
          'Biblioteca': 'white',
         'Bar-vita notturna': 'silver',
          'Servizi': 'gray',
          'Alimentari': 'indigo',
          'Museo-monumento': 'chocolate',
          'Trasporti': 'orchid',
          'Others': 'dodgerblue',
          'Istituzioni':'olive',
          'Editoria': 'c',
          ' Trento': 'navy',
          'Universita_e_altro': 'tan'# errore nel riportare l'indirizzo di un ristorante
}


# In[274]:


fig,ax = plt.subplots(figsize = (30,30))
poli.plot(ax = ax, color = 'grey')
geo_df.plot(ax = ax, color = geo_df['Categorie'].apply(lambda x: colori[x]))
ax.set_title('Point of interest per Category - Scatter', fontdict = {'fontsize' : '50', 'fontweight' : '3'})
ax.annotate('Source: ISTAT, dati Trentino', xy = (0.6, 0.1), xycoords = 'figure fraction', fontsize = 20,
           color = '#555555')
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

red_patch = mpatches.Patch(color=
                           'navy',
          'black',
          'cyan',
          'gold',
          'forestgreen',
          'darkred',
          'white',
         'silver',
          'Servizi': 'gray',
          'Alimentari': 'indigo',
          'Museo-monumento': 'chocolate',
          'Trasporti': 'orchid',
          'Others': 'dodgerblue',
          'Istituzioni':'olive',
          'Editoria': 'c',
          ' Trento': 'navy',
          'Universita_e_altro': 'tan'
                           'red', label='The red data')
plt.legend(handles=[red_patch])

plt.show()
#ax.legend('Type of points:')


# In[275]:


fig.savefig('poi_trento.png')


# In[249]:


dataset_per_scatter.to_csv("dataset_quartiere.csv", index=False)


# ## Shapefile and district - Bus file 

# In[32]:


import pandas as pd
import matplotlib.pyplot as plt
import descartes
import geopandas as gpd
from shapely.geometry import Point, Polygon


# In[33]:


shape = gpd.read_file('poli_sociali.shp')
shape.head()


# In[34]:


bus_stop = pd.read_csv('stops.txt', sep=',')
bus_stop.head()


# In[35]:


# change EPSG from 4283 to 25832


# In[36]:


import pyproj

lat_25832 = [0 for i in range(0,len(bus_stop))]
long_25832 = [0 for i in range(0,len(bus_stop))]
iniz = pyproj.Proj(init='epsg:4283')
final = pyproj.Proj(init='epsg:25832')

for i in range(0, len(bus_stop)):
    latitude, longitude = bus_stop['stop_lat'][i], bus_stop['stop_lon'][i] 
    easting, northing = pyproj.transform(iniz, final, longitude, latitude)
    long_25832[i] = easting
    lat_25832[i] = northing


# In[37]:


bus_stop['lat_25832'] = lat_25832
bus_stop['long_25832'] = long_25832
bus_stop.head()


# In[38]:


Coords = [0 for i in range(0, len(bus_stop))]
for i in range(0, len(bus_stop)):
    Coords[i] = (bus_stop['long_25832'][i], bus_stop['lat_25832'][i])


# In[39]:


bus_stop['coords'] = Coords


# In[40]:


# add district column to the dataset


# In[41]:


import shapefile
from shapely.geometry import Point 
from shapely.geometry import shape


# In[42]:


shp = shapefile.Reader('poli_sociali.shp') 
all_shapes = shp.shapes()
all_records = shp.records()


# In[43]:


quartiere = [0 for i in range(0, len(bus_stop))]
for i in range(0, len(all_shapes)):
    boundary = all_shapes[i] 
    for j in range(0, len(bus_stop)):
        point= bus_stop['coords'][j]
        if Point(point).within(shape(boundary)): 
            name = all_records[i][2] 
            quartiere[j] = name


# In[44]:


bus_stop['Quartiere'] = quartiere


# In[45]:


# delete stops that are not in any district


# In[46]:


bus_ok = bus_stop['Quartiere'] != 0


# In[47]:


dataset_per_scatter = bus_stop[bus_ok]


# In[48]:


# create a geodf in order to plot the scatter on the shape of Trento


# In[49]:


geometry = [Point(xy) for xy in zip(dataset_per_scatter['long_25832'], dataset_per_scatter['lat_25832'])]
geometry[:3]


# In[50]:


crs = {'init':'epsg:25832'}
geo_df_bus = gpd.GeoDataFrame(dataset_per_scatter, crs = crs, geometry = geometry)
geo_df_bus


# In[51]:


poli = gpd.read_file('poli_sociali.shp')
poli.head()


# In[53]:


fig,ax = plt.subplots(figsize = (40,40))
poli.plot(ax = ax, color = 'grey')
geo_df.plot(ax = ax, color = 'darkred')
#fig.suptitle('Scatterplot - Stops in Trento', fontsize=20)
ax.set_title('Bus stops - Scatter', fontdict = {'fontsize' : '30', 'fontweight' : '3'})
ax.annotate('Source: ISTAT, Trentino Trasporti', xy = (0.65, 0.05), xycoords = 'figure fraction', fontsize = 14,
           color = '#555555')


# In[54]:


fig.savefig('bus_trento.png')


# In[55]:


dataset_per_scatter.to_csv("dataset_bus_quartiere.csv", index=False)


# # DataViz of the two joined dataset 

# In[163]:


import pandas as pd


# In[164]:


# upload data - poi


# In[165]:


data = pd.read_csv('dataset_quartiere.csv')
data.head()


# In[166]:


quartieri = []
for quartiere in data['Quartiere']:
    if quartiere not in quartieri:
        quartieri.append(quartiere)


# In[167]:


d = dict()
for quartiere in quartieri:
    d[quartiere] = 0


# In[168]:


for i in range(0, len(data)):
    quartiere = data['Quartiere'][i]
    for k in d:
        if quartiere == k:
            d[k] += 1
    i += 1


# In[169]:


d


# In[170]:


# upload data - bus


# In[171]:


bus = pd.read_csv('dataset_bus_quartiere.csv')
bus.head()


# In[172]:


quartieri_bus = []
for quartiere in bus['Quartiere']:
    if quartiere not in quartieri_bus:
        quartieri_bus.append(quartiere)


# In[173]:


d_bus = dict()
for quartiere in quartieri_bus:
    d_bus[quartiere] = 0


# In[174]:


for i in range(0, len(bus)):
    quartiere = bus['Quartiere'][i]
    for k in d_bus:
        if quartiere == k:
            d_bus[k] += 1
    i += 1


# In[175]:


d_bus


# In[176]:


# selecting only district with at least 10 punti di interesse


# In[177]:


d_lista_quartieri = dict()
for quartiere in d:
    if d[quartiere] >= 10:
        if quartiere not in d_lista_quartieri:
            d_lista_quartieri[quartiere] = d[quartiere]


# In[208]:


d_lista_quartieri


# In[178]:


bus_quartieri = dict()
for quartiere in d_lista_quartieri:
    bus_quartieri[quartiere] = d_bus[quartiere]


# In[211]:


bus_quartieri


# In[217]:


d_lista_morebus = dict()
for quartiere in d_bus:
    if d_bus[quartiere] >= 20:
        if quartiere not in d_lista_morebus:
            d_lista_morebus[quartiere] = d_bus[quartiere]


# In[218]:


d_lista_morebus


# In[179]:


import pandas as pd
import matplotlib.pyplot as plt
import descartes
import geopandas as gpd
from shapely.geometry import Point, Polygon


# In[180]:


shape = gpd.read_file('poli_sociali.shp')
shape


# In[181]:


index = []

for i in range(0, len(shape)):
    #print(shape['nome_quart'][i])
    if shape['nome_quart'][i] in d_lista_quartieri:
        index.append(i)
print(index)


# In[182]:


shape = shape.iloc[[1, 3, 5, 8, 12, 14, 23, 27, 39, 45, 47], :]


# In[183]:


shape.index = range(11)


# In[184]:


shape_tot = gpd.read_file('poli_sociali.shp')
shape_tot


# In[185]:


from matplotlib import colors

palette = dict()
for i in range(0, len(shape_tot)):
    stringa = shape_tot['nome_quart'][i]
    palette[stringa] = 'lime'


# In[186]:


for quartiere in palette:
    if quartiere not in bus_quartieri:
        palette[quartiere] = 'silver'


# ## POI 

# In[187]:


# create a new column (poi or False) according to the fact that that district is or not in the subset 


# In[188]:


bus_quartieri


# In[189]:


data['tipo'] = [0 for i in range(0, len(data))]
for i in range(0, len(data)):
    q = data['Quartiere'][i]
    if q in bus_quartieri:
        data['tipo'][i] = 'poi'
    else:
        data['tipo'][i] = 'FALSE'


# In[190]:


true = data['tipo'] == 'poi' 


# In[191]:


data.head()


# In[192]:


data_poi_quartieri = data[true]


# In[193]:


data_poi_quartieri_coord = data_poi_quartieri.iloc[:, [6,7,9,11]]


# In[194]:


data_poi_quartieri_coord.head()


# ## Bus

# In[195]:


# create a new column (poi or False) according to the fact that that district is or not in the subset 


# In[196]:


bus['tipo'] = [0 for i in range(0, len(bus))]
for i in range(0, len(bus)):
    q = bus['Quartiere'][i]
    if q in bus_quartieri:
        bus['tipo'][i] = 'bus'
    else:
        bus['tipo'][i] = 'FALSE'


# In[197]:


true = bus['tipo'] == 'bus' 


# In[198]:


data_bus_quartieri = bus[true]


# In[199]:


data_bus_quartieri_coord = data_bus_quartieri.iloc[:, [6,7,9,11]]


# In[200]:


frame =[data_poi_quartieri_coord, data_bus_quartieri_coord]


# In[201]:


result = pd.concat(frame)


# In[202]:


# creation of a geodf from union of datasets


# In[203]:


geometry = [Point(xy) for xy in zip(result['long_25832'], result['lat_25832'])]
geometry[:3]


# In[204]:


crs = {'init':'epsg:25832'}
geo_df = gpd.GeoDataFrame(result, crs = crs, geometry = geometry)
geo_df


# In[205]:


poli = gpd.read_file('poli_sociali.shp')
poli.head()


# In[206]:


colori = {'poi': 'darkred',
          'bus': 'dodgerblue'
}


# In[207]:


fig,ax = plt.subplots(figsize = (40,40))
poli.plot(ax = ax, color = 'silver')
geo_df.plot(ax = ax, color = geo_df['tipo'].apply(lambda x: colori[x]))


# In[ ]:


fig.savefig('BUS_VS_POI_quartieri.png')


# In[ ]:


# scatter on the entire sum of points and buses


# In[276]:


data = pd.read_csv('dataset_quartiere.csv')
data['tipo'] = ['poi' for i in range(0,len(data))]
data.head()


# In[277]:


bus = pd.read_csv('dataset_bus_quartiere.csv')
bus['tipo'] = ['bus' for i in range(0, len(bus))]
bus.head()


# In[294]:


data_poi = data.iloc[:, [6,7,9,11]]


# In[295]:


data_bus = bus.iloc[:, [8,9,11,13]]


# In[280]:


frame = [data_poi, data_bus]


# In[281]:


final_total = pd.concat(frame)


# In[282]:


final_total


# In[283]:


# geodf to plot the scatter


# In[284]:


geometry = [Point(xy) for xy in zip(final_total['long_25832'], final_total['lat_25832'])]
geometry[:3]


# In[299]:


geometry_2 = [Point(xy) for xy in zip(data_poi['long_25832'], data_poi['lat_25832'])]


# In[300]:


geometry_3 = [Point(xy) for xy in zip(data_bus['long_25832'], data_bus['lat_25832'])]


# In[285]:


crs = {'init':'epsg:25832'}
geo_df_final = gpd.GeoDataFrame(final_total, crs = crs, geometry = geometry)
geo_df_final.head()


# In[301]:


crs = {'init':'epsg:25832'}
geo_df_poi = gpd.GeoDataFrame(data_poi, crs = crs, geometry = geometry_2)


# In[302]:


crs = {'init':'epsg:25832'}
geo_df_bus = gpd.GeoDataFrame(data_bus, crs = crs, geometry = geometry_3)


# In[286]:


colori = {'poi': 'darkred',
          'bus': 'dodgerblue'
}


# In[317]:


fig,ax = plt.subplots(figsize = (30,30))
poli.plot(ax = ax, color = 'grey')
geo_df_poi.plot(ax = ax, 
                  color = 'darkred')
geo_df_bus.plot(ax = ax, 
                  color = 'dodgerblue')
ax.set_title('Bus stops and POIs - Scatter', fontdict = {'fontsize' : '50', 'fontweight' : '3'})
ax.annotate('Source: ISTAT, Trentino Trasporti, Dati Trentino', xy = (0.50, 0.1), xycoords = 'figure fraction', fontsize = 25,
           color = '#555555')

plt.legend( 
           ['POIs', 'Bus Stops'],  
           frameon=True,                                   # legend border
           framealpha=1,                                   # transparency of border
           ncol=2,                                         # num columns
           shadow=True,                                    # shadow on
           borderpad=1,                                    # thickness of border
           title='',
fontsize = 24)                      # title


# In[318]:


fig.savefig('BUS_VS_POI_total.png')


# # GTFS Analysis 

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
import geopandas as gpd
import os
import requests
import zipfile
from shapely.geometry import Point, LineString, Polygon
import shapely
import folium


# In[ ]:


gtfdir='gtfs'
zipfilegtfs = 'google_transit_urbano_tte.zip'
urlzip = 'https://www.trentinotrasporti.it/opendata/google_transit_urbano_tte.zip'


# In[ ]:


if not os.path.exists(gtfdir):
    os.mkdir(gtfdir)


# In[ ]:


r = requests.get(urlzip,allow_redirects=True)
open(zipfilegtfs, 'wb').write(r.content)


# In[ ]:


with zipfile.ZipFile(zipfilegtfs,"r") as zip_ref:
    zip_ref.extractall(gtfdir)


# In[ ]:


# shape file 


# In[ ]:


comuni_italiani = gpd.read_file("Com01012019_WGS84.shp",driver="ESRI Shapefile")


# In[ ]:


listacomuni=["Trento"]


# In[ ]:


trento = comuni_italiani[comuni_italiani.COMUNE=='Trento']


# In[ ]:


comuni_italiani.crs


# In[ ]:


area = trento.geometry
id = int(trento.index[0])
area = area[id]


# In[ ]:


# import GTFS


# In[ ]:


stops = pd.read_csv(gtfdir + os.sep + 'stops.txt')
stop_times = pd.read_csv(gtfdir + os.sep + "stop_times.txt")
trips = pd.read_csv(gtfdir + os.sep + "trips.txt")
routes = pd.read_csv(gtfdir + os.sep + "routes.txt")
agency = pd.read_csv(gtfdir + os.sep + "agency.txt")
shapes = pd.read_csv(gtfdir + os.sep + "shapes.txt")
calendar = pd.read_csv(gtfdir + os.sep + 'calendar.txt')
calendar_dates = pd.read_csv(gtfdir + os.sep + "calendar_dates.txt")
transfers = pd.read_csv(gtfdir + os.sep + "transfers.txt")


# In[ ]:


geometry = [Point(xy) for xy in zip(stops.stop_lon, stops.stop_lat)]
crs = {'init': 'epsg:4326'}
stops = gpd.GeoDataFrame(stops, crs=crs, geometry=geometry)


# In[ ]:


# list for stops that are in trento


# In[ ]:


results = []
for index, row in stops.to_crs(comuni_italiani.crs).iterrows():
    if (area.contains(row.geometry)):
        results.append(index)


# In[ ]:


stops_trento = stops[stops.index.isin(results)]


# In[ ]:


# network representation of fluxes - bus


# In[ ]:


stopids = list(stops_trento.stop_id.values)


# In[ ]:


stop_times_trento = stop_times[stop_times.stop_id.isin(stopids)]


# In[ ]:


stop_id_trento = list(stop_times_trento.stop_id.unique())


# In[ ]:


stops_trento_area = stops[stops.stop_id.isin(stop_id_trento)]


# In[ ]:


stop_times_trento.to_csv("stop_times.txt",index=False)


# In[ ]:


stops_trento_area.drop(columns=['geometry']).to_csv('stops.txt',index=False)


# In[ ]:


tripids = list(stop_times_trento.trip_id.unique())


# In[ ]:


trips_trento = trips[trips.trip_id.isin(tripids)]


# In[ ]:


routeids = list(trips_trento.route_id.unique())
routes_trento = routes[routes.route_id.isin(routeids)]
agencyids = list(routes_trento.agency_id.unique())
agency_trento = agency[agency.isin(agencyids)]
shapeids = list(trips_trento.shape_id.unique())
shapes_trento = shapes[shapes.shape_id.isin(shapeids)]
transfers_trento=transfers[transfers.from_stop_id.isin(stopids)]
transfers_trento=transfers[transfers.to_stop_id.isin(stopids)]


# In[ ]:


routes_trento.to_csv('routes.txt',index=False)
trips_trento.to_csv("trips.txt",index=False)
shapes_trento.to_csv('shapes.txt',index=False)
agency.to_csv('agency.txt',index=False)
calendar.to_csv('calendar.txt',index=False)
calendar_dates.to_csv('calendar_dates.txt',index=False)


# In[ ]:


# creation of a zip file


# In[ ]:


gtfs_trento = 'gtfs_trento.zip'


# In[ ]:


zf = zipfile.ZipFile(gtfs_trento, mode='w')
try:
    zf.write('routes.txt')
    zf.write('trips.txt')
    zf.write('shapes.txt')
    zf.write('agency.txt')
    zf.write('calendar.txt')
    zf.write('calendar_dates.txt')
    zf.write('stops.txt')
    zf.write('stop_times.txt')
finally:
    zf.close()


# In[ ]:


import networkx as nx
import osmnx as ox
import numpy as np
import peartree as pt


# In[ ]:


path="gtfs_trento.zip"


# In[ ]:


feed = pt.get_representative_feed(path)


# In[ ]:


start = 3*60*60  # 3:00
end = 24*60*60  # 24:00
G = pt.load_feed_as_graph(feed, start, end)


# In[ ]:


pt.generate_plot(G)


# # Heat map of POIs

# In[ ]:


import gmaps
import gmaps.datasets
import pandas as pd

gmaps.configure(api_key='AIzaSyAx7KM1GP_oShgvkuIqNksBVAVRO8so_is') 


# In[ ]:


poi_df = pd.read_csv("finale.csv")
poi_df.head()


# In[ ]:


locations = poi_df[['Lat', 'Long']]
fig = gmaps.figure(center=(46.065, 11.12), zoom_level=11)
fig.add_layer(gmaps.heatmap_layer(locations))
fig


# # Dataset for regression

# In[ ]:


import pandas as pd


# In[ ]:


# count poi for each district and for different categories


# In[ ]:


data = pd.read_csv('dataset_quartiere.csv')
data.head()


# In[ ]:


d = dict()
for i in range(0, len(data)):
    quartiere = data['Quartiere'][i]
    categoria = data['Categorie'][i]
    if quartiere not in d:
        d[quartiere] = dict()
        d[quartiere][categoria] = 1
    else:
        if categoria in d[quartiere]:
            d[quartiere][categoria] += 1
        else:
            d[quartiere][categoria] = 1


# In[ ]:


# count bus stops for each district


# In[ ]:


bus = pd.read_csv('dataset_bus_quartiere.csv')
bus.head()


# In[ ]:


quartieri_bus = []
for quartiere in bus['Quartiere']:
    if quartiere not in quartieri_bus:
        quartieri_bus.append(quartiere)


# In[ ]:


d_bus = dict()
for quartiere in quartieri_bus:
    d_bus[quartiere] = 0


# In[ ]:


for i in range(0, len(bus)):
    quartiere = bus['Quartiere'][i]
    for k in d_bus:
        if quartiere == k:
            d_bus[k] += 1
    i += 1


# In[ ]:


sortedDict = dict(sorted(d_bus.items(), key=lambda x: x[0].lower()) )


# In[ ]:


# pd.dataset 


# In[ ]:


df = pd.DataFrame(list(d_bus.items()), columns=['Quartiere', 'n_fermate'])


# In[ ]:


df['n_poi'] = [0 for i in range (0, len(df))] 


# In[ ]:


for i in range(0, len(data)):
    quartiere = data['Quartiere'][i]
    for j in range (0, len(df)):
        if quartiere == df['Quartiere'][j]:
            df['n_poi'][j] += 1
            j += 1


# In[ ]:


categorie = []
for categoria in data['Categorie']:
    if categoria not in categorie:
        categorie.append(categoria)


# In[ ]:


for categoria in categorie:
    df[categoria] = [0 for i in range(0,len(df))]


# In[ ]:


# filling categories with proper values


# In[ ]:


for i in range(0, len(df)):
    q = df['Quartiere'][i]
    for quartiere in d:
        if quartiere == q:
            for categoria in d[quartiere]:
                df[categoria][i] = d[quartiere][categoria]
    i+=1 


# In[ ]:


df['Ristorante'][22] += 1


# In[ ]:


del df[' Trento']


# In[ ]:


df.head()


# In[ ]:


df.to_csv('quartieri_e_numari.csv', index=False)

