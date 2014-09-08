U.S. Shapes Indexer
=========
Retrieve, convert, and index shapefiles (and suggestions based on those files) from census.gov and Zillow

# Usage
```
$ run.py [--es-host=] [--ogre-host=] [[--no-batch] | [--batch-size=]] [--excludes=] [--no-shapes] [--no-suggestions]
```

## Options:
* es-host: the elastic search host to use; default: localhost:9200
* ogre-host: the elastic search host to use; default: localhost:3000
* no-batch: turn off batch mode
* batch-size: how large should each batch be; default: 100
* excludes: comma-separated list of excluded types; possible types: 'neighborhood', 'city', 'state', 'zip'
* no-shapes: skip creation and indexing of shapes
* no-suggestions: skip creation and indexing of suggestions

# Dependencies:
* [Elasticsearch](http://www.elasticsearch.org)
* [pyes](https://pyes.readthedocs.org/en/latest)
* [ogre](https://github.com/wavded/ogre) (Optional. See below)
* [GDAL](http://www.gdal.org/index.html) (Optional. See below)

If you want to use virtualenv:
```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

# How to install Elasticsearch
```
Read the docs, yo
```

# How to install dependencies
```
pip install -r requirements.txt
```

# ogre and GDAL
ESIndexer needs these libraries for converting shapefiles to GeoJSON files.
However, there is an [ogre instance](http://ogre.adc4gis.com/convert) available online that will
obviate the need for a local install of these libraries. The problem with that option, though,
is that converting large shapefiles will be a very slow process, and you might even bring down
their server.

It is recommended that you install these libraries locally.

```
git@github.com:wavded/ogre.git
./bin/ogre.js -p 3000
```

Or install globally:
```
npm install -g ogre
ogre -p 3000
```
