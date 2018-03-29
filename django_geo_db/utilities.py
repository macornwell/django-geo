import io
from decimal import Decimal
import random
from PIL import Image

from django_geo_db.math import Translations

MAP_STAR_PERCENTAGE = 0.10


def get_lat_lon_from_string(latLonString):
    lat,lon = latLonString.split(' ')
    lat = get_standardized_coordinate(lat)
    lon = get_standardized_coordinate(lon)
    return (Decimal(lat), Decimal(lon))


def get_standardized_coordinate(latOrLon):
    objInt, objFrac = str(latOrLon).split('.', 1)
    objFrac = str(objFrac)[0:5]
    return Decimal('{0}.{1}'.format(objInt, objFrac))


class LatLon:
    """
    Represents a LatLon for manipulation
    """
    lat = None
    lon = None

    @staticmethod
    def parse_string(coordinate_string):
        """
        Parses a coordinate string in the format of lat lon
        -lat -lon
        :param coordinate_string: The string to parse
        :return: Returns a LatLon object.
        """
        lat, lon = coordinate_string.split(' ', 1)
        latLon = LatLon()
        latLon.lat = get_standardized_coordinate(lat)
        latLon.lon = get_standardized_coordinate(lon)
        return latLon


class BoundingBox:
    """
    A bounding box.
    """

    def __init__(self, ne, sw):
        self.__north_east = ne
        self.__south_west = sw

    def get_north_east(self):
        return self.__north_east

    def get_south_east(self):
        return LatLon.parse_string('{0} {1}'.format(self.__south_west.lat, self.__north_east.lon))

    def get_north_west(self):
        return LatLon.parse_string('{0} {1}'.format(self.__north_east.lat, self.__south_west.lon))

    def get_south_west(self):
        return self.__south_west

    def is_lat_lon_inside_bounding_box(self, lat_lon):
        lat = lat_lon.lat
        lon = lat_lon.lon
        lat_passes = self.get_north_west() >= lat >= self.get_south_west().lat
        lon_passes = self.get_north_west() >= lon >= self.get_north_east().lon
        return lat_passes and lon_passes

    def random_coordinate_in_bounding_box(self):
        random_lat = random.uniform(float(self.get_north_west().lat), float(self.get_south_west().lat))
        random_lon = random.uniform(float(self.get_north_west().lon), float(self.get_north_east().lon))
        latLon = LatLon()
        latLon.lat = random_lat
        latLon.lon = random_lon
        return latLon


class GeoResolutionAlgorithm:

    def __init__(self, bounding_box):
        self.__bb = bounding_box

    def lat_db_resolution(self):
        nw = str(self.__bb.get_north_west().lat)
        sw = str(self.__bb.get_south_west().lat)

        result = [False]
        # Must be in the same quandrants
        if nw[0] is '-' and sw[0] is '-':
            result[True]
            nw = nw[1:]
            sw = sw[1:]
        elif nw[0] is '-':
            return None  # Special Case
        elif sw[0] is '-':
            return None  # Special Case
        elif len(nw) != len(sw):
            return None  # Special Case
        elif nw[0] != sw[0]:
            return None  # Nothing to do here.

        leading_zeros = 8 - len(nw)
        for i in range(0, leading_zeros):
            result.append(0)

        end_found = False
        for i in range(0, len(nw)):
            if nw[i] is '.':
                continue
            high = int(nw[i])
            low = int(sw[i])
            if end_found:
                result.append(-1)
            else:
                if high is low:
                    result.append(high)
                else:
                    end_found = True
                    result.append(-1)
        return result

    def lon_db_resolution(self):
        nw = str(self.__bb.get_north_west().lon)
        ne = str(self.__bb.get_north_east().lon)
        result = [False]
        # Must be in the same quandrants
        if nw[0] is '-' and ne[0] is '-':
            result[0] = True
            nw = nw[1:]
            ne = ne[1:]
        elif nw[0] is '-':
            return None  # Special Case
        elif ne[0] is '-':
            return None  # Special Case
        elif len(nw) != len(ne):
            return None  # Special Case
        elif nw[0] != ne[0]:
            return None  # Nothing to do here.

        leading_zeros = 9 - len(nw)
        for i in range(0, leading_zeros):
            result.append(0)

        end_found = False
        for i in range(0, len(nw)):
            if nw[i] is '.':
                continue
            high = int(nw[i])
            low = int(ne[i])
            if end_found:
                result.append(-1)
            else:
                if high is low:
                    result.append(high)
                else:
                    end_found = True
                    result.append(-1)
        return result


class BoundingBoxAndMap:
    """
    A class that allows the interactions of a GeoCoordinate bounding
    box with it's presentation as a coordinate space Map.
    This allows translations between the two such as finding the x,y of an arbitrary GeoCoordinate.
    """
    bounding_box = None
    width = None
    height = None

    def get_coordinate_space(self, lat, lon):
        """
        Converts a GeoCoordinate's lat lon into coordinate space x,y
        Notes: (0,0) is the top left corner also the North West Corner.
        Lat = Y and Lon = X
        :param lat:
        :param lon:
        :return:  (x,y)
        """
        # Note: Lat = Y & Lon = X
        # Step 1: Move the north west corner of the Bounding Box to (0,0)
        se = self.bounding_box.get_south_east()
        bb_max_lat = se.lat
        bb_max_lon = se.lon
        nw = self.bounding_box.get_north_west()
        bb_min_lat = nw.lat
        bb_min_lon = nw.lon

        change_y = bb_min_lat * -1
        change_x = bb_min_lon * -1
        bb_small_lat = bb_max_lat + change_y
        bb_small_lon = bb_max_lon + change_x

        # Step 2 Move coordinate with the same vector as the bounding box.
        new_coord_lat = lat + change_y
        new_coord_lon = lon + change_x

        # Step 3 Apply A Linear Proportion to the coordinate's location in the original bounding box, with the final one.
        new_y = new_coord_lat * self.height / bb_small_lat
        new_x = new_coord_lon * self.width / bb_small_lon
        return int(new_x), int(new_y)


class GeographicRayTest:
    """
    Determines if a Geo Coordinate is located inside an arbitrary area.
    """
    def coordinate_is_inside_area(lat, lon, coord_list):

        length = len(coord_list)
        north_boundary = None
        south_boundary = None
        west_boundary = None
        east_boundary = None

        for i in range(length):
            if i == length - 1:
                break
            a = coord_list[i]
            b = coord_list[i+2]

            pass


class MarkedMap:
    """
    A map that is marked on.
    """

    def __init__(self, data_storage, map_bytes, location_bounds):
        self.data_storage = data_storage
        self.map_bytes = map_bytes
        self.location_bounds = location_bounds

    def __get_star(self):
        return self.data_storage.get_star()

    def add_star_to_base_map(self, coord_obj, marker_size=MAP_STAR_PERCENTAGE):
        # 1. Get Star, translate star to be the standard size relative to picture size.
        coord_star = self.__get_star()

        map_file = io.BytesIO(self.map_bytes)
        map_image = Image.open(map_file)
        map_width, map_height = map_image.size

        star_x, star_y = Translations.rectangle_reduction(map_width, map_height, marker_size)
        changed_star_file = io.BytesIO()
        with io.BytesIO(coord_star) as star_file:
            im = Image.open(star_file)
            im.thumbnail((star_x, star_y), Image.ANTIALIAS)
            im.save(changed_star_file, "PNG")

        # 2. Find the (x,y) for the coordinate that will be the center point of the star on the map.
        bb_and_map = BoundingBoxAndMap()
        bb_and_map.width = map_width
        bb_and_map.height = map_height
        bb_and_map.bounding_box = self.location_bounds.get_bounding_box()
        center_x, center_y = bb_and_map.get_coordinate_space(coord_obj.lat, coord_obj.lon)

        # 3. Instead of using the center we need to offset it to the bottom left corner of the star.
        star_image = Image.open(changed_star_file)
        star_width, star_height = star_image.size
        half_x = star_width // 2
        half_y = star_height // 2
        pos_x = center_x - half_x
        pos_y = center_y - half_y

        # 4. Combine Base Map and Star
        overlay = Image.open(changed_star_file).convert("RGBA")
        image_copy = map_image.copy()
        position = (pos_x, pos_y)
        image_copy.paste(overlay, position, mask=overlay)
        combined_image = io.BytesIO()
        image_copy.save(combined_image, format="PNG")
        return combined_image


def plot_map(coordinates, storage, location_map,
             map_bounds, marker, marker_size_percent):

    map_data = storage.get_static_or_media_data(location_map.map_file_url)
    marked_map = MarkedMap(storage, map_data, map_bounds)

    markers = {
        'star': 'add_star_to_base_map',
    }

    combined = map_data
    for coord in coordinates:
        method_name = markers[marker]
        combined = getattr(marked_map, method_name)(coord, marker_size=marker_size_percent).getvalue()
        # Recreate the object to use the updated map because we're adding many marks to it.
        marked_map = MarkedMap(storage, combined, map_bounds)
    return combined
