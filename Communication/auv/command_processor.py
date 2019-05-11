def calibrate_motor(command_dict):
    return {'last_state': 'READ',
            'next_state': 'CAL',
            'data': command_dict}


def manual_control(command_dict):
    return {'last_state': 'READ',
            'next_state': 'MAN',
            'data': command_dict}


def ballast(command_dict):
    return {'last_state': 'READ',
            'next_state': 'BAL',
            'data': command_dict}


def auto_navigate(command_dict):
    return {'last_state': 'READ',
            'next_state': 'NAV',
            'data': command_dict}


def echo_status(command_dict):
    return {'last_state': 'READ',
            'next_state': 'STATUS',
            'data': command_dict}
