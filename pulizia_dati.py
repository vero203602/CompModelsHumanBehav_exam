
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


data = pd.read_csv('poi.txt', sep=",")

# .txt retrieved form https://dati.trentino.it/dataset/poi-trento


# In[3]:


data.head()


# In[4]:


type(data)


# In[5]:


df = data.iloc[:, [0, 3, 4, 5, 6, 8]]


# In[6]:


df.head()


# In[7]:


df.columns


# In[8]:


df.columns = ['Nome', 'Cat', 'Lat', 'Long', 'Indirizzo', 'Citta']


# In[9]:


df.head()


# In[10]:


len(df)


# In[11]:


trento = df['Citta'] == 'Trento'


# In[12]:


poi_trento = df[trento]


# In[13]:


poi_trento.head()


# In[14]:


len(poi_trento)


# In[15]:


poi_trento.index = range(608)


# In[16]:


poi_trento.head()


# In[17]:


d = {'Bed & Breakfast':'Hotels-camere',
     'Museo': 'Museo-monumento',
    'Alimentari': 'Alimentari',
    'Bar': 'Bar-vita notturna',
    'Ristorante': 'Ristorante',
    'Scuola Sci': 'Sport',
    'Snow Park': 'Sport',
     'Autostazione': 'Trasporti',
     'Stazione dei Treni': 'Trasporti',
     'Piscina': 'Sport',
     'Banca- Bancomat-Cambiovaluta': 'Servizi',
     'Mercatini-Mercato': 'Tempo libero',
     'Centro Wellness': 'Tempo libero',
     'Stadio del ghiaccio': 'Sport',
     'Numeri utili': 'Servizi',
     'Istituzioni': 'Istituzioni',
     'Centro commerciale-Grande magazzino': 'Tempo libero',
     'Appartamento Vacanze': 'Hotels-camere',
     'Prodotti tipici': 'Alimentari',
     'Souvenir': 'Tempo libero',
     'Taxi': 'Trasporti',
     'Teatro': 'Tempo libero',
     'Hotel': 'Hotels-camere',
     'Editoria': 'Editoria',
     'Affitta Camere': 'Hotels-camere',
     'Discoteca': 'Bar-vita notturna',
     'Bus Navetta': 'Trasporti',
     'Biblioteca': 'Biblioteca',
     'Birreria-Pub': 'Bar-vita notturna',
     'Ufficio informazioni turistiche': 'Tempo libero',
     'Posta - Corrieri': 'Servizi',
     'Camping': 'Tempo libero',
     'Sede Trentino Trasporti': 'Trasporti',
     'Monumento': 'Museo-monumento',
     'Gelateria-Pasticceria': 'Bar-vita notturna',
     'Stadio': 'Tempo libero',
     'Parcheggio': 'Parcheggio',
     'Funivia': 'Trasporti',
     'Noleggio Sci': 'Sport',
     'Farmacia': 'Farmacia',
     'Rifugio': 'Hotels-camere',
     'Sport': 'Sport',
     'Residence': 'Hotels-camere',
     'Agriturismo': 'Ristorante',
    }


# In[18]:


column = []
for el in poi_trento['Cat']:
    cat = str(el)
    column.append(cat)

#print(column)


# In[19]:


column_macro = []
for el in column:
    if el in d:
        column_macro.append(d[el])
    else:
        column_macro.append('Others')


# In[20]:


print(len(column_macro))
print(len(poi_trento))


# In[21]:


poi_trento['Categorie'] = column_macro


# In[25]:


poi_trento.head()


# In[27]:


#poi_trento['Indirizzo'][585]


# In[28]:


for el in poi_trento['Indirizzo']:
    print(el)


# In[29]:


stringa = poi_trento['Indirizzo'][25]
stringa


# In[30]:


stringa = stringa[17:38]


# In[31]:


stringa


# In[32]:


poi_trento['Indirizzo'][25] = stringa


# In[33]:


poi_trento['Indirizzo'][25]


# In[34]:


print(poi_trento.loc[[111]])


# In[35]:


poi_trento['Indirizzo'][111] = 'Parcheggio Zuffo'


# In[36]:


poi_trento['Indirizzo'][111]


# In[37]:


for el in poi_trento['Indirizzo']:
    print(el)


# In[38]:


for i in range(0,608):
    stringa = str(poi_trento['Indirizzo'][i])
    if stringa.startswith(' ') and stringa.endswith(' '):
        while stringa.startswith(' ') or stringa.endswith(' '):
            if stringa.startswith(' ') and stringa.endswith(' '):
                stringa = stringa[1:(len(stringa)-2)]
            elif stringa.startswith(' '):
                stringa = stringa[1:(len(stringa)-1)]
            else:
                stringa = stringa[0:(len(stringa)-2)]
        else:
            poi_trento['Indirizzo'][i] = stringa
    elif stringa.endswith(' '):
        while stringa.endswith(' '):
            stringa = stringa[0:(len(stringa)-2)]
        else:
            poi_trento['Indirizzo'][i] = stringa
    elif stringa.startswith(' '):
        while stringa.startswith(' '):
            stringa = stringa[1:(len(stringa)-1)]
        else:
            poi_trento['Indirizzo'][i] = stringa
    else:
        poi_trento['Indirizzo'][i] = stringa


# In[44]:


for i in range(0,608):
    poi_trento['Indirizzo'][i] = str(poi_trento['Indirizzo'][i]+','+' '+'Trento')


# In[45]:


poi_trento.head()


# In[46]:


poi_trento_new = poi_trento.dropna()


# In[47]:


(len(poi_trento_new))


# In[48]:


poi_trento_new.index = range(len(poi_trento_new))


# In[49]:


nan_subset = poi_trento.loc[poi_trento['Lat'].isnull()]


# In[50]:


nan_subset.head()


# In[52]:


nan_subset.index = range(len(nan_subset))


# In[53]:


nan_subset


# In[54]:


from geopy.geocoders import Nominatim
geolocator = Nominatim()

# https://stackoverflow.com/questions/5807195/how-to-get-coordinates-of-address-from-python
# geopy

loc = []
lat_long = []
for i in range(0,len(nan_subset)):
    address = str(nan_subset['Indirizzo'][i])
    #print(stringa)
    location = geolocator.geocode(address, timeout=30)
    if location != None:
        loc.append(i)
        nan_subset['Lat'][i] = location.latitude
        nan_subset['Long'][i] = location.longitude        
        lat_long.append((location.latitude, location.longitude))
        print(loc)


# In[55]:


len(loc)


# In[56]:


final_subset = nan_subset.ix[loc]


# In[64]:


final_subset.index = range(201, (201+len(final_subset)))
final_subset


# In[ ]:


frame = [poi_trento_new, final_subset]


# In[68]:


pd.concat()


# ## Aggiunta di:
# - Università 
# - Studentati
# - Duomo 
# - Buonconsiglio
# - Mense

# In[69]:


import pandas as pd


# In[70]:


df = {'Nome': ['Duomo', 'Buonconsiglio', 'Lettere', 'Sociologia', 'Economia',
              ' Giurisprudenza', 'Povo0', 'Povo1', 'Povo2', 'Mesiano',
              'mensapovo0', 'mensapovo1', 'Mesiano','TommasoGar', '24Maggio', 
               'Unibar', 'barpovo1', 'barmesiano','Mayer', 'Sanbapolis'],
      
     'Cat': ['Mon', 'Mon', 'Istruzione','Istruzione','Istruzione',
             'Istruzione','Istruzione','Istruzione','Istruzione','Istruzione',
              'Mensa','Mensa','Mensa','Mensa','Mensa',
              'Bar-Mensa','Bar-Mensa','Bar-Mensa','Studentato', 'Studentato'
             ],
      
     'Lat':[46.040126, 46.04177 , 46.06743, 46.066644, 46.0656754,
           46.0667941, 46.0652636, 46.0680942, 46.068074, 46.0649417,
           46.0652636, 46.06685265, 46.0646684, 46.0669112, 46.064484, 
            46.0475038, 46.06685265, 46.0649417, 46.073312, 46.0454099 
           ],
      
     'Long': [11.071699, 11.07378, 11.1170248, 11.1196548, 11.1176028,
             11.1196178, 11.1505427, 11.149506220748833, 11.150227, 11.1420192,
             11.1505427, 11.149792443809915, 11.139110671241585, 11.1171988, 11.121250, 
              11.1334213, 11.149792443809915, 11.1420192, 11.118559, 11.1325263
             ],
      
     'Indirizzo': ['Piazza del Duomo, Trento', 
                   'Salita Sodegerio da Tito, Trento', 
                   'Via Tommaso Gar, 14, Trento',
                  'Via Giuseppe Verdi, 26, Trento', 
                   'Via Vigilio Inama, 5, Trento',
                  'Via Giuseppe Verdi, 53, Trento', 
                   'Via Sommarive, 14, Trento', 
                   'Via Sommarive, 9, Trento', 
                   'Polo Scientifico e Tecnologico Fabio Ferrari, Via Sommarive, 9, Trento', 
                   'Via Mesiano, 35, Trento',
                  'Via Sommarive, 14, Trento', 
                   'Via Sommarive, 5, Trento', 
                   'Via Mesiano, 77, Trento' , 
                   'Via Tommaso Gar, 18, Trento',
                   'Via XXIV Maggio, 15, Trento', 
                   'Via Sommarive, 5, Trento', 
                   'Via Mesiano, 20, Trento',
                   'Via della Malpensada, 140, Trento',
                   'piazzetta Valeria Solesin, 1, Trento', 
                   'Via della Malpensada, 80'],
      
     'Citta':['Trento','Trento','Trento','Trento','Trento',
             'Trento','Trento','Trento','Trento','Trento',
             'Trento','Trento','Trento','Trento','Trento',
             'Trento','Trento','Trento','Trento','Trento'], 
      
     'Categorie': ['Museo-monumento', 'Museo-monumento', 'Universita_e_altro', 
                   'Universita_e_altro', 'Universita_e_altro',
                   'Universita_e_altro', 'Universita_e_altro','Universita_e_altro', 'Universita_e_altro','Universita_e_altro',
                   'Universita_e_altro', 'Universita_e_altro','Universita_e_altro', 'Universita_e_altro','Universita_e_altro',
                  'Universita_e_altro','Universita_e_altro', 'Universita_e_altro',
                   'Universita_e_altro','Universita_e_altro'
                  ]
     }


# In[71]:


data = pd.DataFrame.from_dict(df)


# In[72]:


color = ['blue' for i in range(0, len(data))]


# In[73]:


data['Colori'] = color


# In[74]:


data.head()


# In[75]:


# carico il dataset finale per l'unione


# In[76]:


first = pd.read_csv('final_dataset.csv')


# In[77]:


first.head()


# In[78]:


data.head()


# In[79]:


data.index= range(488, 508)


# In[80]:


frame = [first, data] 


# In[81]:


final = pd.concat(frame)


# In[82]:


final.head()


# In[83]:


del final['Cat']


# In[84]:


del final['Colori']


# In[85]:


final.to_csv('finale.csv', index=False)


