from command_processor import *
from command_io import decode

KEYWORDS_HANDLERS = {'CAL': calibrate_motor,
                     'MAN': manual_control,
                     'BAL': ballast,
                     'NAV': auto_navigate,
                     'ALIVE': echo_status}


def parse_command(current_state_info, json_string):
    decoded_dict = decode(json_string)
    assert decoded_dict['cmd'] in KEYWORDS_HANDLERS, 'Handler missing for command ' + decoded_dict['cmd']
    return KEYWORDS_HANDLERS[decoded_dict['cmd']](decoded_dict)
