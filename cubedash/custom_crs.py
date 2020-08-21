'''
These EPSG codes need to be entered into the database with the same PROJ String definition as here.
This is done to create an extra layer and avoid the need to make changes to the proj/pyproj library
'''
CUSTOM_CRS_CODE = {
    'epsg:10001': '+proj=aea +lat_0=-12 +lon_0=-54 +lat_1=-2 +lat_2=-22 +x_0=5000000 +y_0=10000000 +ellps=GRS80 +units=m +no_defs',
    'epsg:10002': '+proj=aea +lat_1=-1 +lat_2=-29 +lat_0=0 +lon_0=-54 +x_0=0 +y_0=0 +ellps=GRS80 +units=m +no_defs +type=crs',
    'epsg:10003': '+proj=aea +lat_1=-1 +lat_2=-29 +lat_0=0 +lon_0=-54 +x_0=0 +y_0=0 +ellps=GRS80 +units=m +no_defs'
}

'''
This option is being defined to enable the use of custom grids to be more easily worked within the explorer, 
this avoids the need to assume characteristics on the data, leaving it to those who configure the 
system to define the CRS that should be used
'''
SCHEMA_FOOTPRINT_SRID = 10001
