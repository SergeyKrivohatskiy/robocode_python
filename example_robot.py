#!/usr/bin/env python
__author__ = 'Sergey Krivohatskiy'
from robot import Robot


class ExampleRobot(Robot):
    def run(self):
        while True:
            print("ExampleRobotRun")
            self.fire(1)
            self.turn_gun_left(5)