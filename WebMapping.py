# Eline van Elburg
# Web Mapping demo
# 21-01-2016

# Imports
import geocoder
import osgeo.ogr, osgeo.osr
import time

# Functions
def read_file(filename):
    myFile = open(filename, 'r')
    string = myFile.read()
    myFile.close()
    return string

def split_string(string):
    myList = string.split(',')
    return myList

def get_location(city):
    g = geocoder.google(city)
    latlong = g.latlng
    return latlong

def make_shp(locationList, fileName):
    # Set spatial reference
    spatialReference = osgeo.osr.SpatialReference()
    spatialReference.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')

    # Create shapefile
    driver = osgeo.ogr.GetDriverByName('ESRI Shapefile')
    shapeData = driver.CreateDataSource(fileName)

    # Create Layer
    layer = shapeData.CreateLayer('cities', spatialReference, osgeo.ogr.wkbPoint)
    layerDefinition = layer.GetLayerDefn()

    # Create Name field
    fid_field = osgeo.ogr.FieldDefn("FID", osgeo.ogr.OFTInteger)
    name_field = osgeo.ogr.FieldDefn("PlaceNames", osgeo.ogr.OFTString)
    name_field.SetWidth(30)
    layer.CreateField(fid_field)
    layer.CreateField(name_field)

    # Create Points
    i = 1
    for city_loc in locationList:
        city = city_loc[0]
        coords = city_loc[1]
        # Create point
        geometry = osgeo.ogr.Geometry(osgeo.ogr.wkbPoint)
        geometry.SetPoint(0, coords[1], coords[0])
        # Create feature
        feature = osgeo.ogr.Feature(layerDefinition)
        feature.SetGeometry(geometry)
        feature.SetField("FID",i)
        feature.SetField("PlaceNames",city)
        # Save feature
        layer.CreateFeature(feature)
        # Cleanup
        geometry.Destroy()
        feature.Destroy()
        i += 1
    # Cleanup
    shapeData.Destroy()
        
# Main code
string_cities = read_file("/home/eline/Documents/Python/Projects/Web_Mapping/WebMapping/cities.txt")
list_cities = split_string(string_cities)

location_list = []
for city in list_cities:
    location = get_location(city)
    location_list.append([city,location])

shp_filename = '/home/eline/Documents/Python/Projects/Web_Mapping/WebMapping/Shapefiles/CityLocation_' + time.strftime('%Y%m%d_%H%M') + '.shp'

try:
    make_shp(location_list, shp_filename)
except AttributeError:
    print "Error: shapefile filename already exists."
except IndexError:
    print "Error: no connection to database, please try again."
else:
    print "Shapefile written succesfully."
