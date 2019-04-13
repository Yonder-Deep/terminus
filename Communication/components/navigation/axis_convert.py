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
        """
        Convert a lat lon into our axis
        :param lat:
        :param lon:
        :return:
        """
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

    def update_wp(self, offset_x, offset_y):
        # TODO: asserts for input
        self.wp_x = offset_x
        self.wp_y = offset_y

    def calculate_pid_heading(self, current_lat, current_lon):
        assert('wp_x' in dir(self)), 'You need to set a Waypoint first using update_wp()'
        assert('wp_y' in dir(self)), 'You need to set a Waypoint first using update_wp()'
        current_x, current_y = self.get_location(current_lat, current_lon)
        dx = abs(current_x - self.wp_x)
        dy = abs(current_y - self.wp_y)
        theta = math.degrees(math.atan2(dy, dx))
        assert 0 <= theta  <= 90
        # Find out quadrant
        if current_x <= self.wp_x and current_y <= self.wp_y:  # Going up right
            angle = 90 - theta
            assert 0 <= angle <= 90
            return angle
        elif current_x <= self.wp_x and current_y >= self.wp_y:  # Going down right
            angle = 90 + theta
            assert 90 <= angle <= 180
            return angle
        elif current_x >= self.wp_x and current_y >= self.wp_y:  # Going down left
            angle = -90 - theta
            assert -180 <= angle <= -90
            return angle
        elif current_x >= self.wp_x and current_y <= self.wp_y:  # Going up left
            angle = -90 + theta
            assert -90 <= angle <= 0
            return angle
