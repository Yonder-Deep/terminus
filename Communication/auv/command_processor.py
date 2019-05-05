CALIBRATE_MOTOR_KW = ['LEFT', '']

def calibrate_motor(remaining_param):
    assert isinstance(remaining_param, list)
    assert len(remaining_param) == 1
    assert remaining_param[0] in CALIBRATE_MOTOR_KW

def manual_control(remaining_param):
    pass

def ballast(remaining_param):
    pass

def auto_navigate(remaining_param):
    pass

def echo_status(remaining_param):
    pass