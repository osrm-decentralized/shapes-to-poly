FROM thinkwhere/gdal-python:3.7-ubuntu

RUN pip3 install geopandas

RUN mkdir -p /app
WORKDIR /app
