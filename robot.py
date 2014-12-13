#!/usr/bin/env python
__author__ = 'Sergey Krivohatskiy'


class Robot(object):
    def __init__(self, game_controller):
        self.position = (0, 0)
        self.controller = game_controller

    def get_x(self):
        return self.position[0]

    def get_y(self):
        return self.position[1]

    def run(self):
        pass

    def fire(self, power):
        pass

    def ahead(self, distance):
        pass

    def back(self, distance):
        pass

    def do_nothing(self):
        pass

    def get_battle_field_width(self):
        pass

    def get_battle_field_height(self):
        pass

    def get_energy(self):
        pass