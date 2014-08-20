from ftplib import FTP
from urllib2 import Request, urlopen
from os.path import isdir, isfile
from os import mkdir
import urllib
from utils import state_codes
import re


def download_state_shapes(outdir='shapefiles'):
    return download_shapefiles_from_census(type='STATE', outprefix='state', outdir=outdir)


def download_city_shapes(outdir='shapefiles'):
    return download_shapefiles_from_census(type='PLACE', outprefix='city', outdir=outdir)


def download_zip_shapes(outdir='shapefiles'):
    return download_shapefiles_from_census(type='ZCTA5', outprefix='zip', outdir=outdir)


# type should be one of PLACE, STATE, or ZCTA5
def download_shapefiles_from_census(type, outprefix, outdir='shapefiles'):
    if not isdir(outdir):
        mkdir(outdir)

    census = FTP('ftp2.census.gov')
    print "Acquiring connection to census.gov"
    census.login()
    print "Connected!"
    filenames = census.nlst('geo/tiger/TIGER2013/%s' % type)

    for ftp_filename in filenames:
        zip_filename = re.match('.*/(.*\.zip)', ftp_filename).group(1)
        zip_filepath = '%s/%s%s' % (outdir, outprefix, zip_filename)

        if not isfile(zip_filepath):
            print 'Downloading %s' % zip_filename
            req = Request('ftp://ftp2.census.gov/%s' % ftp_filename)
            res = urlopen(req)
            with open(zip_filepath, 'a') as out:
                out.write(res.read())
        else:
            print '%s already exists. Skipping download' % zip_filepath

    census.close()

    return outdir


def download_neighborhood_shapes(outdir='shapefiles', outprefix='neighborhood'):
    url_template = 'http://www.zillow.com/static/shp/ZillowNeighborhoods-%s.zip'

    if not isdir(outdir):
        mkdir(outdir)

    f = urllib.URLopener()
    for code in state_codes:
        state = state_codes[code]
        try:
            filename = '%s/%s%s.zip' % (outdir, outprefix, state)
            if isfile(filename):
                print "%s already exists. Skipping..." % filename
                continue
            url = url_template % state
            f.retrieve(url, filename)
        except IOError:
            print "Error retrieving zip file: %s" % (url_template % state)

    return outdir
