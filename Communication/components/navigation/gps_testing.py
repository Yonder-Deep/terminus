import axis_convert

if __name__ == '__main__':
    orig = get_gps()
    g = axis_convert.GeoTool(*orig)
    while True:
        new = get_gps()
        print(g.get_location(*new))
