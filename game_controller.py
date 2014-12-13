#!/usr/bin/env python
__author__ = 'Sergey Krivohatskiy'
from robot import Robot


class NoRobotsException(BaseException):
    pass


class GameController(object):
    # robots_list is a list of Robot class subclasses
    def __init__(self, robots_list):
        robots_list = filter(lambda x: issubclass(x, Robot), robots_list)
        if len(robots_list) == 0:
            raise NoRobotsException()
        self.time = 0
        self.robots = map(lambda robot_class: robot_class(self), robots_list)

    def run(self):
        while True:
            self.redraw()
            self.do_robot_steps()
            self.time += 1
            self.move_bullets()
            self.move_robots()
            self.process_events()

    def do_robot_steps(self):
        pass

    def redraw(self):
        pass

    def move_bullets(self):
        pass

    def move_robots(self):
        pass

    def process_events(self):
        pass