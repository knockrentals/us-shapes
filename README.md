U.S. Shapes Indexer
=========
Retrieve, convert, and index shapefiles (and suggestions based on those files) from census.gov and Zillow

# Usage
```bash
run.py [-h <elasticsearch-host>]  [-p <elasticsearch-port>] [--use-online-ogre]
```

# Dependencies:
* [Elasticsearch](http://www.elasticsearch.org)
* [pyes](https://pyes.readthedocs.org/en/latest)
* [ogre](https://github.com/wavded/ogre) (Optional. See below)
* [GDAL](http://www.gdal.org/index.html) (Optional. See below)


# How to install Elasticsearch
```
Read the docs, yo
```

# How to install pyes
```
pip install pyes
```

# ogre and GDAL
ESIndexer needs these libraries for converting shapefiles to GeoJSON files.
However, there is an [ogre instance](http://ogre.adc4gis.com) available online that will
obviate the need for a local install of these libraries. The problem with that option, though,
is that converting large shapefiles will be a very slow process, and you might even bring down
their server.

It is recommended that you install these libraries locally.
