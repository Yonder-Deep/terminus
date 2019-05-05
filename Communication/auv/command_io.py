import json
import command_validate

CMD_LIST = {'CAL': command_validate.cal_checker,
            'MAN': command_validate.man_checker,
            'BAL': command_validate.bal_checker,
            'NAV': command_validate.nav_checker,
            'ALIVE': command_validate.alive_checker,
            'STATUS': command_validate.status_checker}


def send_calibrate(l=True, r=True, f=True, b=True):
    packet = {'cmd': 'CAL',
              'l': l,
              'r': r,
              'f': f,
              'b': b}
    send_dict(packet)


def send_manual_control(left, right, forward, back):
    packet = {'cmd': 'MAN',
              'l': left,
              'r': right,
              'f': forward,
              'b': back}
    send_dict(packet)


def send_ballast(target_depth, timeout=60):
    packet = {'cmd': 'BAL',
              'depth': target_depth,
              'timeout': timeout}
    send_dict(packet)


def send_nav(target_lat, target_lon):
    packet = {'cmd': 'NAV',
              'lat': target_lat,
              'lon': target_lon}
    send_dict(packet)


def send_alive():
    packet = {'cmd': 'ALIVE'}
    send_dict(packet)


def send_status(current_lat, current_lon, current_state): # For AUV only
    packet = {'cmd': 'BAL',
              'lat': current_lat,
              'lon': current_lon,
              'state': current_state}
    send_dict(packet)


def send_dict(a_dict):
    raw = json.dumps(a_dict)
    assert decode(raw)
    print(raw)


def decode(a_json_str):
    cmd_dict = json.load(a_json_str)
    try:
        assert isinstance(cmd_dict, dict)
        assert 'cmd' in cmd_dict.keys()
        assert cmd_dict['cmd'] in CMD_LIST.keys()
        assert CMD_LIST[cmd_dict['cmd']](cmd_dict)  # Call particular command's validator

    except AssertionError:
        # TODO: Dump log!
        print("INVALID COMMAND")