#!/usr/bin/env python
__author__ = 'Sergey Krivohatskiy'
from robot import Robot


class ExampleRobot(Robot):
    def run(self):
        while True:
            self.ahead(100)
            #self.turn_gun_right(360)
            self.turn_left(20)
            self.back(100)
            self.turn_gun_right(20)
            self.turn_left(20)
            self.fire(1)
            self.turn_radar_left(40)