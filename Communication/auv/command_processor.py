def calibrate_motor(last_state, command_dict):
    return {'last_state': last_state,
            'next_state': 'CAL',
            'data': command_dict}


def manual_control(last_state, command_dict):
    return {'last_state': last_state,
            'next_state': 'MAN',
            'data': command_dict}


def ballast(last_state, command_dict):
    return {'last_state': last_state,
            'next_state': 'BAL',
            'data': command_dict}


def auto_navigate(last_state, command_dict):
    return {'last_state': last_state,
            'next_state': 'NAV',
            'data': command_dict}


def echo_status(last_state, command_dict):
    return {'last_state': last_state,
            'next_state': 'STATUS',
            'data': command_dict}
