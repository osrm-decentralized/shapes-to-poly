#!/usr/bin/env python
# coding: utf-8

# In[15]:


import geopandas as gpd
import shapely.geometry
import os
# dependency to install:
# pip install descartes


# In[16]:


states_shapefile = 'states-shapefile-orig/IND_adm1.shp'
polyFolder = 'states_poly'

buffer_kms = 50
simplification_factor = 5000


# In[20]:


os.makedirs(polyFolder, exist_ok=True)


# In[3]:


gdf = gpd.read_file(states_shapefile)


# ### convert CRS to 7755 (india meters)

# In[4]:


gdf2 = gdf.to_crs('EPSG:7755')


# In[5]:


del gdf


# In[6]:


gdf3 = gdf2.copy()
gdf3.geometry = gdf3.geometry.buffer(buffer_kms*1000).simplify(5000, preserve_topology=True)


# In[7]:


del gdf2


# In[9]:


gdf4 = gdf3.to_crs('EPSG:4326')


# In[11]:


del gdf3


# In[12]:


def pgon2poly(p,name):
    content = name
    for coord in p.exterior.coords:
        content += '\n    {:e}    {:e}'.format(coord[0],coord[1])
    content += '\nEND'
    return content


# In[19]:


for i,row in gdf4.iterrows():
    name = row['NAME_1'].lower().replace(' ','_')
    print(name)
    if type(row.geometry) == shapely.geometry.multipolygon.MultiPolygon:
        content = name
        # print(row.geometry)
        for N,b in enumerate(row.geometry.geoms):
            content += '\n' + pgon2poly(b,'area_{}'.format(N+1))
        content += '\nEND'
    else:
        content = name
        content += '\n' + pgon2poly(row.geometry,'area_1')
        content += '\nEND'
    
    with open(os.path.join(polyFolder,'{}.poly'.format(name)),'w') as f:
        f.write(content)
    


# In[ ]:




