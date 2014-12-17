#!/usr/bin/env python
__author__ = 'Sergey Krivohatskiy'
from robot import Robot


class ExampleRobot(Robot):
    def run(self):
        while True:
            self.set_rot_speed(8)
            self.set_vel(1)
            for i in range(0, 50):
                self.do_nothing()
            self.set_vel(-1)
            for i in range(0, 50):
                self.do_nothing()