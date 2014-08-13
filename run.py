#!/usr/bin/python

from os.path import isfile, isdir
from os import mkdir, chdir
from mapper import ESMapper
from subprocess import call
from fileinput import input
from time import sleep
from indexer import Indexer
from pyes import ES
from builder import Builder
import sys, getopt

def main(args):
	host = 'localhost'
	port = '9200'

	try:
	  opts, args = getopt.getopt(args,"h:p:")
	except getopt.GetoptError:
	  print 'run.py -h <host> -p <port>'
	  sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			host = arg
		elif opt == '-p':
			port = arg

	eshost = '%s:%s' % (host, port)
	client = ES(eshost)

	mapper = ESMapper(client)
	indexer = Indexer(client)
	builder = Builder()

	initialize_mappings(mapper)

	index_shapes(builder, indexer)
	index_suggestions(builder, indexer)


def initialize_mappings(mapper):
	# Create indices and put mappings
	
	shapes_index = 'shapes'
	suggest_index = 'suggestions'

	print 'Creating indices'
	mapper.create_indices(indices=[shapes_index, suggest_index])
	mapper.put_shapes_mappings(index=shapes_index)
	mapper.put_suggestions_mappings(index=suggest_index)


def index_shapes(builder, indexer):
	# Download and format shapefiles, if they don't exist

	shapes_dir = 'shapes'
	neighborhood_shapes_file = 'shapes_neighborhood.json'
	city_shapes_file = 'shapes_city.json'
	state_shapes_file = 'shapes_state.json'
	zip_shapes_file = 'shapes_zip.json'

	if not isdir(shapes_dir):
		mkdir(shapes_dir)

	chdir(shapes_dir)

	if not isfile(neighborhood_shapes_file):
		builder.build_neighborhood_shapes(outfile=neighborhood_shapes_file)
	if not isfile(city_shapes_file):
		builder.build_city_shapes(outfile=city_shapes_file)
	if not isfile(state_shapes_file):
		builder.build_state_shapes(outfile=state_shapes_file)

	# Index shapes
	indexer.bulk_index(shapes_index, 'neighborhood', neighborhood_shapes_file)
	indexer.bulk_index(shapes_index, 'city', city_shapes_file)
	indexer.bulk_index(shapes_index, 'state', state_shapes_file)
	indexer.bulk_index(shapes_index, 'zip', zip_shapes_file)

	chdir('..')


def index_suggestions(builder, indexer):
	# Generate suggestion files, if they don't exist

	suggestions_dir = 'suggestions'
	neighborhood_suggestions_file = 'suggestions_neighborhood.json'
	city_suggestions_file = 'suggestions_city.json'

	if not isdir(suggestions_dir):
		mkdir(suggestions_dir)

	chdir(suggestions_dir)

	if not isfile(neighborhood_suggestions_file):
		print 'Building neighborhood suggestions file'
		neighborhood_geofile = '../%s/%s' % (shapes_dir, neighborhood_shapes_file)
		builder.build_neighborhood_suggestions(outfile=neighborhood_suggestions_file, neighborhood_geofile=neighborhood_geofile)
	if not isfile(city_suggestions_file):
		city_geofile = '../%s/%s' % (shapes_dir, city_shapes_file)
		builder.build_city_suggestions(outfile=city_suggestions_file, city_geofile=city_geofile)

	# Index suggestions
	indexer.bulk_index(suggest_index, 'neighborhood', neighborhood_suggestions_file)
	indexer.bulk_index(suggest_index, 'city', city_suggestions_file)

	chdir('..')



if __name__ == "__main__":
   main(sys.argv[1:])