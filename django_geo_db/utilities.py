from decimal import Decimal

def get_lat_lon_from_string(latLonString):
    lat,lon = latLonString.split(' ')
    lat = get_standardized_coordinate(lat)
    lon = get_standardized_coordinate(lon)
    return (Decimal(lat), Decimal(lon))

def get_standardized_coordinate(latOrLon):
    objInt, objFrac = str(latOrLon).split('.', 1)
    objFrac = str(objFrac)[0:5]
    return Decimal('{0}.{1}'.format(objInt, objFrac))
