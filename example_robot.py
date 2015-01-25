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

    def on_scanned_robot(self, event):
        self.fire(1)

    def on_hit_by_bullet(self, event):
        self.turn_left(90 - event.get_bearing())