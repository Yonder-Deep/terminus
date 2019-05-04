import utm
import math
import numbers


class GeoTool:
    def __init__(self, origin_lat, origin_lon):
        self.origin_easting, self.origin_northing, self.origin_zone_num, self.origin_zone_letter = self.convert_axis(
            origin_lat, origin_lon)

    @staticmethod
    def convert_axis(lat, lon):
        # Validate location
        assert isinstance(lat, numbers.Number), 'Latitude has to be a number!'
        assert isinstance(lon, numbers.Number), 'Longitude has to be a number!'
        assert -90 <= lat <= 90, 'Latitude has to be within -90 and 90!'
        assert -180 <= lon <= 180, 'Longitude has to be within -180 and 180!'

        return utm.from_latlon(lat, lon)

    @staticmethod
    def convert_latlon(easting, northing, zone_num, zone_letter):
        # TODO: asserts
        return utm.to_latlon(easting, northing, zone_num, zone_letter)

    def get_location(self, lat, lon):
        x, y, _, _ = self.convert_axis(lat, lon)
        x_diff = x - self.origin_easting
        y_diff = y - self.origin_northing
        return x_diff, y_diff

    def calc_distance(self, orig_lat, orig_lon, dest_lat, dest_lon):
        start = self.convert_axis(orig_lat, orig_lon)
        end = self.convert_axis(dest_lat, dest_lon)
        return math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)

    def to_latlong(self, offset_x, offset_y):
        easting = self.origin_easting + offset_x
        northing = self.origin_northing + offset_y
        # TODO: Assuming in the same zone as origin
        return self.convert_latlon(easting, northing, self.origin_zone_num, self.origin_zone_letter)
