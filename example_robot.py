#!/usr/bin/env python
__author__ = 'Sergey Krivohatskiy'
from robot import Robot


class ExampleRobot(Robot):
    def run(self):
        while True:
            self.ahead(100)
            self.turn_gun_right(360)
            self.back(100)
            self.turn_gun_left(360)