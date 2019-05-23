CAL_ARGS = ['l', 'r', 'f', 'b']
MAN_ARGS = ['l', 'r', 'f', 'b']
BAL_ARGS = ['depth', 'timeout']
NAV_ARGS = ['lat', 'lon']
ALIVE_ARGS = []
STATUS_ARGS = ['lat', 'lon', 'updated', 'state']


def cal_checker(cmd_dict):
    arg_check(check_dict=cmd_dict, expected_args=CAL_ARGS)
    for arg in CAL_ARGS:
        assert isinstance(cmd_dict[arg], int), 'Argument ' + arg + ' expected to be int for: ' + str(cmd_dict)
        assert 0 <= cmd_dict[arg] <= 200, 'Argument ' + arg + ' value unexpected for: ' + str(cmd_dict)


def man_checker(cmd_dict):
    arg_check(check_dict=cmd_dict, expected_args=MAN_ARGS)
    for arg in MAN_ARGS:
        assert isinstance(cmd_dict[arg], int), 'Argument ' + arg + ' expected to be int for: ' + str(cmd_dict)
        assert 0 <= cmd_dict[arg] <= 200, 'Argument ' + arg + ' value unexpected for: ' + str(cmd_dict)


def bal_checker(cmd_dict):
    arg_check(check_dict=cmd_dict, expected_args=BAL_ARGS)
    assert isinstance(cmd_dict['depth'], int), 'Argument depth expected to be int for: ' + str(cmd_dict)
    assert 1 <= cmd_dict['depth'] <= 100, 'Argument depth value unexpected for: ' + str(cmd_dict)
    assert isinstance(cmd_dict['timeout'], int), 'Argument timeout expected to be int for: ' + str(cmd_dict)
    assert 0 <= cmd_dict['timeout'] <= 3600, 'Argument timeout value unexpected for: ' + str(cmd_dict)


def nav_checker(cmd_dict):
    arg_check(check_dict=cmd_dict, expected_args=NAV_ARGS)
    for arg in NAV_ARGS:
        assert isinstance(cmd_dict[arg], float), 'Argument ' + arg + ' expected to be float for' + str(cmd_dict)
    assert -90 <= cmd_dict['lat'] <= 90, 'Argument lat out of range -90, 90 for ' + str(cmd_dict)
    assert -180 <= cmd_dict['lon'] <= 180, 'Argument lon out of range -180, 180 for' + str(cmd_dict)
    assert 1558587000 < cmd_dict['updated'] < 7270404600, 'Argument updated has unexpected value' + str(cmd_dict)


def alive_checker(cmd_dict):
    arg_check(check_dict=cmd_dict, expected_args=ALIVE_ARGS)


def status_checker(cmd_dict):
    arg_check(check_dict=cmd_dict, expected_args=STATUS_ARGS)
    assert isinstance(cmd_dict['lat'], float), 'Argument lat expected to be float for' + str(cmd_dict)
    assert -90 <= cmd_dict['lat'] <= 90, 'Argument lat out of range -90, 90 for ' + str(cmd_dict)
    assert isinstance(cmd_dict['lon'], float), 'Argument lon expected to be float for' + str(cmd_dict)
    assert -180 <= cmd_dict['lon'] <= 180, 'Argument lon out of range -180, 180 for' + str(cmd_dict)
    assert isinstance(cmd_dict['state'], str)


def arg_check(check_dict, expected_args):
    expect_arg_length = len(expected_args)
    args = check_dict.keys()
    assert len(args) == expect_arg_length + 1, 'Expected ' + str(expect_arg_length) + ' Args for: ' + str(check_dict) # Include the 'cmd'
    for expect_arg in expected_args:
        assert expect_arg in args, 'Expected Argument ' + expect_arg + ' for decoded result: ' + str(check_dict)