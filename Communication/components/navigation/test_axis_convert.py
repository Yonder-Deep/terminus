"""
Function to test axis_convert.py
"""
import axis_convert


def test_axis_convert_1():
    orig = (32.870065, -117.252132)
    dest = (32.870091, -117.242911)
    g = axis_convert.GeoTool(*orig)
    assert g.get_location(*dest) == (862.6577479215921, 0.8596824347041547)
