U.S. Shapes Indexer
=========
Retrieve, convert, and index shapefiles into Elasticsearch, and generate a suggestions index for those locations

# Install
Follow the instructions below for non-Python dependencies, then
```
pip install usshapes
```

# Usage
A runnable module is included that can be used to automate the process of indexing your data. This is the most likely way you want to use this package.

```
$ us-shapes.py [--es-host=] [--ogre-host=] [[--no-batch] | [--batch-size=]] [--excludes=] [--no-shapes] [--no-suggestions] [--sleep-time]
```

## Options:
* es-host: the elastic search host to use; default: localhost:9200
* ogre-host: the elastic search host to use; default: localhost:3000
* no-batch: turn off batch mode
* batch-size: how large should each batch be; default: 100
* excludes: comma-separated list of excluded types; possible types: 'neighborhood', 'city', 'state', 'zip'
* no-shapes: skip creation and indexing of shapes
* no-suggestions: skip creation and indexing of suggestions
* sleep-time: time to sleep between bulk index operations, in seconds; default: 0.1

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

### Gotcha! A note about ogre and Big Files
Some of the files downloaded from census.gov and zillow.com are Big Files. The zip archive containing the raw zip code shapefiles is half a gigabyte and it expands to a single GeoJSON file weighing in at around 1.5 GB. The ogre client currently does not accept a command line setting for adjusting the timeout used by the underlying ogr2ogr library to convert the shapefpiles to GeoJSON, and it's default timeout is 15 seconds. This is not enough time to convert these files. I've submitted a patch to the author of ogre that would allow setting a timeout, but until then, here's what you need to do:

Go to the ogre installation directory where you're running the ogre client from and open up ```index.js```. In the post route for /convert, there should be the following declaration:
```
var ogr = ogr2ogr(req.files.upload.path)
```

Change that to:
```
var ogr = ogr2ogr(req.files.upload.path).timeout(1000000000) # or whatever other suitably large timeout
```

That should take care of the timeout issues.

# Non-script Usage
If you elect to not use the script to automate the task (which I still think you should), the best current documentation for how to use the module is still looking at us-shapes.py and seeing how it operates. If there's any demand for proper docs, I'll write them up. Otherwise, I assume you're good.