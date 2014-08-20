from os.path import isdir, isfile
from os import mkdir
from glob import glob
from shlex import split
from subprocess import check_output


class GeoJSONConverter:
    def to_geojson(self, raw_geofile, raw_geodir='geojson', shapefile_prefix='', shapefile_ext='zip',
                   shapefiles_dir='shapefiles'):
        if not isdir(raw_geodir):
            mkdir(raw_geodir)

        print "Converting files in %s matching %s*.%s into GeoJSON. Results stored in %s/%s" % (
        shapefiles_dir, shapefile_prefix, shapefile_ext, raw_geodir, raw_geofile)
        raw_geofilepath = '%s/%s' % (raw_geodir, raw_geofile)

        if isfile(raw_geofilepath):
            print "%s already exists. Skipping conversion..." % raw_geofilepath
            return raw_geofilepath

        with open(raw_geofilepath, 'a') as out:
            file_pattern = "%s/%s*.%s" % (shapefiles_dir, shapefile_prefix, shapefile_ext)
            files = glob(file_pattern)

            for filename in files:
                try:
                    print "Converting %s to GeoJSON" % filename
                    raw_command = r'curl -F "upload=@%s" localhost:3000/convert' % filename
                    command = split(raw_command)
                    converted = check_output(command)
                    out.write("%s" % converted)
                except IOError as e:
                    print "Error converting %s" % filename
                    print "I/O error({0}): {1}".format(e.errno, e.strerror)

        return raw_geofilepath