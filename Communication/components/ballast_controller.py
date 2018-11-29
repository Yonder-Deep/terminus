"""
The ballast_controller class autonomously ballasts and collects data
"""


class BallastController:

    def __init__(self, horizontal_mc, vertical_mc):
        self.horizontal_mc = horizontal_mc
        self.vertical_mc = vertical_mc

    def start(self):
        self.vertical_mc.update_motor_speeds({'front': 50, 'back': 50})
        while not self.has_reached_depth():
            pass
            '''
            self.pid.adjust(self.vertical_mc)
            '''

    def has_reached_depth(self):
        return False