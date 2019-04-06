import utm
import math
import numbers


class GeoTool:
    def __init__(self, origin_lat, origin_lon):
        self.origin_x, self.origin_y = self.convert_axis(origin_lat, origin_lon)

    @staticmethod
    def convert_axis(lat, lon):
        # Validate location
        assert isinstance(lat, numbers.Number), 'Latitude has to be a number!'
        assert isinstance(lon, numbers.Number), 'Longitude has to be a number!'
        assert -90 <= lat <= 90, 'Latitude has to be within -90 and 90!'
        assert -180 <= lon <= 180, 'Longitude has to be within -180 and 180!'

        return utm.from_latlon(lat, lon)[0:2]

    def get_location(self, lat, lon):
        x, y = self.convert_axis(lat, lon)
        x_diff = x - self.origin_x
        y_diff = y - self.origin_y
        return x_diff, y_diff

    def calc_distance(self, orig_lat, orig_lon, dest_lat, dest_lon):
        start = self.convert_axis(orig_lat, orig_lon)
        end = self.convert_axis(dest_lat, dest_lon)
        return math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
