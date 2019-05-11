import json
import command_validate
import traceback
import collections
import os

CMD_VALIDATE = {'CAL': command_validate.cal_checker,
                'MAN': command_validate.man_checker,
                'BAL': command_validate.bal_checker,
                'NAV': command_validate.nav_checker,
                'ALIVE': command_validate.alive_checker,
                'STATUS': command_validate.status_checker}

# Sets the PYTHONPATH to include the components.
split_path = os.path.abspath(__file__).split('/')
split_path_communication = split_path[0:len(split_path) - 2]
split_path_sensors = split_path[0:len(split_path) - 3]

components_path = "/".join(split_path_communication) + "/components"


class CommandIO:

    def __init__(self, radio):
        self.radio = radio

    def send_calibrate(self, l=True, r=True, f=True, b=True):
        packet = {'cmd': 'CAL',
                  'l': l,
                  'r': r,
                  'f': f,
                  'b': b}
        self.send_dict(packet)

    def send_manual_control(self, left, right, front, back):
        packet = {'cmd': 'MAN',
                  'l': left,
                  'r': right,
                  'f': front,
                  'b': back}
        self.send_dict(packet)

    def send_ballast(self, target_depth, timeout=60):
        packet = {'cmd': 'BAL',
                  'depth': target_depth,
                  'timeout': timeout}
        self.send_dict(packet)

    def send_nav(self, target_lat, target_lon):
        packet = {'cmd': 'NAV',
                  'lat': target_lat,
                  'lon': target_lon}
        self.send_dict(packet)

    def send_alive(self):
        packet = {'cmd': 'ALIVE'}
        self.send_dict(packet)

    def send_status(self, current_lat, current_lon, current_state):  # For AUV only
        packet = {'cmd': 'STATUS',
                  'lat': current_lat,
                  'lon': current_lon,
                  'state': current_state}
        self.send_dict(packet)

    def send_dict(self, a_dict):
        self.radio.write(encode_json(a_dict) + '\n')


def encode_json(a_dict):
    raw = json.dumps(a_dict)
    assert decode_json(raw)
    return raw


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
