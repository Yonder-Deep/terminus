import math


class AngleConvert:
    def __init__(self, offset=0):
        self.offset = offset

    def convert(self, angle):
        return (angle + 360 - self.offset) % 360

    def update_offset(self, offset):
        self.offset = offset

    @staticmethod
    def get_heading(y, x):
        degree = math.degrees(math.atan2(y, x))
        return (degree + 360 - 90) % 360


if __name__ == '__main__':
    # Test
    a = AngleConvert(20)
    test_angles = [i for i in range(361)]
    for i in test_angles:
        print(f'{i}\t{a.convert(i)}')
