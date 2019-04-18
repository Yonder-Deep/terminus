import axis_convert

if __name__ == '__main__':

    base_station = (24.171814, 72.246094)
    g = axis_convert.GeoTool(*base_station)
    position1 = (24.171814, 72.246094)
    for i in test_pts:
        g.update_wp(*i)
        print(i, g.calculate_pid_heading(*position1))
