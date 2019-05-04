import axis_convert
from test import get_gps

if __name__ == '__main__':
    orig = get_gps()
    g = axis_convert.GeoTool(*orig)
    gg = gps(mode=WATCH_ENABLE)
    while True:
        new = get_gps()
        print(g.get_location(*new))
