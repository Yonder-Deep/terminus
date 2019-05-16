def calibrate_motor(hold_state, command_dict):
    return {'hold_state': hold_state,
            'next_state': 'CAL',
            'data': command_dict}


def manual_control(hold_state, command_dict):
    return {'hold_state': hold_state,
            'next_state': 'MAN',
            'data': command_dict}


def ballast(hold_state, command_dict):
    return {'hold_state': hold_state,
            'next_state': 'BAL',
            'data': command_dict}


def auto_navigate(hold_state, command_dict):
    return {'hold_state': hold_state,
            'next_state': 'NAV',
            'data': command_dict}


def echo_status(hold_state, command_dict):
    return {'hold_state': hold_state,
            'next_state': 'STATUS',
            'data': command_dict}
