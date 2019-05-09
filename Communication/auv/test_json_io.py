from command_io import *


def test_send_nav():
    send_nav(10.1, 10.1)


def test_send_alive():
    send_alive()


def test_send_ballast():
    send_ballast(100, 10)


def test_send_calib():
    send_calibrate(True, False, True, True)


def test_send_mc():
    send_manual_control(100,100,0,0)


def test_send_status():
    send_status(50.0, 100.0, 'BAL')


if __name__ == '__main__':
    test_send_nav()
    test_send_alive()
    test_send_ballast()
    test_send_calib()
    test_send_mc()
    test_send_status()
