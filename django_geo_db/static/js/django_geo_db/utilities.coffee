root = exports ? this
root.django_geo_db = root.django_geo_db ? {}

class GeoUtilities

  textCoordinateToGMapsDict:(stringCoordinate)->
    result = stringCoordinate.split(' ');
    return {lat:parseFloat(result[0]), lng: parseFloat(result[1])};

root.django_geo_db.GeoUtilities = GeoUtilities
