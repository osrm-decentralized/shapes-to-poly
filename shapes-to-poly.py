#!/usr/bin/env python
# coding: utf-8

import geopandas as gpd
import shapely.geometry
import os
import time
import argparse

start = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("shape", help="filename or URL of shapefile to convert to .poly(s). Can be .geojson, .shp, .gpkg or any format supported by geopandas / fiona packages.", type=str)
parser.add_argument("-n", "--namingColumn", help="If there are multiple shapes, what is the unique field/column in the shapefile to name each .poly file by (default:will just name them shape_1.poly shape_2.poly etc", type=str, default='')
parser.add_argument("-b", "--buffer", help="buffer each shape by this many kms", type=float, default=0)
parser.add_argument("-s", "--simplification", help="simplification factor to reduce output filesize. Best used in conjunction with buffer. Typical values: for country-level: 5000", type=float, default=0)
parser.add_argument("-c", "--crs", help="CRS projection to use for kms calculations. Default: EPSG:7755 for India", type=str, default='EPSG:7755')
parser.add_argument("-l", "--layer", help="specify name of layer if loaded shapefile is multi-layered", type=str, default='')
parser.add_argument("-g", "--geojson", help="also create .geojson to preview", action="store_true")

args = parser.parse_args()

print(args.shape)

polyFolder = 'output'
os.makedirs(polyFolder, exist_ok=True)

#print('buffer kms:', args.buffer)
#simplification_factor = args.simplification or 0
#print('simplification factor:', args.simplification)

if(args.layer):
    gdf = gpd.read_file(args.shape, layer=args.layer)
else:
    gdf = gpd.read_file(args.shape)


# convert CRS to the CRS specified in options.. only if there is buffering or simplification involved
if args.buffer or args.simplification:
    gdf2 = gdf.to_crs(args.crs)

    del gdf

    gdf3 = gdf2.copy()

    if(args.buffer):
        gdf3.geometry = gdf3.geometry.buffer(args.buffer*1000)

    if(args.simplification):
        gdf3.geometry = gdf3.geometry.simplify(args.simplification, preserve_topology=True)

    del gdf2

    # convert back to lat-longs
    gdf4 = gdf3.to_crs('EPSG:4326')
    del gdf3

else: # skip CRS conversion if user didn't want to buffer or simplify
    gdf4 = gdf

    
# now main conversion to .poly

def pgon2poly(p,name):
    content = name
    for coord in p.exterior.coords:
        content += '\n    {:e}    {:e}'.format(coord[0],coord[1])
    content += '\nEND'
    return content


for i,row in gdf4.iterrows():
    if args.namingColumn:
        name = row[args.namingColumn].replace(' ','_')
    else:
        name = "shape_{}".format(i+1)
    print(i+1, name)
    if type(row.geometry) == shapely.geometry.multipolygon.MultiPolygon :
        content = name
        # print(row.geometry)
        for N,b in enumerate(row.geometry.geoms):
            content += '\n' + pgon2poly(b,'area_{}'.format(N+1))
        content += '\nEND'
    elif type(row.geometry) == shapely.geometry.polygon.Polygon :
        content = name
        content += '\n' + pgon2poly(row.geometry,'area_1')
        content += '\nEND'
    else:
        print("Cannot make .poly of a non-polygonal shape: {} . Skipping.".format(type(row.geometry)))
    
    with open(os.path.join(polyFolder,'{}.poly'.format(name)),'w') as f:
        f.write(content)

if args.geojson:
    gdf4.to_file(os.path.join(polyFolder,"{}.geojson".format(args.shape)), driver="GeoJSON")

end = time.time()    
print("Done! Check the output/ folder. Took {} secs".format(round(end-start,3)))

