from fileinput import input
from time import sleep
from pyes import ES
import re

class Indexer:
	def __init__(self, client):
		self.client = client

	def bulk_index(self, index, type, shapefile, bulk_index_limit=400, sleep_time=1):
		print 'Indexing [%s] docs into [%s] from %s' % (type, index, shapefile)

		self.client.bulk_size = bulk_index_limit
		index_count = 0

		id_re = re.compile('^.*?"id"\s*:\s*"([^"]+)"')
		parens_re = re.compile('\(.*?\)')

		for line in input(shapefile):
			id = id_re.match(line).group(1)

			# cleanup any lines that contain parentheticals
			line = parens_re.sub('',line).strip()

			try:
				self.client.index(line, index, type, id, bulk=True)
			except UnicodeDecodeError as e:
				print "Error processing line with id %s: %s" % (id, e)
			
			index_count += 1
			if index_count % bulk_index_limit == 0:
				print 'Indexing batch of %d, starting from %s' % (bulk_index_limit, id)
				sleep(sleep_time)