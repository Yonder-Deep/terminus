from command_processor import *
from command_io import decode_json

KEYWORDS_HANDLERS = {'CAL': calibrate_motor,
                     'MAN': manual_control,
                     'BAL': ballast,
                     'NAV': auto_navigate,
                     'ALIVE': echo_status}


def parse_command(current_state_info, json_string):
    print("Packet->" + json_string + "<-")
    decoded_dict = decode_json(json_string)
    assert decoded_dict['cmd'] in KEYWORDS_HANDLERS, 'Handler missing for command ' + decoded_dict['cmd']
    return KEYWORDS_HANDLERS[decoded_dict['cmd']](current_state_info['last_state'], decoded_dict)
