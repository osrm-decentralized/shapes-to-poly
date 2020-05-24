# shapes-to-poly
python3 program that converts a each polygon/multipolygon in an input shapefile into a .poly file

> Where is a .poly used?  
> Mainly by osmconvert to clip out custom OSM .pbf data, and then to use the .pbf in routing applications like OSRM / OpenTripPlanner.
> See: https://wiki.openstreetmap.org/wiki/Osmconvert#Clipping_based_on_a_Polygon



## Usage
You can run `python3 shapes-to-poly.py -h` to display the same options documentation as below:
```
usage: shapes-to-poly.py [-h] [-n NAMINGCOLUMN] [-b BUFFER]
                         [-s SIMPLIFICATION] [-c CRS] [-l LAYER] [-g]
                         shape

positional arguments:
  shape                 filename or URL of shapefile to convert to .poly(s).
                        Can be .geojson, .shp, .gpkg or any format supported
                        by geopandas / fiona packages.

optional arguments:
  -h, --help            show this help message and exit
  -n NAMINGCOLUMN, --namingColumn NAMINGCOLUMN
                        If there are multiple shapes, what is the unique
                        field/column in the shapefile to name each .poly file
                        by (default:will just name them shape_1.poly
                        shape_2.poly etc
  -b BUFFER, --buffer BUFFER
                        buffer each shape by this many kms
  -s SIMPLIFICATION, --simplification SIMPLIFICATION
                        simplification factor to reduce output filesize. Best
                        used in conjunction with buffer. Typical values: for
                        country-level: 5000
  -c CRS, --crs CRS     CRS projection to use for kms calculations. Default:
                        EPSG:7755 for India
  -l LAYER, --layer LAYER
                        specify name of layer if loaded shapefile is multi-
                        layered
  -g, --geojson         also create .geojson to preview
```

## Sample commands

If you have a shape saved as a shape.geojson file:
```
python3 shapes-to-poly.py shape.geojson
```

Buffer by 50 km:
```
python3 shapes-to-poly.py -b 50 shape.geojson
```

Buffer by 50km, and simplify by a factor of 5000 (ok at country level):
```
python3 shapes-to-poly.py -b 50 -s 5000 shape.geojson
```

If you have a ESRI shapefile (sample.shp +) with multiple shapes and a column like "S_NAME" holding the name for each shape,
```
python3 shapes-to-poly.py -b 50 -s 5000 -n "S_NAME" sample.shp
```

If your shape is not in India and you want to apply a diffrent CRS for 100km buffering, for example: EPSG:1324 for USA:
```
python3 shapes-to-poly.py -c "EPSG:1324" -b 100 shape.geojson
```

## Features
- buffering : If you want to apply ex: 100 kms buffer to your shape before converting to .poly, use `-b 100`
- handles multi-polygons : The .poly output will also be multi-polygon. Just make sure to keep the shape(s) saved as a multi-polygon in your input file.
- simplification of geometry : Esp recommended in confunjction with buffering: It cuts down complexity for other processes downstream like osmconvert


## Installing requirements before running:
```
pip3 install geopandas
```

### Windows
Note: If on windows and using anaconda / miniconda, then conda is better than pip as it takes care of some GDAL dependencies:
```
conda insall geopandas
```

### Linux / Ubuntu
In linux/ubuntu, there can be extra dependencies of geopandas on GDAL. Here's one way to install them which worked for me:

```
sudo apt-get install python3-pip libgdal-dev locales build-essential python3-dev python3-setuptools python3-wheel
pip3 install GDAL==2.4.2
```

If the last line errored out, try this:
```
pip3 install GDAL=="`gdal-config --version`.*"
```

### Alternative ways
- See https://github.com/nextgis/pygdal

### Using Docker
Ensure that your shapefile is present in the same folder (or in a folder beneath)

Open a terminal/command prompt, navigate it to current folder, and run these commands if for the first time:
```
docker build -t shapes-to-poly1 .
docker run -v $(pwd):/app -it shapes-to-poly1
```
This gets you into a dockerised ubuntu shell with all dependencies installed, your current directory mounted in it. Practically speaking you haven't gone anywhere; the system with the dependencies installed has just momentarily come above. You can type the command `ls -l` to see and confirm that all your files are there. Check out the `Dockerfile` in this repo to see what's happening under the hood.  

You can now run the same python commands as given above. The outputs will be saved in a output/ folder in your current folder, and will stay even after you've exited the dockerised ubuntu shell.  

Once done, you can get out with the `exit` command.

To run this again, you won't need the "build" command unless you purge your local docker images:
```
docker run -v $(pwd):/app -it shapes-to-poly1
```
Shout-out to https://github.com/thinkWhere/GDAL-Docker for making a gdal-friendly docker container readily available.
