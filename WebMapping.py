# Eline van Elburg
# Web Mapping demo
# 21-01-2016

# Just in case
list_in_case = [['Wageningen', [51.9691868, 5.6653948]],
                ['Amsterdam', [52.3702157, 4.895167900000001]],
                ['Fuji', [35.3605555, 138.7277777]],
                ['Lima', [-12.046374, -77.0427934]],
                ['Bennekom', [51.99910389999999, 5.674754399999999]],
                ['Cairo', [30.0444196, 31.2357116]],
                ['Sao Paulo', [-23.5505199, -46.63330939999999]],
                ['Brisbane', [-27.4710107, 153.0234489]],
                ['New York', [40.7127837, -74.0059413]]]

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

def make_shp(locationList):
    # Set spatial reference
    spatialReference = osgeo.osr.SpatialReference()
    spatialReference.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')

    # Create shapefile
    driver = osgeo.ogr.GetDriverByName('ESRI Shapefile')
    fileName = 'CityLocation_' + time.strftime('%Y%m%d_%H%M_%S') + '.shp'
    shapeData = driver.CreateDataSource(fileName)

    # Create Layer
    layer = shapeData.CreateLayer('cities', spatialReference, osgeo.ogr.wkbPoint)
    layerDefinition = layer.GetLayerDefn()

    i = 1
    # Create Points
    for city_loc in locationList:
        city = city_loc[0]
        coords = city_loc[1]
        print coords
        # Create point
        geometry = osgeo.ogr.Geometry(osgeo.ogr.wkbPoint)
        geometry.SetPoint(0, coords[0], coords[1])
        # Create feature
        feature = osgeo.ogr.Feature(layerDefinition)
        feature.SetGeometry(geometry)
        feature.SetFID(i)
        # Save feature
        layer.CreateFeature(feature)
        # Cleanup
        geometry.Destroy()
        feature.Destroy()
        i += 1
    # Cleanup
    shapeData.Destroy()
        
# Main code
string_cities = read_file("C:/Users/Eline/Documents/Python/Geo-Scripting/WebMapping/cities.txt")
list_cities = split_string(string_cities)

location_list = []
for city in list_cities:
    location = get_location(city)
    location_list.append([city,location])

make_shp(location_list)
