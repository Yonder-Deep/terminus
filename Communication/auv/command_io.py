import json
import command_validate
import traceback
import collections

CMD_VALIDATE = {'CAL': command_validate.cal_checker,
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


def send_status(current_lat, current_lon, current_state):  # For AUV only
    packet = {'cmd': 'STATUS',
              'lat': current_lat,
              'lon': current_lon,
              'state': current_state}
    send_dict(packet)


def send_dict(a_dict):
    print(encode_json(a_dict))


def encode_json(a_dict):
    raw = json.dumps(a_dict)
    assert decode_json(raw)
    return a_dict


def decode_json(a_json_str):
    print(a_json_str)
    cmd_dict = json.loads(a_json_str)
    cmd_dict = dict_unicode_to_string(cmd_dict)
    try:
        assert isinstance(cmd_dict, dict), "Json decoder returns type: " + str(type(cmd_dict))
        assert 'cmd' in cmd_dict.keys(), "Json decoded dict doesn't contain 'cmd': " + str(cmd_dict)
        assert cmd_dict['cmd'] in CMD_VALIDATE.keys()
        CMD_VALIDATE[cmd_dict['cmd']](cmd_dict)  # Call particular command's validator
        return cmd_dict

    except AssertionError:
        # TODO: Dump log!
        traceback.print_exc()


def dict_unicode_to_string(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(dict_unicode_to_string, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(dict_unicode_to_string, data))
    else:
        return data