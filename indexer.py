from fileinput import input
from time import sleep
from pyes import ES
from pyes.exceptions import NoServerAvailable
import re


class Indexer:
    def __init__(self, client):
        self.client = client

    def bulk_index(self, index, type, shapefile, batch_mode=True, batch_index_limit=20, sleep_time=0.1):
        print 'Indexing [%s] docs into [%s] from %s' % (type, index, shapefile)

        self.client.bulk_size = batch_index_limit
        index_count = 0

        id_re = re.compile('^.*?"id"\s*:\s*"([^"]+)"')
        parens_re = re.compile('\(.*?\)')

        for line in input(shapefile):
            id = id_re.match(line).group(1)

            # cleanup any lines that contain parentheticals
            line = parens_re.sub('', line).strip()

            try:
                self.client.index(line, index, type, id, bulk=batch_mode)
            except UnicodeDecodeError as e:
                print "Error processing line with id %s: %s" % (id, e.message)
            except NoServerAvailable as e:
                print "The server failed to respond while indexing %s: [%s]. Sleeping 5 seconds and retrying..." % (id, e.message)
                sleep(5)
                try:
                    print "Retrying indexing of %s" % id
                    self.client.index(line, index, type, id, bulk=batch_mode)
                except NoServerAvailable as e:
                    print "Failed to reconnect again. Skipping indexing %s" % id

            index_count += 1
            if index_count % batch_index_limit == 0:
                print 'Indexing batch of %d, starting from %s' % (batch_index_limit, id)
                sleep(sleep_time)