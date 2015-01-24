#!/usr/bin/env python
__author__ = 'Sergey Krivohatskiy'
from robot import Robot


class ExampleRobot(Robot):
    def run(self):
        while True:
            print("ExampleRobotRun")
            self.do_nothing()
            self.turn_gun_right(90)
            self.fire(1)
            self.turn_gun_left(180)
            self.turn_left(90)
            self.ahead(100)
            self.fire(1)
            self.turn_right(90)
            self.back(100)
            self.turn_radar_right(360)