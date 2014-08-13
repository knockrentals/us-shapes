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

class ESIndexer():
	def __init__(self, args):
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
		self.client = client = ES(eshost)

		mapper = ESMapper(client)
		indexer = Indexer(client)
		builder = Builder()

		self.shapes_index = 'shapes'
		self.suggest_index = 'suggestions'

		self.initialize_mappings(mapper)

		self.index_shapes(builder, indexer)
		self.index_suggestions(builder, indexer)


	def initialize_mappings(self, mapper):
		# Create indices and put mappings

		print 'Creating indices'
		mapper.create_indices(indices=[self.shapes_index, self.suggest_index])
		mapper.put_shapes_mappings(index=self.shapes_index)
		mapper.put_suggestions_mappings(index=self.suggest_index)


	def index_shapes(self, builder, indexer):
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
		indexer.bulk_index(self.shapes_index, 'neighborhood', neighborhood_shapes_file)
		indexer.bulk_index(self.shapes_index, 'city', city_shapes_file)
		indexer.bulk_index(self.shapes_index, 'state', state_shapes_file)
		indexer.bulk_index(self.shapes_index, 'zip', zip_shapes_file)

		chdir('..')


	def index_suggestions(self, builder, indexer):
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
		indexer.bulk_index(self.suggest_index, 'neighborhood', neighborhood_suggestions_file)
		indexer.bulk_index(self.suggest_index, 'city', city_suggestions_file)

		chdir('..')



if __name__ == "__main__":

   ESIndexer(sys.argv[1:])