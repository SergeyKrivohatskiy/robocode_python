#!/usr/bin/env python
__author__ = 'Sergey Krivohatskiy'
from robot import Robot


# http://robowiki.net/wiki/Robocode/My_First_Robot
class MyFirstRobot(Robot):
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


# sample.Fire
class Fire(Robot):
    def __init__(self, *args, **kwargs):
        super(Fire, self).__init__(*args, **kwargs)
        self.dist = 50

    def run(self):
        while True:
            self.turn_gun_right(5)

    def on_scanned_robot(self, event):
        if event.distance < 50 and self.energy > 50:
            self.fire(3)
        else:
            self.fire(1)

    def on_hit_by_bullet(self, event):
        self.turn_left(90 - event.get_bearing())
        self.ahead(self.dist)
        self.dist *= -1
