"""
Function to test axis_convert.py
"""
import axis_convert


def test_axis_convert_1():
    orig = (32.870065, -117.252132)
    dest = (32.870091, -117.242911)
    g = axis_convert.GeoTool(*orig)
    assert g.get_location(*dest) == (862.6577479215921, 0.8596824347041547)


def test_convert_to_latlon_1():
    orig = (78.3549, 14.79119)
    g = axis_convert.GeoTool(*orig)
    assert g.to_latlong(100000, 100000) == (79.21752940261766, 19.567340615934533)


def test_get_heading_1():
    test_pts = [(0, 2), (1, 2), (2, 2), (2, 1), (2, 0),
                (2, -1), (2, -2), (1, -2), (0, -2),
                (-1, -2), (-2, -2), (-2, -1), (-2, 0),
                (-2, 1), (-2, 2), (-1, 2)]
    base_station = (78.3549, 14.79119)
    g = axis_convert.GeoTool(*base_station)
    position1 = (78.3549, 14.79119)
    for i in test_pts:
        g.update_wp(*i)
        print(i, g.calculate_pid_heading(*position1))