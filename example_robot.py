#!/usr/bin/env python
__author__ = 'Sergey Krivohatskiy'
from robot import Robot


class ExampleRobot(Robot):
    def run(self):
        while True:
            print("ExampleRobotRun")
            self.do_nothing()
            self.turn_gun_right(90)
            self.turn_gun_left(180)
            self.turn_left(90)
            self.turn_radar_right(360)